#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import json

model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    # Opening JSON file 
    with open('./Data/UI_Data.json') as json_file: 
        ui_data = json.load(json_file) 
    
    car_model_mapping = ui_data['CarModel']
    cust_count_mapping = ui_data['Cust']
    plant_count_mapping = ui_data['Plant']

    if request.method == 'POST':
        
       City = request.form['city']
       CModel = request.form['Car_Model']
       Sales_organization = request.form['sales_organization']
       Item_Category = request.form['item_category']
       Target_quantity_UoM = request.form['target_quantity_UoM']
       
       KMs_Reading = float(request.form['km_read'])
       Labour_Total = float(request.form['labour_value'])
       Parts_Total = float(request.form['parts_value'])
       Order_Item = int(request.form['order_item'])
       Order_Quantity = int(request.form['order_quantity'])

       # Sales Organization
       if Sales_organization == 'MFCB':
           Sales_organization_MFCB = 1
           Sales_organization_MFCC = 0
           Sales_organization_MFCD = 0
           Sales_organization_MFCS = 0           
       elif Sales_organization == 'MFCC':
           Sales_organization_MFCB = 0
           Sales_organization_MFCC = 1
           Sales_organization_MFCD = 0
           Sales_organization_MFCS = 0           
       elif Sales_organization == 'MFCD':
           Sales_organization_MFCB = 0
           Sales_organization_MFCC = 0
           Sales_organization_MFCD = 1
           Sales_organization_MFCS = 0           
       elif Sales_organization == 'MFCS':
           Sales_organization_MFCB = 0
           Sales_organization_MFCC = 0
           Sales_organization_MFCD = 0
           Sales_organization_MFCS = 1           
       else:
           Sales_organization_MFCB = 0
           Sales_organization_MFCC = 0
           Sales_organization_MFCD = 0
           Sales_organization_MFCS = 0
           
       # Item Category           
       if Item_Category == 'P002':
           Item_Category_P002 = 1
           Item_Category_P010 = 0
           Item_Category_P011 = 0         
       elif Item_Category == 'P010':
           Item_Category_P002 = 0
           Item_Category_P010 = 1
           Item_Category_P011 = 0         
       elif Item_Category == 'P011':
           Item_Category_P002 = 0
           Item_Category_P010 = 0
           Item_Category_P011 = 1        
       else:
           Item_Category_P002 = 0
           Item_Category_P010 = 0
           Item_Category_P011 = 0
           
       # Target Quantity UoM           
       if Target_quantity_UoM == 'L':
           Target_quantity_UoM_L = 1
           Target_quantity_UoM_MIN = 0          
       elif Target_quantity_UoM == 'MIN':
           Target_quantity_UoM_L = 0
           Target_quantity_UoM_MIN = 1         
       else:
           Target_quantity_UoM_L = 0
           Target_quantity_UoM_MIN = 0
       
       Cust_Count = cust_count_mapping.get(City)
       Plant_Count = plant_count_mapping.get(City)
       Car_Model_fcode = car_model_mapping.get(CModel)

       prediction = model.predict([[KMs_Reading, Labour_Total, Parts_Total, Order_Item, Order_Quantity, Cust_Count, Plant_Count, Sales_organization_MFCB, Sales_organization_MFCC, Sales_organization_MFCD, Sales_organization_MFCS, Item_Category_P002, Item_Category_P010, Item_Category_P011, Target_quantity_UoM_L, Target_quantity_UoM_MIN, Car_Model_fcode]])
       
       total_value = abs(round(prediction[0][0],2))
       service_time = abs(round(prediction[0][1],2))
              
    return render_template('index.html', prediction_text='Service will take '+str(service_time)+' hours to complete and it will cost around '+str(total_value)+' Rupees.')

if __name__=="__main__":
    app.run(debug=True)
    