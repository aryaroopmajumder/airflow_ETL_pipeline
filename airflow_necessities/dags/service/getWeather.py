"""getWeather.py: getWeather python file"""

__author__ = "Aryaroop Majumder"




import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
def get_weather():
	"""
	Query openweathermap.com's API and to get the weather for
	Brooklyn, NY and then dump the json to the /src/data/ directory
	with the file name "<today's date>.json"
	"""
	try:
		api_key = os.getenv('API_KEY')

		parameter = {'q': 'Bengaluru, India', 'appid': api_key}

		result = requests.get("http://api.openweathermap.org/data/2.5/weather?", parameter)

		print(result)
		print(result.json())


		if result.status_code == 200 :

			# Get the json data
			json_data = result.json()
			file_name = str(datetime.now().date()) + '.json'
			tot_name = os.path.join(os.path.dirname(__file__), 'data', file_name)
			print(tot_name)


			with open(tot_name, 'w') as outputfile:
				json.dump(json_data, outputfile)
	except Exception as ex:
		print(f"Error In API call. {ex.args}")

