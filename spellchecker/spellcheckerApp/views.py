from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse
import os, sys, logging, logging.handlers, re
from datetime import datetime
from logging import handlers, Formatter
from logging.handlers import RotatingFileHandler
import jamspell
import requests
import simplejson, json, math
from requests.auth import HTTPBasicAuth
from .models import SearchEngineIndexerConfigs
from .kubernetes import getConfigMapSettings
from .propertiesFiles import saveSettings, loadSettings

initialPath = ""
try:
    __file__
    initialPath = os.path.dirname(os.path.abspath(__file__+"/../"))
except NameError:
    initialPath = os.path.abspath('')
    
sys.path.append(initialPath)

# Ruta al archivo .env
archivo_env = initialPath+'/.env'

#### LOGGING CLASS SETTINGS (py25+, py30+)
file_name = datetime.now().strftime("%y-%b-%d_%H:%M")+'.log'
f = logging.Formatter(fmt='%(levelname)s<;>%(asctime)s<;>%(message)s',datefmt="%Y-%m-%d:%H:%M:%S")
handlers = [
	logging.handlers.RotatingFileHandler(
		initialPath+'/logs/'+file_name, encoding='utf8',
		maxBytes=1000*1000*150, backupCount=100),
	logging.StreamHandler()
]

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

for h in handlers:
	h.setFormatter(f)
	h.setLevel(logging.DEBUG)
	root_logger.addHandler(h)
#### END LOGGING SETTINGS

#Init objects jamspell
correctorBasic = jamspell.TSpellCorrector()
correctorEntity = jamspell.TSpellCorrector()

trainFile = initialPath+"/diccionario/content/cleanCompleteContent.txt"
alphabetFile = initialPath+"/diccionario/train/alphabet_es.txt"
modelEntity = initialPath+"/diccionario/train/model_entity.bin"
modelBasic = initialPath+"/diccionario/train/model_basic.bin"
filenamesVoc = ['solrContent.txt', 'vocabulary_extract_basic.txt']

if (os.path.exists(modelEntity) and os.path.getsize(modelEntity) > 0):
	logging.info("Cargando modelo de la entidad...")
	correctorEntity.LoadLangModel(modelEntity)
	logging.info("Modelo de la entidad cargado...")
else:
	logging.info("Cargando modelo basico...")
	correctorBasic.LoadLangModel(modelBasic)
	logging.info("Modelo basico cargado...")

#active or empty
#proxy = "active"
proxy = ""

#Get configmap settings
configmapSettings = getConfigMapSettings(proxy)

#Save configmap settings
if(configmapSettings):
	saveSettings(configmapSettings)
	
#Load configmap settings
configsSettings = loadSettings()
if(configsSettings):
	# Leer el contenido actual del archivo .env
	with open(archivo_env, 'r') as f:
		lineasEnv = f.readlines()
		
	for i, linea in enumerate(lineasEnv):
		if linea.startswith("DB_NAME="):
			lineasEnv[i] = "DB_NAME="+configsSettings.get("mysql.database").data+"\n"
		elif linea.startswith("DB_USER="):
			lineasEnv[i] = "DB_USER="+configsSettings.get("mysql.username").data+"\n"
		elif linea.startswith("DB_PASSWORD="):
			lineasEnv[i] = "DB_PASSWORD="+configsSettings.get("mysql.password").data+"\n"
		elif linea.startswith("DB_HOST="):
			lineasEnv[i] = "DB_HOST="+configsSettings.get("mysql.host").data+"\n"
		elif linea.startswith("DB_PORT="):
			lineasEnv[i] = "DB_PORT="+configsSettings.get("mysql.port").data+"\n"
			
	# Escribir las modificaciones de vuelta al archivo .env
	with open(archivo_env, 'w') as f:
		f.writelines(lineasEnv)

def home(request):
	return HttpResponse('Home')
	
def active(request):
	return HttpResponse('Servicio activo')

def handler404(request, *args, **argv):
	response = render(request,'/opt/spellchecker/templates/base/404.html', {})
	response.status_code = 404
	return response

def handler500(request, *args, **argv):
	response = render(request,'/opt/spellchecker/templates/base/500.html', {})
	response.status_code = 500
	return response
	

## Functions spellchecker

def getSearchEngineIndexer(searchEngineId):
	try:
		print(searchEngineId)
		seObj	= SearchEngineIndexerConfigs.objects.get(search_engine_config=searchEngineId)
		return seObj
	except SearchEngineIndexerConfigs.DoesNotExist:
		return "notSearchEngine"
	except SearchEngineIndexerConfigs.MultipleObjectsReturned:
		return "multiSearchEngine"

