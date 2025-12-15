from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/getall')
def getall():
    return render_template('getall.html')

if __name__ == '__main__':
    app.run(debug=True)