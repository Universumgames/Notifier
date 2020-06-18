import sys
import requests
import base64

def base64Encode(content):
  return base64.b64encode(content.encode('utf-8')).decode('utf-8')

def base64Decode(content):
  return base64.b64decode(content).decode("utf-8")

url = "http://localhost/"

title = ""
content = ""
iconPath = ""
recieverUUID = ""
sender = ""

if(len(sys.argv) == 5):
  title = sys.argv[0]
  content = sys.argv[1]
  iconPath = sys.argv[2]
  recieverUUID = sys.argv[3]
  sender = sys.argv[4]
else:
  title = "Test title"
  content = "test content"
  iconPath = "https://www.microsoft.com/favicon.ico?v2"
  recieverUUID = "quadro"
  sender = "script"


payload = {'title': title,
'content': content,
'iconPath': iconPath,
'recieverUUID': recieverUUID,
'sender': sender}
files = [

]
headers= {}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text)


