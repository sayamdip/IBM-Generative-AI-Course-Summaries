

def jsonify_decorator(function):

    def modifyOutput():

        return {"Output":function()}

    return modifyOutput




@jsonify_decorator
def hello():
    return "Hello World"

@jsonify_decorator
def add():
    num1=int(input("Enter A Number="))
    num2=int(input("Enter Another Number="))
    return num1 + num2


print(hello())
print(add())