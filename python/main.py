import tempfile
import platform
import base64
import requests
import json
import os
import time
from plyer import notification
import notify
from win10toast_persist import ToastNotifier
import shutil
import wget

websiteAddress = "localhost"
waitDelayInSec = 5


def notificationClick():
    print("hi")


def base64Encode(toEncode):
    return base64.b64encode(toEncode.encode('utf-8')).decode('utf-8')


def base64Decode(toDecode):
    return base64.b64decode(toDecode.encode("utf-8")).decode("utf-8")


# notify.init('E:/tommy/Programming/Python/Notifier/python/icon.ico', notificationClick)
# toaster = ToastNotifier()
with tempfile.TemporaryDirectory() as directory:
    # if True:
    while True:
        pcName = platform.node()
        encodedName = base64Encode(pcName)
        address = f'http://{websiteAddress}/?pcname={encodedName}'
        r = requests.get(address)
        # text = r.text.replace("<html>", "").replace("</html>", "").replace("<head>", "").replace("</head>",
        # "").replace("<body>", "").replace("</body>", "")
        notifications = r.json()

        for notifi in notifications:
            # decode json data
            receiverUUID = base64Decode(notifi["recieverUUID"])
            iconData = base64.b64decode(notifi["iconData"])
            title = base64Decode(notifi["title"])
            content = base64Decode(notifi["content"])
            id = base64Decode(notifi["id"])
            sender = base64Decode(notifi["sender"])

            # download and save picture
            filename = "picture.ico"
            filePath = directory + "\\" + filename
            writeData = "".encode("utf-8")
            if iconData[:4] == "http":
                writeData = requests.get(iconData).content
            else:
                utfDecoded = iconData.decode("utf-8")
                beginDataIndex = utfDecoded.rindex(",") + 1
                description = utfDecoded[:beginDataIndex]
                print(description + "(" + content + ")")
                data = utfDecoded[beginDataIndex:]
                if "icon" in description:
                    writeData = base64.b64decode(data)

            # delete file when existing
            if os.path.exists(filePath):
                os.remove(filePath)
            # write image in file
            open(filePath, 'wb').write(writeData)
            # set filepath to NUll if no image is written
            if writeData == "".encode("utf-8"):
                filePath = None

            # if filePath is not None:
            # send notification
            notification.notify(
                app_name="Notifier",
                title="title",
                message="content",
                app_icon="icon.ico",  # e.g. 'C:\\icon_32x32.ico'
                timeout=15,
                ticker="null",
            )
            # notify.notify(content, title, filepath, True, 5, notify.dwInfoFlags.NIIF_USER | notify.dwInfoFlags.NIIF_LARGE_ICON)
            # toaster.show_toast(title=title,
            #             msg=content,
            #             icon_path=filepath,
            #             duration=None)
            time.sleep(5)
        print(".")
# notify.uninit()
