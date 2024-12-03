from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return "Hier gibt es nix zu sehen."

@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"

if __name__ == "__main__":
    app.run(port=5001, debug=True)