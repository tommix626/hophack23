from flask import Flask, request, render_template, redirect, url_for

app=Flask(__name__,template_folder='Templates')
# app.config['UPLOAD_FOLDER'] = "img/"
# Initialize the "txt" variable
user_input_link = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global user_input_link

    if request.method == 'POST':
        user_input_link = request.form['userInput_var']
        # Redirect to the output page after saving the input
        return redirect(url_for('process_user_input_link'))

    return render_template('index.html')


@app.route("/process", methods=['GET', 'POST'])
def process_user_input_link():
    #use the openai api
    
    # Render the output.html template with the value of the txt variable
    return render_template('index_2.html', user_link=user_input_link)


@app.route('/save', methods=['POST'])
def save_text():
    global user_input_link
    user_input_link = request.form.get('user_text')
    return "Text saved successfully." + user_input_link

if __name__ == '__main__':
    app.run(debug=True)