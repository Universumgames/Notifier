import tempfile
import platform
import base64
import requests
import json
import os
import time
from plyer import notification

def notificationClick():
  print("hi")

def base64Encode(content):
  return base64.b64encode(content.encode('utf-8')).decode('utf-8')

def base64Decode(content):
  return base64.b64decode(content).decode("utf-8")

#notify.init('E:/tommy/Programming/Python/Notifier/python/icon.ico', notificationClick)
with tempfile.TemporaryDirectory() as directory:
  while True:
    pcName = platform.node()
    encodedName = base64Encode(pcName)
    r = requests.get("http://localhost/?pcname=" + encodedName)
    #text = r.text.replace("<html>", "").replace("</html>", "").replace("<head>", "").replace("</head>", "").replace("<body>", "").replace("</body>", "")
    notifications = r.json()

    for notifi in notifications:
      recieverUUID = base64Decode(notifi["recieverUUID"])
      iconPath = base64Decode(notifi["iconPath"])
      title = base64Decode(notifi["title"])
      content = base64Decode(notifi["content"])
      id = base64Decode(notifi["id"])
      sender = base64Decode(notifi["sender"])

      filename = "picture.ico"
      filepath = directory + "/" + filename
      writeData = ""
      if iconPath[:4] == "http":
        writeData = requests.get(iconPath).content
      else:
        lastIndex = str(iconPath).rindex(",")
        writeData = base64Decode(iconPath[lastIndex:])
      open(filepath, 'wb').write(writeData)
      notification.notify(
        title=title,
        message=content,
        app_icon=filepath,  # e.g. 'C:\\icon_32x32.ico'
        timeout=10,  # seconds
      )
      #notify.notify(content, title, filepath, True, 2, notify.dwInfoFlags.NIIF_USER | notify.dwInfoFlags.NIIF_LARGE_ICON)
      #toaster.show_toast(title, content, icon_path=filepath, duration=None)
  time.sleep(5)
  #notify.uninit()