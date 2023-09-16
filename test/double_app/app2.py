from flask import Flask, render_template

app2 = Flask(__name__)

@app2.route('/display_in_new_window', methods=['GET','POST'])
def display_in_new_window():
    # Generate the content you want to display in the new window/tab
    content = "<h1>Hello from App 2!</h1>"

    # You can also include JavaScript to manipulate the new window/tab if needed
    script = "<script>alert('App 2 content loaded');</script>"

    return f"{content}{script}"


if __name__ == '__main__':
    app2.run(port=5001,debug=True)