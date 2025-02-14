import os, sys, logging, logging.handlers
from datetime import datetime
from logging import handlers, Formatter
from logging.handlers import RotatingFileHandler
from .aws_s3 import downloadConfigCrawler
from kubernetes import client, config
from kubernetes.client import ApiException

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


def getConfigMapSettings(proxy):
	try:
		kubeConfigPath = downloadConfigCrawler(proxy)
		
		# Configs can be set in Configuration class directly or using helper utility
		config.load_kube_config(kubeConfigPath)
		v1 = client.CoreV1Api()
		
		namespace = "ifindit-settings"
		config_map_name = "ifindit-settings"
		
		# Obtener el ConfigMap
		configmap = v1.read_namespaced_config_map(config_map_name, namespace)
		
		return configmap.data
	except ApiException as e:
		logging.error("Excepción al obtener el ConfigMap: %s\n" % e)
	