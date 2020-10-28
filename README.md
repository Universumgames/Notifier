# Notifier

This is a small notifier app for your windows pc.
Notifications can be send with your own webserver wether in your local network, a virtual private network (VPN) or with a webserver on the internet.

## Usage

1. To set up everything just move the files inside the ```server``` directory to your webserver folder. The alternative is to use a container with Docker for example, better instructions with using docker to run the webserver will follow, but it's working, so if you know what you're doing within docker, just try it out.
2. Currently you need to edit the ```data.json``` file and edit it to add the pc's you want to use with this application. In the future this won't be neccessary anymore.... 
<br/>
But in the meantime you have to change the ```name``` parameter to the name of your PC and change the ```uuid``` attribute to whatever you like. It's important that for every other pc you want to add, you have to give the ```name``` as well as an ```uuid```. 
3. The last thing to do is start the ```python/startNotifier.bat``` file to run the notifier. 
4. You can add a seperate script into the Startup folder, so that the script automatically runs everytime your computer starts.
5. Now you can send a notification to your computer by running the ```python/addNotification.py``` file, accessing the ```index.php``` on your webserver or sending a POST request to your ```index.php``` if everything is set up correctly you should recieve a notification.

