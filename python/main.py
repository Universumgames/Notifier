import tempfile
import platform
import base64
import requests
import json
import os
import time
#from plyer import notification
#import notify
from win10toast_persist import ToastNotifier
import shutil
import wget

def notificationClick():
  print("hi")

def base64Encode(content):
  return base64.b64encode(content.encode('utf-8')).decode('utf-8')

def base64Decode(content):
  return base64.b64decode(content).decode("utf-8")

#notify.init('E:/tommy/Programming/Python/Notifier/python/icon.ico', notificationClick)
toaster = ToastNotifier()
while True:
#if True:
  with tempfile.TemporaryDirectory() as directory:
    pcName = platform.node()
    encodedName = base64Encode(pcName)
    r = requests.get("http://localhost/?pcname=" + encodedName)
    #text = r.text.replace("<html>", "").replace("</html>", "").replace("<head>", "").replace("</head>", "").replace("<body>", "").replace("</body>", "")
    notifications = r.json()

    for notifi in notifications:
      #decode json data
      recieverUUID = base64Decode(notifi["recieverUUID"])
      iconPath = base64Decode(notifi["iconPath"])
      title = base64Decode(notifi["title"])
      content = base64Decode(notifi["content"])
      id = base64Decode(notifi["id"])
      sender = base64Decode(notifi["sender"])

      #download and save picture
      filename = "picture.ico"
      filepath = directory + "\\" + filename
      writeData = ""
      if iconPath[:4] == "http":
        wget.download(iconPath, filepath)
      else:
        lastIndex = iconPath.rindex(",")
        writeData = base64.b64decode(iconPath[lastIndex+1:].encode("utf-8"))
        open(filepath, 'wb').write(writeData)
      #display notification
      #notification.notify(
      #  title=title,
      #  message=content,
      #  app_icon="E:\\tommy\\Programming\\Python\\Notifier\\python\\icon.ico",
      #  timeout=10,
      #)
      #notify.notify(content, title, filepath, True, 5, notify.dwInfoFlags.NIIF_USER | notify.dwInfoFlags.NIIF_LARGE_ICON)
      toaster.show_toast(title=title,
                   msg=content,
                   icon_path=filepath,
                   duration=None)
    time.sleep(5)
  print(".")
  #notify.uninit()