# clipper_start
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

clipper_conn.start_clipper()
clipper_conn.connect()

clipper_conn.register_application(
	name="digit", 
	input_type="doubles", 
	default_output="-1.0", 
	slo_micros=10000000) # 10,000,000 micros == 10 sec

clipper_conn.get_all_apps()

#################################################
######### Define Own Prediction Function ########
#################################################

import sklearn
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

model_path = "../../models/sklearn/" 
model_name = "dig_nn_model.sav"
clf = joblib.load(model_path + model_name)

def clf_predict(xs):
	return clf.predict(xs)

#################################################
#################################################
#################################################

from clipper_admin.deployers import python as python_deployer

python_deployer.deploy_python_closure(
	clipper_conn, 
	name="digit-nn-model", 
	version=1, 
	input_type="doubles", 
	func=clf_predict)

clipper_conn.link_model_to_app(app_name="digit", model_name="digit-nn-model")

# clipper_conn.stop_all()