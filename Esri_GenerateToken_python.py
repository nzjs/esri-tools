import urllib
import requests
import json
import sys

url = 'https://www.arcgis.com/sharing/rest/generateToken?f=pjson' # Set destination URL here
payload = { 'username': 'ARCGIS ONLINE USERNAME',
            'password': 'ARCGIS ONLINE PASSWORD',
            'referer': 'https://www.arcgis.com'
          }     # Set POST fields here 
                # Eg. &username=user&password=password&referer=https://www.arcgis.com

response = requests.post(url, data=payload)

#print(response.text) #TEXT/HTML
#print(response.status_code, response.reason) #HTTP
r = response.json()
token = r['token']