from win10toast import ToastNotifier
import tempfile
import platform
import base64
import requests
import json
import os

with tempfile.TemporaryDirectory() as directory:
  pcName = platform.node()
  encodedName = base64.b64encode(pcName.encode('utf-8')).decode('utf-8')
  r = requests.get("http://localhost/?pcname=" + encodedName)
  #text = r.text.replace("<html>", "").replace("</html>", "").replace("<head>", "").replace("</head>", "").replace("<body>", "").replace("</body>", "")
  notifications = r.json()
  toaster = ToastNotifier()

  for notifi in notifications:
    recieverUUID = notifi["recieverUUID"]
    iconPath = notifi["iconPath"]
    title = notifi["title"]
    content = notifi["content"]
    id = notifi["id"]
    sender = notifi["sender"]

    filename = "picture.ico"
    filepath = directory + "/" + filename
    open(filepath, 'wb').write(base64.b64decode(iconPath[iconPath.rindex(","):]))
    try:
      toaster.show_toast(title, content, icon_path=filepath, duration=None)
      break
    except TypeError:
      pass