from flask import Flask, make_response, request

app = Flask(__name__)




# Define a route for the root URL ("/")
@app.route("/")
# Define the view function for the index route
def index():
    # Function that handles requests to the root URL
    # Return a plain text response
    return "Hello World, My Name Is Sayamdip Dey Chaklader"

# Define a route for the "/no_content" URL
@app.route("/no_content")
def no_content():
    """Return 'no content' and a 204 status code.

    Returns:
        tuple: A tuple containing a string message and a status code.
    """
    # Create a response object with the message "Hello World"
    resp = make_response({"message": "Hello World"})
    # Set The Status Code Of The Response To 200
    resp.status_code = 204
    # Return The Response Object
    return resp

@app.route("/count")
def count():
    try:
        # Attempt To Return The Count Of Items In 'Data' As A JSON Response
        return {"data count": len(data)}, 200
    except NameError:
        # Handle the Case Where 'Data' Is Not Definded
        # Return A JSON Response With A Message And A 500 Internal Server Error Status Code
        return {"message": "data not defined"}, 500

@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    # Iterate through the 'data' list to search for a person with a matching ID
    for person in data:
        # Check if the 'id' field of the person matches the 'id' parameter
        if person["id"] == str(id):
            # Return the matching person as a JSON response with a 200 OK status code
            return person

    # If no matching person is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "person not found"},404

@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    # Iterate through the 'data' list to search for a person with a matching ID
    for person in data:
        # Check if the 'id' field of the person matches the 'id' parameter
        if person["id"] == str(id):
            # Remove the person from the 'data' list
            data.remove(person)
            # Return a JSON response with a message confirming deletion and a 200 OK status code
            return {"message": f"Person With ID {id} Deleted"},200
    # If no matching person is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "person not found"}, 404

@app.route("/person", methods=["POST"])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    # Code To Validate new_person ommitted
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500
    
    return {"message": f"{new_person['id']}"}, 200
