import json
import requests
import psycopg2
import urllib.parse as urlparse
import os


class Region(object):
    """docstring for UserFunctions"""
    def __init__(self):
        super(Region, self).__init__()

    def getTouristSiteWeather(self,city):
        try:
            if city!="":
                url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric"+ "&APPID=e2cd7d4ec205a87e9fedc5b591cedd72"
                result = requests.get(url)
                result = json.loads(result.text)
                weather_data = {
                    'temp': result['main']['temp'],
                    'humidity': result['main']['humidity']
                }
                return weather_data
            else:
                out = { 'code': '01', 'msg': 'City name is empty', 'data': [] }
        except Exception as e:
            out = {"err": str(e)}
        
    

    def getTouriteSiteByRegion(self,data):
        conn = ""
        out = []
        
        try:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except Exception as e:
            out = {"err": str(e)}
        try:
            cur = conn.cursor()
            cur.execute("""SELECT * from tourist_site where region_shortname = '{0}'""".format(data['region_shortname']))
            rows = cur.fetchall()
         
            data = []
            for row in rows:
                data.append({ "id": row[0], "tourist_site_name": row[1], "tourist_site_image": row[2], "tourist_alt_name": row[3], "region_shortname": row[4], "tourist_site_description": row[5],"tourist_site_area_name": row[6] })
          
            if data == []:
                out = {'code': '01', 'msg': 'Failed to retrieve data', 'data': [] }
            else:
                out = { 'code': '00', 'msg': 'Data Retrieved Successfully', 'data': data }
        except Exception as e:
            out = {"err": str(e)}
        return json.dumps(out)

    def getTouriteSiteById(self,data):
        conn = ""
        out = []
        
        try:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except Exception as e:
            out = {"err1": str(e)}
        try:
            print("Printing incomg request in getTouriteSiteById")
            print(data)
            cur = conn.cursor()
            cur.execute("""SELECT * from tourist_site where id = '{0}'""".format(data['id']))
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0], 
                    "tourist_site_name": row[1],
                    "tourist_site_image": row[2], 
                    "tourist_alt_name": row[3],
                    "region_shortname": row[4], 
                    "tourist_site_description": row[5],
                    "tourist_site_area_name": row[6] })
            
            if data != []:
                #weather_data = self.getTouristSiteWeather(data['tourist_site_area_name'])
                print("Printing weather_data in site id")
                print("weather_data")
                out = {
                    'code':'00',
                    'msg':'Data Retrieved Successfully',
                    'data':data }
            else:
                out = {
                    'code':'01',
                    'msg':'Failed to retrieve data',
                    'data':[] }
        except Exception as e:
            out = {"err2": str(e)}
        return json.dumps(out)
