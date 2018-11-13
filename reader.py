from keras.models import model_from_json
# Testing
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
model.compile(loss='mean_squared_logarithmic_error', optimizer=sgd, metrics=['mae'])
score = model.evaluate(X_test, Y_test, batch_size=25)
print(score)

# ---- INPUTS --------
# Given hour, nitrogen dioxide,
hour = 1
nitrogenD = 14
carbonM = 12
pm10M =  106
zone = 1 # noroeste: 1, noreste:2, centro: 3, suroeste:4, sureste:5
month = 0 # from 0 to 11

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


Xnew = np.array([[hour, nitrogenD, carbonM, pm10M, zone, month]])
# make a prediction
ynew = model.predict(Xnew)
# Denormalization
ynew = ynew * (np.max(Y_train) - np.min(Y_train)) + np.min(Y_train)
# show the inputs and predicted outputs
print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
