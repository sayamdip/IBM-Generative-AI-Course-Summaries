from flask import Flask

myApp = Flask(__name__)

@myApp.route("/")

def hello_world():
    return "<b>Hello World!, My Name Is Sayamdip Dey Chaklader</b>"
