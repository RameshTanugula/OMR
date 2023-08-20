#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import cv2
import numpy as np
import pandas as pd
from uuid import uuid4
from utils1 import find_paper,id_read,read_answer
import matplotlib.pyplot as plt
from skimage import io
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '1'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

@app.route('/submit', methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def submit_omr():
    data = request.form
    print(data)
    file = request.files['file']
    key = data['key']
    test_id1 = data['testId']
    roll_no = data['rollNo']
    image = io.imread(file)
    d=find_paper(image)
    def answers():
        q1=d[440:1245,55:185]
        q2=d[440:1240,255:390]
        q3=d[440:1240,455:590]
        q4=d[438:1240,655:790]
        q5=d[435:1240,855:990]

        s1=read_answer(q1) 
        s2=read_answer(q2)
        s3=read_answer(q3) 
        s4=read_answer(q4) 
        s5=read_answer(q5)
        final=s1+s2+s3+s4+s5
        return final
    def s_id_reader():
        std_1=d[75:350,12:34]
        std_2=d[75:350,36:58]
        std_3=d[75:350,62:84]
        std_4=d[75:350,88:110]
        std_5=d[75:350,112:134]
        std_6=d[75:350,136:158]
        std_7=d[75:350,160:182]
        std_8=d[75:350,186:208]
        std_9=d[75:350,210:232]
        std_10=d[75:350,234:256]
        st_1=id_read(std_1) 
        st_2=id_read(std_2)
        st_3=id_read(std_3)
        st_4=id_read(std_4)
        st_5=id_read(std_5)
        st_6=id_read(std_6)
        st_7=id_read(std_7)
        st_8=id_read(std_8)
        st_9=id_read(std_9)
        st_10=id_read(std_10)
        student_Id=st_1+st_2+st_3+st_4+st_5+st_6+st_7+st_8+st_9+st_10
        return student_Id
    def t_id_reader():
        t_id_1=d[75:350,282:304]
        t_id_2=d[75:350,312:334]
        t_id_3=d[75:350,342:364]
        t_1=id_read(t_id_1) 
        t_2=id_read(t_id_2)
        t_3=id_read(t_id_3)
        t_Id=t_1+t_2+t_3
        return t_Id 
    bubbled = None
    student_id = None
    test_id = None

    try:
        bubbled = answers()
    except ValueError:
        print("Bubbled answers are not found")

    try:
        student_id = s_id_reader()
    except ValueError:
        print("student_id is not found")

    try:
        test_id = t_id_reader()
    except ValueError:
        print("test_id is not found")
    
    marks = 0
    for i in range(len(key)):
        if key[i] == 0:
            marks += 1
        elif key[i] == bubbled[i]:
            marks += 1
    total=marks
    none_count = len([x for x in bubbled if x is None])
    worng=50-total-none_count
    student_id = ''.join(map(str, student_id))
    test_id = ''.join(map(str, test_id))
    k=(student_id==roll_no)
    h=(test_id==test_id1)
    return {"Rollno_matched":k,"TestId_matched":h,"Answered":bubbled,"Key":key,"Total_marks":total,"Total_worng":worng,"Count_None_values":none_count}
#     return jsonify({"message":"successful"})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
   app.run(debug = True)
