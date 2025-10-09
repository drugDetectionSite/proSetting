from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/textAno')
def textAno():
    return render_template('textAno.html')

@app.route('/drugDict')
def drugDict():
    return render_template('drugDict.html')

if __name__ == '__main__':
    print("start")
    app.run(debug=True)