from flask import Flask,request,render_template,jsonify
from flask_restful import Resource,Api
from PIL import Image
import numpy as np 
import pickle

app = Flask(__name__)


flower_model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def method_name():
    return render_template('flower.html')
@app.route('/flower')
def flower():
    return render_template('flower.html')

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 4)
    result = flower_model.predict(to_predict)
    return result

# @app.route('/resultApi', methods=['POST'])
# def Api():
#     if request.method == 'POST':
#         to_predict_list = request.form.to_dict()
#         to_predict_list = list(to_predict_list.values())
#         to_predict_list = list(map(int, to_predict_list))
#         result = ValuePredictor(to_predict_list)
            
#         return jsonify({'prediction':prediction})
# app.route('/recommend',methods='POST') 
# def recommend():
#     if request.method=='POST':
#         a=request.form.get('Pregnancies')
#         b=request.form.get('Glucose')
#         c=request.form.get(BloodPressure)
#         d=request.form.get('SkinThickness') 
#         data=[a,b,c,d]
#         ress=np.array(data)
#         print(ress)
#         res=np.array(data) 
#         res=flower_model.predict(res)  
@app.route('/add', methods = ['POST'])
def recommend():
    a=request.json['Pregnancies']
    b=request.json['Glucose']
    c=request.json['BloodPressure']
    d=request.json['SkinThickness']
    add=a+b+c+d
    return jsonify({'add':add})

@app.route('/predict', methods = ['POST'])
def results():
    if request.method == 'POST':
            a=request.json['Pregnancies']
            b=request.json['Glucose']
            c=request.json['BloodPressure']
            d=request.json['SkinThickness']
            
            test_data=[a,b,c,d]
            test_data=np.array(test_data)
            test_data=test_data.reshape(1,-1)
            predict=flower_model.predict(test_data)
            predicted_value=predict.tolist()[0]
            print(predicted_value)
            if int(predicted_value==1):
                res='it is 1'
            elif int(predicted_value==2):
                res='it is 2'
            elif int(predicted_value==3):
                res='it is 3'
            else:
                res='it is 4'
            return jsonify({'predict':res})
            
@app.route('/crops',methods=['POST'])
def crops():
    if request.method=='POST':     
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)

        if int(result)== 1:
            prediction ='The person is 1'
        elif int(result)==2:
            prediction ='The person is 2'
        elif int(result)==3:
            prediction ='The person is 3'
        else:
            prediction ='The person is 4'
        
        return jsonify({'flaskResult':prediction})
        # else:
        #     prediction ='The person is 4'	
        # return render_template("flower.html",prediction =prediction)
   
    
 
    

if __name__ == '__main__':

    app.run()
