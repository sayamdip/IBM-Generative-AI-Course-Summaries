from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def get_author():
    res = requests.get("https://openlibrary.org/search/authors.json?q=William Shakespeare")

    if res.status_code == 200:
        return {"message": res.json()}
    elif res.status_code == 404:
        return {"message": "Something Went Wrong!"}, 404
    else:
        return {"message": "Server Error!"},500

if __name__ == "__main__":
    app.run(debug=True, port=5001)