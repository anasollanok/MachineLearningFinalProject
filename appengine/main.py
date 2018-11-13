# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
from json import dumps

from keras.models import model_from_json
from keras.optimizers import SGD
import numpy as np
import tensorflow as tf
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]

# [Start app variables]

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
sgd = SGD(lr=0.05, decay=1e-6, momentum=0.5, nesterov=True) # optimizer
loaded_model.compile(loss='mean_squared_logarithmic_error', optimizer=sgd, metrics=['mae'])
loaded_model._make_predict_function()
graph = tf.get_default_graph()

# [End app variables]

def predecirAire(hour, nitrogenD, carbonM, pm10M, zone, month):

    #score = loaded_model.evaluate(X_test, Y_test, batch_size=25)
    #print(score)

    # ---- INPUTS --------
    # Given hour, nitrogen dioxide,
    #hour = 1
    #nitrogenD = 14
    #carbonM = 12
    #pm10M =  106
    #zone = 1 # noroeste: 1, noreste:2, centro: 3, suroeste:4, sureste:5
    #month = 0 # from 0 to 11

    # Categorizing
    if nitrogenD <= 10:
        nitrogenD = 0
    elif nitrogenD <= 15:
        nitrogenD = 1
    elif nitrogenD <= 20:
        nitrogenD = 2
    else:
        nitrogenD = 3

    if carbonM <= 5:
        carbonM = 0
    elif carbonM <= 6:
        carbonM = 1
    elif carbonM <= 8:
        carbonM = 2
    else:
        carbonM = 3

    if pm10M <= 44:
        pm10M = 0
    elif pm10M <= 64:
        pm10M = 1
    elif pm10M <= 94:
        pm10M = 2
    else:
        pm10M = 3

    global graph
    with graph.as_default():
        Xnew = np.array([[hour, nitrogenD, carbonM, pm10M, zone, month]])
        # make a prediction
        ynew = loaded_model.predict(Xnew)
    # Denormalization
    #ynew = ynew * (np.max(Y_train) - np.min(Y_train)) + np.min(Y_train)
    # show the inputs and predicted outputs
    #return ("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
    return ynew[0][0]



# [START home]
@app.route('/')
def home():
    return render_template('home.html')
# [END home]

# [START leaving]
@app.route('/leaving')
def leavingform():
    return render_template('leavingform.html')
# [END leaving]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted():
    HOUR = request.form['HOUR']
    NITROGEND = request.form['NITROGEND']
    CARBONM = request.form['CARBONM']
    PM10M = request.form['PM10M']
    ZONE = request.form['ZONE']
    MONTH = request.form['MONTH']
    # Set up the timer and use this variables.
    prediccion = predecirAire(HOUR, NITROGEND, CARBONM, PM10M, ZONE, MONTH)
    # [END submittedleaving]
    # [START render_template]
    return render_template('submitted_form.html', result=prediccion, hour=HOUR, nitro=NITROGEND, carbon=CARBONM, pm10M=PM10M, zone=ZONE, month=MONTH)
    # [END render_template]

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
