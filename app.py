from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'dkdjflkjlkajlkj!'

if __name__ == '__main__':
    print("start")
    app.run(debug=True)