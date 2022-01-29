#importing dependencies
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/")
@app.route("/home")

def home():
  return render_template("index.html")

@app.route("/result", methods = ["POST", "GET"])
def result():
    def get_result(age, sex, bmi, children, smoker, region):
        # data collection
        dataset = pd.read_csv('dataset/insurance.csv')

        # DATA PRE-PROCESSING
        # encoding categorical featres: 'sex', 'smoker', 'region'
        dataset.replace({'sex':{'male':0, 'female':1}}, inplace = True)
        dataset.replace({'smoker':{'yes':0, 'no':1}}, inplace = True)
        dataset.replace({'region':{'southeast':0, 'southwest':1, 'northeast':2, 'northwest':3}}, inplace = True)

        # splitting the Features and Target
        X = dataset.drop(columns = 'charges', axis = 1)
        Y = dataset['charges']

        # splitting the data into Training data & Testing data
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)

        # Model training: Linear Regression
        regressor = LinearRegression()
        regressor.fit(X_train.values, Y_train.values)

        # Building a predictive system
        input_data = (age, sex, bmi, children, smoker, region)

        # changing input data to a numpy array
        numpy_array = np.asarray(input_data)

        # reshaping the array
        input_data_reshaped = numpy_array.reshape(1, -1)
        prediction = regressor.predict(input_data_reshaped)
        return(round(prediction[0], 2))

    age = int(request.form["age"])
    sex = request.form["gender"]  
    if sex == "female":
        sex = 1
    else:
        sex = 0
    bmi = float(request.form["bmi"])
    children = int(request.form["children"])
    smoker = request.form["smoker"] 
    if smoker == "yes":
        smoker = 0
    else:
        smoker = 1 
    region = request.form["region"]
    if region == "southeast":
        region = 0
    elif region == "southwest":
        region = 1
    elif region == "northeast":
        region = 2
    else:
        region = 3

    cost = get_result(age, sex, bmi, children, smoker, region)
    return render_template("index.html", cost = str(cost))

if __name__ == '__main__':
    app.run(debug = True)
