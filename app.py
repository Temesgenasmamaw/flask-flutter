from flask import Flask,request,render_template,jsonify,Markup
import numpy as np 
import pandas as pd
import pickle
from Utils.fertilizer import fertilizer_dic
app = Flask(__name__)


model = pickle.load(open('myModel.pkl', 'rb'))

@app.route('/predict', methods = ['POST'])
def results():
    if request.method == 'POST':
            a=request.json['ph']
            b=request.json['rain fall']
            c=request.json['temprature']
            d=request.json['altitude']
            
            test_data=[a,b,c,d]
            test_data=np.array(test_data)
            test_data=test_data.reshape(1,-1)
            predict=model.predict(test_data)
            predicted_value=predict.tolist()[0]
            print(predicted_value)
            print(predict)
            print(type(predict))
        
            return jsonify({'predict':predicted_value})
@app.route('/fertilizer', methods=['POST'])
def fert_recommend():  
    if request.method == 'POST':   

        crop_name = str(request.json['cropname'])
        N = int(request.json['nitrogen'])
        P = int(request.json['phosphorus'])
        K = int(request.json['potassium'])
        # ph = float(request.form['ph'])

        df = pd.read_csv('fertilizer.csv')

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"

        fertilizer_result =fertilizer_dic[key]
        return jsonify({'fertilizer':fertilizer_result})

    

if __name__ == '__main__':

    app.run()
