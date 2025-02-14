import os, sys, logging, logging.handlers
from datetime import datetime
from logging import handlers, Formatter
from logging.handlers import RotatingFileHandler
from minio import Minio
import urllib3
from .propertiesFiles import loadPropertiesAWS

initialPath = ""
try:
    __file__
    initialPath = os.path.dirname(os.path.abspath(__file__+"/../"))
except NameError:
    initialPath = os.path.abspath('')
    
sys.path.append(initialPath)

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

def downloadConfigCrawler(proxy):
	logging.info("Leyendo archivo properties aws_s3")
	configs = loadPropertiesAWS()
	
	client = None
	if(proxy=="active"):
		client = Minio(
			configs.get("aws.s3.server").data,
			access_key=configs.get("aws.s3.access-key").data,
			secret_key=configs.get("aws.s3.secret-key").data,
			region=configs.get("aws.s3.region").data,
			secure=False,
			http_client=urllib3.ProxyManager(
				"http://"+configs.get("aws.s3.server-proxy").data+":"+configs.get("aws.s3.port-proxy").data+"/",
				timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
				cert_reqs="CERT_NONE",
				retries=urllib3.Retry(
					total=5,
					backoff_factor=0.2,
					status_forcelist=[500, 502, 503, 504],
				),
			),
		)
	else:
		client = Minio(
			configs.get("aws.s3.server").data,
			access_key=configs.get("aws.s3.access-key").data,
			secret_key=configs.get("aws.s3.secret-key").data,
			region=configs.get("aws.s3.region").data,
			secure=False,
		)
		
	logging.info("Autenticación correcta...")
			
	try:
		if not os.path.exists(os.path.dirname(initialPath+"/Kubernetes/crawler/")):
			os.makedirs(os.path.dirname(initialPath+"/Kubernetes/crawler/"))
			logging.info("Directorio creado...")
		
		kubeConfigPath=""
		keyCrawler=None
		if(proxy=="active"):	
			kubeConfigPath = initialPath + "/Kubernetes/crawler/config_proxy"
			keyCrawler = configs.get("aws.s3.key-crawler").data + "/config_proxy"
		else:
			kubeConfigPath = initialPath + "/Kubernetes/crawler/config";
			keyCrawler = configs.get("aws.s3.key-crawler").data + "/config"
			
		if os.path.exists(kubeConfigPath):
			os.remove(kubeConfigPath)
			logging.info("Archivo crawler eliminado...")
				
		
		logging.info("Descargango archivo de configuración del cluster de Crawler")
		
		# Get data of an object.
		response = client.get_object(configs.get("aws.s3.bucket-name").data, keyCrawler)
		# Read data from response.
		binary_file = open(kubeConfigPath, "wb")
		binary_file.write(response.data)
		binary_file.close()	
		logging.info("Archivo descargado correctamente a: " + kubeConfigPath)
		response.close()
		response.release_conn()	
		
	except OSError as err:
		logging.error(err)
		
	return kubeConfigPath