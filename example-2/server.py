from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    print("****************")
    print(request.headers)
    print("****************")
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)

