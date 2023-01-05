from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/indianCuisine')
def indianCuisine():
    return render_template('indianCuisine.html')

@app.route('/westernDelights')
def westernDelights():
    return render_template('westernDelights.html')

if __name__ == '__main__':
    app.run(debug=True) 
