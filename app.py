from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
from collections import Counter

app=Flask(__name__)
app.config['SECRET_KEY'] = 'gaur123'

desc=pd.read_csv("Description.csv")
def desc_ription(pred):
    return desc[desc['Disease'] == pred]['Description'].values[0]


train=pd.read_csv("Training.csv")
index_value={}
temp=train.iloc[:,0:132]
for index,value in enumerate(temp.columns):# index=column number and value =column name
    value=' '.join([i for i in value.split('_')])
    value=value.strip()
    index_value[value]=index
#print(len(index_value))
prec=pd.read_csv("precaution.csv")

def pre_caution(pred):
    l=[]
    array=prec[prec['Disease']==pred].values[:,1:]
    for i in array:
        for j in i:
            l.append(j)
    return l
    

with open('model1.pkl','rb') as m1:
    model1 =pickle.load(m1)
    
with open('model2.pkl','rb') as m2:
    model2 =pickle.load(m2)

with open('model3.pkl','rb') as m3:
    model3 =pickle.load(m3)
    
with open('encoded.pkl','rb') as e:
    encoded=pickle.load(e)

def prediction(arr):
    input_data=[0]*len(index_value)# input data has 132 zeroes
    for i in arr:
        if i in index_value.keys():
            num=index_value[i]# yaha pr disease ki respective encoded value ayegi
            input_data[num]=1 # disease k respective column me one ho jayega
        
    input_data=np.array(input_data).reshape(1,-1)
    predict1=model1.predict(input_data)#as predict is array of size one
    predict2=model2.predict(input_data)
    predict3=model3.predict(input_data)
    predict_array=tuple([predict1[0],predict2[0],predict3[0]])
    final_predict=Counter(predict_array).most_common(1)[0][0]
    print(final_predict)
    type(final_predict)
    return encoded[final_predict]
    
    
@app.route('/')
def main():
    return render_template("main.html")

@app.route("/main.html")#yaha pr keval "/main" ye bhi ho skta h
def home():
    return render_template("main.html")

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/doctors.html')
def doctor():
    return render_template("doctors.html")

@app.route('/login.html')
def login():
    return render_template("login.html")

@app.route('/services.html')
def services():
    return render_template("services.html")

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html') 

@app.route('/output.html',methods=['POST','GET'])
def predicted_value():
    symptom1 :str=request.form.get('symptom1','')
    symptom2 :str=request.form.get('symptom2','')
    symptom3 :str=request.form.get('symptom3','')
    symptom4 :str=request.form.get('symptom4','')
    symptom5 :str=request.form.get('symptom5','')
    arr=np.array([symptom1,symptom2,symptom3,symptom4,symptom5])
    pred=prediction(arr)
    print(pred)
    #session['pred'] =pred
    details=desc_ription(pred)
    takecareof=pre_caution(pred)
    return render_template('output.html',result=pred,otp=details,precaution_list=takecareof) 

@app.route('/contacts.html')
def contact():
    return render_template("contacts.html")
@app.route('/dashboard.html')
def dashboard():
    return render_template("dashboard.html")

@app.route('/learn.html')
def learn():
    return render_template("learn.html")
@app.route('/appointment.html')
def appointment():
    return render_template("appointment.html")

if __name__=='__main__':
    app.run(debug=True)