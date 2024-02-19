from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/record')
def food_record():
    return render_template('record.html')

if __name__ == '__main__':
    app.run(debug=True)
