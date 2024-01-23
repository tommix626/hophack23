from flask import redirect, url_for, Flask, render_template, request, jsonify
import requests

app1 = Flask(__name__)

@app1.route('/', methods=['GET', 'POST'])
def index():
    global user_input_link

    if request.method == 'POST':
        # user_input_link = request.form['userInput_var']
        # Redirect to the output page after saving the input
        return redirect(url_for('open_dash_window'))

    return render_template('testhome.html')

@app1.route('/open_app2_window', methods=['GET','POST'])
def open_app2_window():
    # Send a POST request to app2
    # response = requests.post('http://localhost:5001/display_in_new_window')

    # Handle the response to open a new window/tab in the client-side JavaScript
    window_script = f"window.open('http://localhost:8050/api/callback/');"
    return f"<script>{window_script}</script>"

@app1.route('/open_dash_window', methods=['GET','POST'])
def open_dash_window():
    window_script = f"window.open('http://localhost:8050/data?url=baidu.com');"
    return f"<script>{window_script}</script>"


if __name__ == '__main__':
    app1.run(port=5000)