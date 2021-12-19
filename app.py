import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/")
@app.route("/home")

def home():
  return render_template("index.html")

@app.route("/result", methods = ["POST", "GET"])
def result():
  def get_result(age, sex, bmi, children, smoker, region):
    url = "http://79d543a0-1516-4358-914f-ea59e4b91924.centralindia.azurecontainer.io/score"

    def createJSON(age, sex, bmi, children, smoker, region):
      data = {
            "age": str(age),
            "sex": str(sex),
            "bmi": str(bmi),
            "children": str(children),
            "smoker": str(smoker),
            "region": str(region)
          }
      return data

    data = createJSON(age, sex, bmi, children, smoker, region)

    payload = json.dumps({
      "Inputs": {
        "WebServiceInput0": [
            data
        ]
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer 6C671DOwQMpQsptgj2Myr5aW1pyFV3aO'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    return(round(json_data['Results']['WebServiceOutput0'][0]['Scored Labels'],2))

  age = request.form["enter_age"]
  sex = request.form["enter_sex"]
  bmi = request.form["enter_bmi"]
  children = request.form["enter_children"]
  smoker = request.form["enter_smoker"]
  region = request.form["enter_region"]

  cost = get_result(age, sex, bmi, children, smoker, region)
  return render_template("index.html", cost = str(cost))

if __name__ == '__main__':
  app.run(debug=True)