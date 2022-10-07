# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
from wsgiref import simple_server
import os
import sqlite3

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user

            Item_MRP = float(request.form['Item_MRP'])
            Outlet_Type = float(request.form['Outlet_Type'])
            Item_Visibility = float(request.form['Item_Visibility'])
            Item_Weight = float(request.form['Item_Weight'])
            Item_Type = float(request.form['Item_Type'])
            Outlet_Establishment_Year= float(request.form['Outlet_Establishment_Year'])
            Outlet_Size	 = float(request.form['Outlet_Size'])
            Outlet_Location_Type = float(request.form['Outlet_Location_Type'])

            filename = 'Store price.pickle'
            loaded_model = pickle.load(open(filename, 'rb'))
            # loading the model file from the storage
            # predictions using the loaded model file

            prediction=loaded_model.predict([[Item_MRP,Outlet_Type,Item_Visibility,Item_Weight,Item_Type,
                                             Outlet_Establishment_Year,Outlet_Size,Outlet_Location_Type]])
            print('prediction PRICE is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction[0])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('index.html')



if __name__ == "__main__":
    port = str(os.getenv("PORT"))
    app.run(host='127.0.0.1', port=8000, debug=True)
    # app = app.run()
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port=port, app=app)
    httpd.serve_forever()