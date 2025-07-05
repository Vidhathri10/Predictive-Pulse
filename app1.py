import numpy as np
import pickle
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__,static_url_path='/Flask/static')
# model = pickle.load(open('model.pkl','rb'))
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')# route to display the home page
def home():
    return render_template('index.html')
@app.route('/details')
def details():
    return render_template('details.html')
@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/predict', methods=['POST'])
def predict():
    Gender = float(request.form["Gender"]or 0) 
    Age = float(request.form["Age"] or 0)
    History = float(request.form['History']or 0)
    Patient = float(request.form["Patient"] or 0)
    TakeMedication = float(request.form['TakeMedication']or 0)
    Severity = float(request.form["Severity"] or 0)
    BreathShortness = float(request.form["BreathShortness"] or 0)
    VisualChange = float(request.form["VisualChanges"] or 0)
    NoseBleeding = float(request.form["NoseBleeding"] or 0)
    Whendiagnoused = float(request.form["Whendiagnoused"] or 0)
    Systolic = float(request.form["Systolic"] or 0)
    Diastolic = float(request.form["Diastolic"] or 0)
    ControlledDiet = float(request.form["ControlledDiet"] or 0)
    
    

    features_values = np.array([Gender, Age, History, Patient, TakeMedication, Severity, BreathShortness, VisualChange, NoseBleeding, Whendiagnoused, Systolic, Diastolic, ControlledDiet])

    df = pd.DataFrame(features_values.reshape(1, -1), columns=['Gender', 'Age','History', 'Patient','TakeMedication', 'Severity', 
                                                               'BreathShortness', 'VisualChanges',
                                                               'NoseBleeding', 'Whendiagnoused', 'Systolic', 'Diastolic', 'ControlledDiet',
                                                               ])

    print(df)

    prediction = model.predict(df)
    print(prediction[0])
    if prediction[0] == 0:
        result = "NORMAL"
    elif prediction[0] == 1:
        result = "HYPERTENSION (Stage-1)"
    elif prediction[0] == 2:
        result = "HYPERTENSION (Stage-2)"
    else:
        result = "HYPERTENSIVE CRISIS"
    print(result)
    text = "Your Blood Pressure stage is: "
    return render_template('predict.html', prediction_text= text + result)

if __name__ == "__main__":
    app.run(debug=False, port=5000)