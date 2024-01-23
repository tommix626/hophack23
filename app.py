from flask import Flask, request, render_template, redirect, url_for
from gpt_api import GPTReader

app = Flask(__name__, template_folder='Templates')
# app.config['UPLOAD_FOLDER'] = "img/"
# Initialize the "txt" variable
user_input_link = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    global user_input_link

    if request.method == 'POST':
        user_input_link = request.form['userInput_var']
        # Redirect to the output page after saving the input
        return redirect(url_for('open_dash_window'))

    return render_template('home.html')


@app.route('/open_dash_window', methods=['GET', 'POST'])
def open_dash_window():
    window_script = f"window.open('http://localhost:8050/data?url={user_input_link}');"
    return f"<script>{window_script}</script>"


# @app.route("/process", methods=['GET', 'POST'])
# def process_user_input_link():
#     # use the openai api
#     reader = GPTReader()
#     reader.run(user_input_link)
#     print(reader.get_similar_sources())
#     # Render the output.html template with the value of the txt variable
#     return render_template('index_2.html', reader=reader)


# @app.route('/save', methods=['POST'])
# def save_text():
#     global user_input_link
#     user_input_link = request.form.get('user_text')
#     return "Text saved successfully." + user_input_link

###Bash app###
#
# bashapp=Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
#
# bashapp.layout = html.Div([
#     html.H1(children='Analytic Report', style={'textAlign':'center'}),
#     dcc.Graph(figure=radar_fig,style={}),
#     dcc.Graph(figure=create_gauge_graph(data=None))
# ])
# bashapp.layout = html.Div([
#     html.H1(children='Analytic Report', style={'textAlign':'center'}),
#     html.Div([
#         html.Br(),
#         html.Div(children=[dcc.Graph(figure=radar_fig,style={})], style={'padding': 10, 'flex': 1}),
#         html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=None))], style={'padding': 10, 'flex': 1})
#     ], style={'display': 'flex', 'flex-direction': 'row'}
#     )
# ])


if __name__ == '__main__':
    app.run(debug=True)
