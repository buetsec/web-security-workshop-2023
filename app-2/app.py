from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/file/")
def file():
    file = request.args.get("name")
    try:
        content = open(file, "r").read()
    except:
        content = "The file couldn't be found. Are you sure you put correct file name?"
    return content

if __name__ == "__main__":
    app.run(debug=True)
