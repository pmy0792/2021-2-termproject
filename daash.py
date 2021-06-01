import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

result = pd.read_csv("./static/result5.csv")[["College", "Major", "Continent", "Country", "Foreign Univ", "Semester", "Url"]]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
def create_dash_app(flask_app):
    dash_app=dash.Dash(
        server=flask_app,
        name="dashboard",
        url_base_pathname='/dashboard/'
    )
    dash_app.layout = html.Div(children=[
        html.H1(children='Dash Board'),

        html.Div(children='''
            대륙별 파견 현황
        '''),

        dcc.Graph(
            id='continent-country-graph',
            figure=make_fig1()
        ),

        html.Div(children='''
            학기별 파견현황
        '''),
        dcc.Graph(
            id='semester-graph',
            figure=make_fig2()
        )

    ])

def make_fig2():
    semester = result["Semester"].value_counts().rename_axis('Semester').reset_index(name='Count')
    semester_df = pd.DataFrame(columns=["Semester", "Count"])

    for index, row in semester.iterrows():

        if row["Semester"].endswith('-1'):
            new_sem = int(row["Semester"][:4])
        elif row["Semester"].endswith('-2'):
            new_sem = int(row["Semester"][:4]) + 0.5
        else:
            print("error!")
        semester_df = semester_df.append({"Semester": new_sem, "Count": row["Count"]}, ignore_index=True)
    semester_df = semester_df.sort_values(by="Semester", ascending=True).reset_index(drop=True)
    fig = px.line(semester_df, x="Semester", y="Count")
    return fig

def make_fig1():

    continents = result["Continent"].unique()
    continents = list(continents)
    continents

    df = pd.DataFrame(columns=["Continent", "Country", "Count"])
    for continent in continents:
        temp = result[result["Continent"] == continent]
        country_count = temp["Country"].value_counts().rename_axis('Country').reset_index(name='Count')

        for index, row in country_count.iterrows():
            df = df.append({"Continent": continent, "Country": row["Country"], "Count": row["Count"]},
                           ignore_index=True)
    fig = px.bar(df, x="Continent", y="Count", color="Country")
    #fig.show()
    return fig


