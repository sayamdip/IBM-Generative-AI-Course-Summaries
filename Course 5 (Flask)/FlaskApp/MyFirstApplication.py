from flask import Flask

my_app=Flask("My First Application")


@my_app.route("/")

def hello_world():
    return "Hello World"

if __name__ == "__main__":
    my_app.run(debug=True, port=5000)