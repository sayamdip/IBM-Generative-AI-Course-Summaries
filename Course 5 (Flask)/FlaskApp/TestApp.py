from flask import Flask

app = Flask(__name__)

# Adding Routes

@app.route("/")
def hello_world():
    return "<b> My Test App In Action </b>"

if __name__ == "__main__":
    app.run(debug=True)
