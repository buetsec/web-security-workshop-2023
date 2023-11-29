from flask import Flask, request, render_template, make_response, redirect, url_for
import jwt
import json


app = Flask(__name__)
secret = "this-is-the-app-secret"


db = None
def load_database():
    global db
    db = json.load(open("database.json"))
    print("Database has been loaded")

def save_database():
    global db
    json.dump(db, open("database.json", "w"), indent=4)
    print("Database has been saved")

def insert_to_database(user_data):
    global db
    db.append(user_data)


def generate_token(data):
    global secret
    encoded = jwt.encode(data, key=secret)
    return str(encoded)

def decode_token(data):
    decoded = jwt.decode(data, key=None, options={"verify_signature": False})
    return decoded


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if "token" in request.cookies:
            print("Cookie is available")
            token = request.cookies.get("token", None)
            if token:
                try:
                    token = decode_token(token)
                    username = token["username"]

                    global db
                    for user in db:
                        if user["username"] == username:
                            message = user["message"]
                            return f"The message is: {message}"
                    # exhausted
                    return "There's no user with this name. Clear cookies."
                except:
                    return "Error in decoding cookie. Clear cookies."
            else:
                # no cookie present
                return redirect(url_for("login"))
        else:
            # no cookie present
            return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        global db
        for user in db:
            if user["username"] == username:
                if user["password"] == password:
                    print("User matched")
                    data = {
                        "username": username,
                    }
                    token = generate_token(data=data)
                    resp = make_response("Login success!")
                    resp.set_cookie("token", token)
                    return resp
                else:
                    return "Wrong password"
        # exhausted
        return "Username not in database"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        message  = request.form.get("message")

        global db
        user_id = len(db) + 1
        user_data = {
            "id": user_id,
            "username": username,
            "password": password,
            "message": message 
        }
        insert_to_database(user_data)
        save_database()
        print("User data has been created")
        return "User data has been created!"
    else:
        return "Wrong method. Refresh & try again."


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        resp = redirect(url_for("login"))
        resp.set_cookie("token", "")
        return resp


if __name__ == "__main__":
    load_database()
    app.run(debug=True)
