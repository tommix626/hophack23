from flask import Flask, render_template, request

app=Flask(__name__,template_folder='Templates')
# app.config['UPLOAD_FOLDER'] = "img/"
# Initialize the "txt" variable
txt = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_text():
    global txt
    txt = request.form.get('user_text')
    return "Text saved successfully." + txt

if __name__ == '__main__':
    app.run(debug=True)