def downloadContent(searchEngineId):
	searchEngine = getSearchEngineIndexer(searchEngineId)
	print(searchEngine)
	resp = None
	if(searchEngine=="notSearchEngine"):
		logging.error("El buscador no existe")
	elif(searchEngine=="multiSearchEngine"):
		logging.error("Multiples buscadores encontrados")
	else:
		ipSolr=searchEngine.ip_dns
		portSolr=searchEngine.port
		coreSolr=searchEngine.core
		pathSolr=""
		
		if(portSolr):
			pathSolr='http://'+ipSolr+':'+portSolr+"/solr/"+coreSolr
		else:
			pathSolr='http://'+ipSolr+"/solr/"+coreSolr
			
		pathCount = pathSolr+"/select?q=content%3A%5B*%20TO%20*%5D&rows=0"
		logging.info(pathCount)
		try:
			configsSettings = loadSettings()
			solrUsername = configsSettings.get("solr.cluster.username").data
			solrPassword = configsSettings.get("solr.cluster.password").data
			
			resp = requests.get(pathCount, auth = HTTPBasicAuth(solrUsername, solrPassword))
			resp_string = resp.content.decode('utf8') 
			jsonResponse = json.loads(resp_string)
			largeResponse=int(jsonResponse['response']['numFound'])
			lenBatch=10000
			logging.info("Se haran "+str(int(largeResponse/lenBatch)+1)+" consultas")
			with open(initialPath+"/diccionario/content/solrContent.txt","w") as file:
				for i in range(int(largeResponse/lenBatch)+1):
					initial=str(lenBatch*i)
					final=str(int(initial)+lenBatch-1)
					pathContent = pathSolr+"/select?q=content%3A%5B*%20TO%20*%5D&rows="+str(lenBatch-1)+"&start="+initial+"&wt=csv&fl=content"
					logging.info(pathContent)
					resp = requests.get(pathContent, auth = HTTPBasicAuth(solrUsername, solrPassword))
					content = re.sub(r"\\n", "", resp.content.decode('utf8'))
					file.write(content)
		except:
			logging.error("Error en solr")
	return resp
	
def mergeContent():
	with open(initialPath+'/diccionario/content/completeContent.txt', 'w') as outfile:
		for names in filenamesVoc:
			with open(initialPath+"/diccionario/content/"+names) as infile:
				outfile.write(infile.read())
			outfile.write("\n")
			
def cleanContent():
	f = open(initialPath+"/diccionario/content/completeContent.txt", "r")
	y=""
	stringContent=""
	for x in f:
		y=y+x
	w = list(set(y.split('\\n')))
	for l in w:
		remvQuo = re.sub(r'\"', '', l)
		remvBackSl = re.sub(r'\\', '', remvQuo)
		addSpaces = " ".join(remvBackSl.split())
		stringContent=stringContent+addSpaces
	text_file = open(trainFile, "w")
	n = text_file.write(stringContent)
	text_file.close()
	
def trainLangModelEntity(trainText, alphabetFile, modelEntity):
	correctorEntity.TrainLangModel(trainText, alphabetFile, modelEntity)

def createModel(request):
	if request.method=="GET":
		searchEngine = request.GET.get('searchEngine')
		if(searchEngine != None):
			logging.info("Descargando contenido de la entidad...")
			resp = downloadContent(searchEngine)
			logging.info("Descarga finalizada...")
			codeResp = str(resp).replace("<Response [","").replace("]>","")
			logging.info(codeResp=="200")
			if(codeResp=="200"):
				logging.info("Uniendo archivos entidad y basico...")
				mergeContent()
				logging.info("Union finalizada...")
				logging.info("Limpiando archivo para el modelo...")
				cleanContent()
				logging.info("Limpieza finalizada...")
				logging.info("Entrenando modelo...")
				trainLangModelEntity(trainFile,alphabetFile,modelEntity)
				logging.info("Modelo entrenado...")
				logging.info("Cargando nuevo modelo...")
				global correctorEntity
				correctorEntity.LoadLangModel(modelEntity)
				logging.info("Modelo cargado...")
				return HttpResponse("Modelo creado...", status=codeResp)
			else:
				return HttpResponse("Error al crear el modelo...", status=codeResp)
		else:
			return HttpResponse("Por favor indique el id del buscador")
			
def loadModels(request):
	if request.method=="GET":
		typeSpell = request.GET.get('typeSpell')
		if(typeSpell != None):
			logging.info("Cargando modelo "+typeSpell+"...")
			if(typeSpell=="basic"):
				global correctorBasic
				correctorBasic=jamspell.TSpellCorrector()
				correctorBasic.LoadLangModel(modelBasic)
			else:
				global correctorEntity
				correctorEntity=jamspell.TSpellCorrector()
				correctorEntity.LoadLangModel(modelEntity)
			logging.info("Carga finalizada del modelo "+typeSpell+"...")
			return HttpResponse("Carga finalizada del modelo "+typeSpell+"...")
		else:
			return HttpResponse("Por favor indique el tipo de corrección que desea cargar typeSpell= 'Básico(basic)' o Entidad(entity)")
			
def wordSpell(request):
	if request.method=="GET":
		query = request.GET.get('query')
		if(query != None):
			try:
				typeSpell = request.GET.get('typeSpell')
				if(typeSpell=="entity"):
					global correctorEntity
					if(correctorEntity != None):
						corrected_q = correctorEntity.FixFragment(query)
					else:
						correctorEntity=jamspell.TSpellCorrector()
						correctorEntity.LoadLangModel(modelEntity)
						corrected_q = correctorEntity.FixFragment(query)
				elif(typeSpell=="basic"):
					global correctorBasic
					if(correctorBasic != None):
						corrected_q = correctorBasic.FixFragment(query)
					else:
						correctorBasic=jamspell.TSpellCorrector()
						correctorBasic.LoadLangModel(modelBasic)
						corrected_q = correctorBasic.FixFragment(query)
				else:
					if(correctorBasic != None):
						corrected_q = correctorBasic.FixFragment(query)
					else:
						correctorBasic=jamspell.TSpellCorrector()
						correctorBasic.LoadLangModel(modelBasic)
						corrected_q = correctorBasic.FixFragment(query)
				
				if(corrected_q.strip()==query.strip()):
					corrected_q="sin_correccion"
				logging.info(corrected_q)
				return HttpResponse(corrected_q)
			except Exception as e: 
				logging.error(e)
				return HttpResponse("Error "+str(e))
		else:
			return HttpResponse('active')
	else:
		return HttpResponse('active')