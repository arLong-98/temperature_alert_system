import requests,json,time
from boltiot import Bolt
import config

mybolt = Bolt(config.bolt_api_key,config.device_id)

def get_sensor_value_from_pin(pin):
	try:
		response = mybolt.analogRead(pin)
		data= json.loads(response)
		if data["success"]!=1:
			print("Request not successful")
			print("This is the response ->",data)
			return -999
		sensor_value = int(data['value'])
		return sensor_value
	except Exception as e:
		print("Something went wrong when returning sensor value")
		print(e)
		return -999

def send_telegram_messages(message):
	url = "https://api.telegram.org/"+config.telegram_bot_id+"/sendMessage"
	data1 = {
		"chat_id":config.telegram_chat_id,
		"text": message
		}
	
	try:
		response = requests.post(url,data=data1)
		print("This is the telegram response")
		print(response.text)
		telegram_data = json.loads(response.text)
		return telegram_data["ok"]
	except Exception as e:
		print("An erroe occured in sending alert via telegram")
		print(e)
		return False

while True:
	sensor_value = get_sensor_value_from_pin("A0")
	temp = sensor_value/10.24
	print("Current sensor reading: "+str(sensor_value) +"and temperature: "+str(temp))
	
	if sensor_value == -999:
		print("Request was unsuccessful. Skipping")
		time.sleep(10)
		continue
	if sensor_value>=config.threshold :
		print("Sensor value has exceeded threshold")
		message = "Alert! Sensor value has exceeded " +str(config.threshold)+ ".The Current value is "+ str(sensor_value)
		telegram_status = send_telegram_messages(message)
		print("This is the telegram status: ", telegram_status)
	time.sleep(10)
