from flask import Flask

exerciseApp = Flask(__name__)

@exerciseApp.route("/")
def return_dictionary():
    return {"Name":"Sayamdip Dey Chaklader"}