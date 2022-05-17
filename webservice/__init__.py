# Imports REST
#from flask import Flask
#from flask_restful import Resource, Api
import json
import re
import collections
import datetime
from flask import Flask, request, jsonify, render_template, make_response
from flask_restful import Resource, Api


# Import passwd hash
import bcrypt
import base64

import psycopg2
from config import config

# Webservice
app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(e):
  return "NO HAY NADA AQUI!"

err_response = {
        "status":"false"
        }

class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

class Validate(Resource):
    def get(self):
        # AGSCh DB Connect
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)

        group = request.args.get('group')
        if not group:
            return err_response
        else:
            if(request.args.get('year')):
                year = request.args.get('year')
                cursor.execute("""
                    select inicio, termino
                    from registration_types,
                    (
                    	select registration_type_id, min(date_from) as inicio, max(date_to) as termino
                    	from periods_containers
                    	group by registration_type_id
                    	order by registration_type_id
                    ) as date_data
                    where date_data.registration_type_id = registration_types.id
                    and year = '%s'
                """ % (year))
                dates = cursor.fetchall()
            else:
                #year = '2020'
                now = datetime.datetime.now()
                if (now.month > 5):
                    year = now.year
                else:
                    year = now.year - 1
                cursor.execute("""
                    select inicio, termino
                    from registration_types,
                    (
                    	select registration_type_id, min(date_from) as inicio, max(date_to) as termino
                    	from periods_containers
                    	group by registration_type_id
                    	order by registration_type_id
                    ) as date_data
                    where date_data.registration_type_id = registration_types.id
                    and year = '%s'
                """ % (year))
                dates = cursor.fetchall()
            #print(str(group))
            cursor.execute("""
                select count(user_id) from credentials where registration_id in (
            	select id from registrations where group_id = (
            		select id from groups where code = '%s')
            	and date_done between '%s' and '%s' order by date_done)
                """ % (group, dates[0][0], dates[0][1]))
            result = cursor.fetchall()
            #print(result[0][0])
            if result[0][0] > 0:
                response = {
                        "registro":result[0][0],
                        "año":str(year)
                        }
                return response
            else:
                response = {
                        "registro":0,
                        "año":str(year)
                        }
                return response
            if(connection):
                cursor.close()
                connection.close()


api.add_resource(Home, '/') #Home
api.add_resource(Validate, '/validador') #Login users

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')
