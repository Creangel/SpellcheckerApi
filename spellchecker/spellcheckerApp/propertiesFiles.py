import os, sys, re
from jproperties import Properties
import simplejson, json, math

initialPath = ""
try:
    __file__
    initialPath = os.path.dirname(os.path.abspath(__file__+"/../"))
except NameError:
    initialPath = os.path.abspath('')
    
sys.path.append(initialPath)

def loadPropertiesAWS():
	configs = Properties()
	with open(initialPath+'/aw_s3.properties', 'rb') as config_file:
		configs.load(config_file)
	
	return configs
	
def saveSettings(configmapSettings):
	configs = Properties()
	for key, value in configmapSettings.items():
		jsonProps = json.loads(value)
		if(key == "collection.properties"):
			configs["collection.service.url"] = jsonProps["collection.service.url"]
		elif(key == "monitor.properties"):
			configs["monitor.service.url"] = jsonProps["monitor.service.url"]
		elif(key == "mysql.properties"):
			configs["mysql.driver-class-name"] = jsonProps["mysql.driver-class-name"]
			
			if(jsonProps["mysql.url"]):
				configs["mysql.url"] = jsonProps["mysql.url"]
				urlSplit = jsonProps["mysql.url"].split("/")
				configs["mysql.database"] = urlSplit[-1]
				configs["mysql.host"] = urlSplit[2].split(":")[0]
				configs["mysql.port"] = urlSplit[2].split(":")[1]
				
			configs["mysql.username"] = jsonProps["mysql.username"]
			configs["mysql.password"] = jsonProps["mysql.password"]
		elif(key == "rabbitmq.properties"):
			configs["rabbitmq.host"] = jsonProps["rabbitmq.host"]
			configs["rabbitmq.port"] = jsonProps["rabbitmq.port"]
			configs["rabbitmq.username"] = jsonProps["rabbitmq.username"]
			configs["rabbitmq.password"] = jsonProps["rabbitmq.password"]
			configs["rabbitmq-exchange.name"] = jsonProps["rabbitmq-exchange.name"]
			configs["rabbitmq-reply-queue.name"] = jsonProps["rabbitmq-reply-queue.name"]
			configs["rabbitmq-send-queue.name"] = jsonProps["rabbitmq-send-queue.name"]
			configs["rabbitmq-reply-queue.routing-key"] = jsonProps["rabbitmq-reply-queue.routing-key"]
			configs["rabbitmq-send-queue.routing-key"] = jsonProps["rabbitmq-send-queue.routing-key"]
		elif(key == "solr.properties"):
			configs["solr.cluster.username"] = jsonProps["solr.cluster.username"]
			configs["solr.cluster.password"] = jsonProps["solr.cluster.password"]
		elif(key == "tasker.properties"):
			configs["tasker.service.url"] = jsonProps["tasker.service.url"]
			
	pathSettings = initialPath+"/configmapSettings.properties"
	if os.path.exists(pathSettings):
		os.remove(pathSettings)
			
	with open(pathSettings, "wb") as f:
		configs.store(f, encoding="utf-8")
		
def loadSettings():
	configs = Properties()
	with open(initialPath+'/configmapSettings.properties', 'rb') as config_file:
		configs.load(config_file)
	
	return configs