#!/usr/bin/env python3
from flask import Flask
from flask import request  # to handle the different http requests
from flask import Response  # to reply (we could use jsonify as well but we handled it)
import json, time, threading

# My libraries
from client import Client
from message_catalog import MessageCatalog

from pynput import keyboard

app = Flask(__name__)

# “Routes” will handle all requests to a specific resource indicated in the
# @app.route() decorator


# These routes are for the "person" use case
# case 1 : if client receive a response (status 200), the app is running
@app.route("/", methods=["GET"])
def index():
    response = Response("running", mimetype="text/plain", status=200)
    return response


# case 2 other client sent a message
@app.route("/<msg>", methods=["POST"])
def receive_msg(msg):
    client.catalog.addHeardMessage(msg)  # adding message to client's catalog
    response = Response("ok", mimetype="text/plain", status=200)
    return response


# case 3 change distance parameter
@app.route("/proximity", methods=["GET"])
def change_proximity():
    client.toggleProximity()  # changing client's proximity variable
    response = Response("ok", mimetype="text/plain", status=200)
    return response


# End of person use case


# Hospital use case
@app.route("/they-said", methods=["GET", "POST"])
def hospital_use_case():
    if request.method == "GET":
        client.catalog.purge()  # removing outdated messages from hospital
        # the reponse will be a json structure with all messages in the hospital catalog
        response = Response(
            client.catalog.exportData(2), mimetype="application/json", status=200
        )
    else:
        # in case the client used post : he declared covid
        # importing all "he's said messages" in the hospital catalog
        client.catalog.importData(json.loads(request.get_json()))
        response = Response("ok", mimetype="text/plain", status=200)
    return response


# End of hospital use case


# key listening thread function to test the app
def on_press(key):
    vars(key)
    if key == keyboard.Key.esc:  # escape closes the app
        client.catalog.save()  # writing on xml
        print("\n Closing ANTICOVID")
        client.run = False
        return False  # stop listener
    elif key == keyboard.Key.ctrl_l:
        client.send_history()  # clients has covid, sending its messages to the hospital
    elif key == keyboard.Key.alt_l:
        client.toggleProximity(True)  # toggle proximity with the other user
    elif key == keyboard.Key.shift:
        client.get_covid()  # check if user has covid based on hosp catalog
    elif key == keyboard.Key.caps_lock:
        print(client.catalog)


# running server thread function
def launch_app():
    print("lauching server\n")
    app.run(host="0.0.0.0", debug=False)


# will only execute if this file is run
if __name__ == "__main__":

    # 1 - defining variables
    hospital_ip = ""  # computer running hospital's ip
    other_client_ip = ""  # the other client's ip
    client = Client(MessageCatalog("msgxml.xml"))
    # client can be instancied with hospital and other client ip
    # localhost by default
    # in case you play hospital, no need to fill ip variables

    # 2 - launching app on a separate daemon thread
    x = threading.Thread(target=launch_app, daemon=True)
    x.start()
    # thread will be killed when main reach its end

    time.sleep(1)

    # 3 - waiting for all computers to be running the app
    while client.allClientsReady() == False:
        print("En attente des autres PC")
        time.sleep(5)  # retrying every 5 seconds
        # does sleep mean we won't receive requests during those 5 secs tho?

    print("\n Tous les utilisateurs sont connectés")
    print("\n Aucun utilisateur à proximité \n")

    # 4 - when ready (all users launched) starting the key listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    # CONTROLS :
    # alt = toggle proximity (commanded by client's location in final app)
    # control = declare a covid case
    # shift = check if client can be infected
    # CAPS LOCK = print catalog to console
    # escape = quit the app

    # 5 - running the client's loop
    t = time.time()
    loop_interval = 5  # 5s between two client's loop
    while client.run:
        if time.time() >= t + loop_interval:
            client.loop()  # sends a message and checks for any covid risks
            t = time.time()
