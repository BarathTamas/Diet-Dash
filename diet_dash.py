# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 20:15:14 2021

@author: barath_tamas
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import jellyfish

def calc_total_macros(df,drop=True):
    macros=["kcal","protein","carbs","fat"]
    for macro in macros:
        df["total "+macro]=df["g"]/100*df[macro]
    if drop:
        df.drop(macros,axis=1,inplace=True)

#%%
food_types_df=pd.read_csv(
    r"C:\Users\Tamás Baráth\Documents\diet\meal_types.csv",
                       sep=",")
food_types_df["name"]=food_types_df["name"].astype(str)
foods_eaten_df=pd.read_csv(
    r"C:\Users\Tamás Baráth\Documents\diet\meals_eaten.csv",
                       sep=",")
foods_eaten_dict=foods_eaten_df.to_dict()
foods_eaten_df["date"]=pd.to_datetime(foods_eaten_df["date"],
                                      format="%d/%m/%Y")

food_types=food_types_df["name"].unique()

today = pd.to_datetime("today")
today_string=str(today.day)+"/"+str(today.month)+"/"+str(today.year)
#%%
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#color scheme:
sand_brown="#F7F4EF"
dark_blue="#31525b"
light_blue="#b3dee5"
orange="#ffa101"
peach_yellow="#fae6b1"
maroon="#712e1e"
green="#788402"

img_url='url("/assets/smooth_paper_texture.jpg")'

tabs_styles = {
    'height': '30px',
    'display': 'inline-block',
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': sand_brown,
    'color':dark_blue,
    'padding': '0px',
    'fontWeight': 'bold',
    'borderRadius': '10px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': peach_yellow,
    'color': maroon,
    'fontWeight': 'bold',
    'padding': '0px',
    'borderRadius': '10px'
}

# Main panel
app.layout = html.Div(
    className='dashboard',
    style={'backgroundColor':sand_brown,
           'display': 'block'},
    children=[
        # add title
        html.H1(children='Diet Dashboard',
                style={'margin-left':'30px',
                       'color': orange}),
        dcc.Markdown('''
            [Don't forget!](https://www.youtube.com/watch?v=1LsIQr_4iSY)
            ''',
            style={'margin-left':'30px',
                   'margin-bottom':'20px'}),
        # new food input
        html.Div(
            className='new food',  # option selection panel
            children=[
                html.H2(
                    children='Enter new food type',
                    style={'color': maroon,
                           'margin-left':'15px',
                           'margin-right':'15px'}),
                html.Div(children=[
                    html.Div(children=[
                        html.Label('Food name',
                                   style={'color': dark_blue,
                                          'margin-left':'15px',
                                          'margin-right':'15px'}),
                        dcc.Input(
                            style={'width': 300,
                                   'display': 'block',
                                   'margin-left':'15px',
                                   'margin-right':'15px'},
                            id="new-food-name", 
                            type="text",
                            disabled=False,
                            value=""
                        ),
                        html.Div(style={'display': 'block',
                                        'margin-left':'15px',
                                        'margin-right':'15px',
                                        "maxWidth": "300px"},
                                 id="similar-food"
                        )
                    ],
                    style={'display': 'block'},
                    ),
                    html.Div(children=[
                        html.Label('Kcal',
                                   style={'color': dark_blue,
                                          'margin-left':'15px',
                                          'margin-right':'15px'}),
                        dcc.Input(
                            style={'width': 100,
                                   'color': dark_blue,
                                   'margin-left':'15px',
                                   'margin-right':'15px'},
                            id="new-food-kcal", 
                            disabled=False,
                        ),
                    ],
                    style={'display': 'inline-block'},
                    ),
                    html.Div(children=[
                        html.Label('Protein',
                                   style={'color': dark_blue,
                                          'margin-left':'15px',
                                          'margin-right':'15px'}),
                        dcc.Input(
                            style={'width': 100,
                                   'color': dark_blue,
                                   'margin-left':'15px',
                                   'margin-right':'15px'},
                            id="new-food-protein", 
                            disabled=False,
                        ),
                    ]
                    ),
                    html.Label('Carbohydrates',
                               style={'color': dark_blue,
                                      'margin-left':'15px',
                                      'margin-right':'15px'}),
                    dcc.Input(
                        style={'width': 100,
                               'color': dark_blue,
                               'margin-left':'15px',
                               'margin-right':'15px'},
                        id="new-food-carbs", 
                        disabled=False,
                    ),
                    html.Label('Fat',
                               style={'color': dark_blue,
                                      'margin-left':'15px',
                                      'margin-right':'15px'}),
                    dcc.Input(
                        style={'width': 100,
                               'color': dark_blue,
                               'margin-left':'15px',
                               'margin-right':'15px',
                               'margin-bottom': '15px'},
                        id="new-food-fat", 
                        disabled=False,
                    ),
                    html.Button(id='new-food-btn',
                        n_clicks=0,
                        children='Submit',
                        style={'backgroundColor': sand_brown,
                               'color':dark_blue}
                    )
                ])
            ],
            style={'display': 'inline-block',
                   'margin-left':'15px',
                   'vertical-align': 'top',
                   'backgroundColor':peach_yellow,
                   'borderRadius': '15px'}
        ),
        # eaten food entry panel
        html.Div(
            className='food eaten',  # option selection panel
            children=[
                html.H2(children='Enter food eaten',
                        style={'color': maroon,
                               'margin-left':'15px',
                               'margin-right':'15px'}),
                # dropdown to select food eaten
                html.Label('Select food type',
                           style={'color': dark_blue,
                                  'margin-left':'15px',
                                  'margin-right':'15px'}),
                # generate dropdowns for every hour of the day with a loop
                dcc.Dropdown(
                    style={'width': 250,
                           'color': dark_blue,
                           'margin-left':'8px',
                           'margin-right':'15px'},
                    id='eaten-food-name',
                    value='0'
                ),
                html.Label('Enter weight in grams',
                           style={'color': dark_blue,
                                  'margin-left':'15px',
                                  'margin-right':'15px'}),
                dcc.Input(
                        style={'width': 50,
                               'color': dark_blue,
                               'margin-left':'15px',
                               'margin-right':'5px',
                               "-moz-appearance": "textfield",
                               "-webkit-appearance": "none"},
                        id="eaten-food-weight0",
                        disabled=False,
                        value="",
                ),
                html.Label('/',
                           style={"width":5,
                                  'color': dark_blue,
                                  "font-size":15,
                                  'margin-left':'0px',
                                  'margin-right':'0px',
                                  'display': 'inline-block'}),
                dcc.Input(
                        style={'width': 40,
                               'color': dark_blue,
                               'margin-left':'5px',
                               'margin-right':'10px',
                               'display': 'inline-block',
                               "-moz-appearance": "textfield",
                               "-webkit-appearance": "none"},
                        id="eaten-food-div",
                        disabled=False,
                        value=1,
                ),
                html.Label('X',
                           style={"width":10,
                                  'color': dark_blue,
                                  "font-size":15,
                                  'margin-left':'0px',
                                  'margin-right':'0px',
                                  'display': 'inline-block'}),
                dcc.Input(
                        style={'width': 40,
                               'color': dark_blue,
                               'margin-left':'5px',
                               'margin-right':'5px',
                               "-moz-appearance": "textfield",
                               "-webkit-appearance": "none"},
                        id="eaten-food-mult",
                        disabled=False,
                        value=1,
                ),
                html.Label('=',
                           style={"width":10,
                                  'color': dark_blue,
                                  "font-size":15,
                                  'margin-left':'0px',
                                  'margin-right':'0px',
                                  'display': 'inline-block'}),
                dcc.Input(
                        style={'width': 50,
                               'color': dark_blue,
                               'margin-left':'5px',
                               'margin-right':'15px',
                               'display': 'inline-block',
                               "-moz-appearance": "textfield",
                               "-webkit-appearance": "none"},
                        id="eaten-food-weight1",
                        disabled=False,
                ),
                html.Label('Enter Date',
                           style={'color': dark_blue,
                                  'margin-left':'15px',
                                  'margin-right':'15px',
                                  'display': 'block'}),
                dcc.Input(
                        style={'width': 100,
                               'color': dark_blue,
                               'margin-left':'15px',
                               'margin-right':'15px',
                               'margin-bottom': '15px',
                               'display': 'block'},
                        id="eaten-food-date", 
                        type="text",
                        value=today_string,
                        disabled=False,
                ),
                html.Button(id='eaten-food-btn',
                        n_clicks=0,
                        children='Submit',
                        style={'backgroundColor': sand_brown,
                               'color': dark_blue,
                               'margin-left':'15px',
                               'margin-right':'15px'}
                ),
                # daily food summary
                html.Div(
                    children=[
                    html.H2(children='Summary',
                        style={'color': green}),    
                    html.Div(
                        id="summary",
                        style={'color': dark_blue,
                               'display': 'block',
                               'vertical-align': 'top'}
                    )
                ],
                style={'display': 'block',
                                   'margin-left':'15px',
                                   'vertical-align': 'top'}
                ),
            ],
            style={'display': 'inline-block',
                   'margin-left':'15px',
                   'vertical-align': 'top',
                   'backgroundColor':peach_yellow,
                   'borderRadius': '15px'}
        ),
        html.Div(
            style={'margin-left':'15px',
                        "display":"inline-block"},
            children=[
        dcc.Tabs(
            style=tabs_styles,
            children=[
            dcc.Tab(label='Graph tab',
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                # add panel with graph
                html.Div(
                    children=[
                    # add graph to dashboard
                    dcc.Graph(id='timeseries-graph',
                              style={'display': 'inline-block',
                                      'margin-left':'0px',
                                      'margin-right':'0px',
                                      'margin-top':'0px',
                                      'margin-bottom':'0px',
                                      'vertical-align': 'top'})
                    ],
                    style={'background-image': img_url,
                           'display': 'inline-block',
                           'vertical-align': 'top',
                           'backgroundColor':sand_brown,
                           'borderRadius': '15px'}
                )
                ]),
                dcc.Tab(label='Table tab',
                        style=tab_style,
                        selected_style=tab_selected_style,
                        children=[   
                            dash_table.DataTable(
                            id='food-types-table',
                            columns=[{
                                'name': i,
                                'id': i } for i in list(food_types_df.columns)],
                            data=[
                                {i: food_types_df[i][j] for i in list(food_types_df.columns)}
                                for j in range(len(food_types_df))
                            ],
                            editable=True
                        )
    
            ]) 
        ])
        ]),
        # Save changes button
        html.Div(
            className='save',  # option selection panel
            children=[
                html.Button(id='save-btn',
                            n_clicks=0,
                            children='Save changes',
                            disabled=False,
                            style={'backgroundColor': peach_yellow,
                                   'color':maroon,
                                   'width':'20%'}
                )
            ],
            style={'display': 'block',
                   'margin-top':'0px',
                   'margin-left':'30px',
                   'vertical-align': 'top'}
        ),
        dcc.Store(id='food-types-memory',
                  storage_type='local'),
        dcc.Store(id='eaten-food-memory'
                  ,storage_type='local'),
        html.Div(id='hidden-div', style={'display':'none'})
    ])
             
# callback for checking for similar food type
@app.callback(
    Output(component_id='similar-food',component_property='children'),
    Input(component_id='new-food-name',component_property= 'value'))
def get_similar(new_name):
    global food_types_df
    closest_name=""
    max_sim=0
    if new_name != "":
        for name in food_types_df["name"]:
            sim=jellyfish.jaro_similarity(name, new_name)
            if sim>max_sim:
                max_sim=sim
                closest_name=name
        out="{} - similarity: {:.2f}".format(closest_name,max_sim)
        return out
        
# callback for adding new food type and updating dropdown
@app.callback(
    Output(component_id='eaten-food-name', component_property='options'),
    Input(component_id='new-food-btn', component_property='n_clicks'),
    State(component_id='new-food-name',component_property= 'value'),
    State(component_id='new-food-kcal',component_property= 'value'),
    State(component_id='new-food-protein',component_property= 'value'),
    State(component_id='new-food-carbs',component_property= 'value'),
    State(component_id='new-food-fat',component_property= 'value'))
def update_types(n_clicks,name,kcal,protein,carbs,fat):
    global food_types_df
    if n_clicks>0 and name!=0 and kcal!=0:
        new_food=pd.DataFrame({
            "name": [name],
            "kcal":[float(kcal)],
            "protein":[float(protein)],
            "carbs":[float(carbs)],
            "fat":[float(fat)]
             })
        if not new_food["name"][0] in food_types_df["name"].to_list():
            food_types_df=food_types_df.append(new_food)
    # always populate dropdown -> have values at startup
    out=[{"label":food_name, 'value': food_name}
            for food_name in food_types_df["name"].unique()] 
    return out
    
# callback for calculating eaten food weight
@app.callback(
    Output(component_id='eaten-food-weight1', component_property='value'),
    Input(component_id='eaten-food-weight0', component_property='value'),
    Input(component_id='eaten-food-div', component_property= 'value'),
    Input(component_id='eaten-food-mult',component_property= 'value'))
def calc_weight(weight0,div,mult):
    if weight0=="":
        return ""
    div=float(div)
    mult=float(mult)
    if mult==0:
        return 0
    if div>0:
        weight0=float(weight0)
        return weight0/div*mult
    else:
        return ""

# callback for adding eaten food
@app.callback(
    Output(component_id='eaten-food-memory', component_property='value'),
    Input(component_id='eaten-food-btn', component_property='n_clicks'),
    State(component_id='eaten-food-name',component_property= 'value'),
    State(component_id='eaten-food-weight1',component_property= 'value'),
    State(component_id='eaten-food-date',component_property= 'value'))
def update_eaten(n_clicks,name,weight,date):
    global foods_eaten_df
    if n_clicks>0 and weight!=0 and name!=0:
        new_food_eaten=pd.DataFrame({
        "name": [name],
        "g":[weight],
        "date":[date]
         })
        new_food_eaten["date"]=pd.to_datetime(new_food_eaten["date"],
                                              format="%d/%m/%Y")
        foods_eaten_df=foods_eaten_df.append(new_food_eaten)
    return 0
        
# callback for summary, chained from update_eaten through dummy output/input
# updates when date is chanaged or when new food is input
@app.callback(
    Output(component_id='summary',component_property='children'),
    Input(component_id='eaten-food-memory', component_property='value'),
    Input(component_id='eaten-food-date',component_property= 'value'))
def summary(_,date):
    global food_types_df
    global foods_eaten_df
    macros=["kcal","protein","carbs","fat"]
    #timestamp=pd.Timestamp(today_string)
    date_selected=pd.to_datetime(date,format="%d/%m/%Y")
    # Select meals eaten at date
    macros_df=foods_eaten_df[foods_eaten_df['date']==date_selected] 
    # left join food macros
    macros_df=macros_df.merge(food_types_df,on="name")
    # calculate total macros
    calc_total_macros(macros_df)
    out=["Date: {}".format(date_selected.strftime("%d/%m/%Y"))]
    for macro in macros:
        out.append("{} eaten: {:.2f}".format(
            macro,macros_df["total "+macro].sum()))
    return html.P([out[0],html.Br(),
                   out[1],html.Br(),
                   out[2],html.Br(),
                   out[3],html.Br(),
                   out[4]])

# callback for saving changes
@app.callback(
    Output(component_id="hidden-div",component_property="value"),
    Input(component_id='save-btn', component_property='n_clicks'))
def save(n_clicks):
    global food_types_df
    global foods_eaten_df
    if n_clicks>0:
        food_types_df.to_csv(
            r"C:\Users\Tamás Baráth\Documents\diet\meal_types.csv",
                sep=",",index=False)
        foods_eaten_df["date"]=pd.to_datetime(foods_eaten_df["date"])
        foods_eaten_df.to_csv(
            r"C:\Users\Tamás Baráth\Documents\diet\meals_eaten.csv",
                sep=",",index=False,date_format="%d/%m/%Y")
        
    
@app.callback(
    Output(component_id='timeseries-graph', component_property='figure'),
    Input(component_id='eaten-food-memory', component_property='value'))
def update_timeseries_plot(_):
    plot_df=foods_eaten_df.merge(food_types_df,on="name")
    calc_total_macros(plot_df)
    plot_df=plot_df.resample("D",on="date").sum()
    plot_df['date'] = plot_df.index
    kcal_plot_df=plot_df[['date',"total kcal"]]
    mean_kcal=kcal_plot_df["total kcal"].mean()
    mean_protein=plot_df["total protein"].mean()
    plot_df=plot_df.drop(["g","total kcal"],axis=1)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            showlegend=False,
            name="mean kcal",
            x = [kcal_plot_df["date"].min(), kcal_plot_df["date"].max()],
            y = [mean_kcal, mean_kcal],
            mode = "lines",
            line=dict(color=orange, width=2,dash="dash"),
            marker = dict(color = orange, size=2,opacity=0.5)),
        secondary_y=True,
        row=1, col=1)
    fig.add_trace(
        go.Scatter(
            showlegend=False,
            name="mean protein",
            x = [kcal_plot_df["date"].min(), kcal_plot_df["date"].max()],
            y = [mean_protein, mean_protein],
            mode = "lines",
            line=dict(color=dark_blue, width=2,dash="dash"),
            marker = dict(color = dark_blue, size=2,opacity=0.5)),
        secondary_y=False,
        row=1, col=1)
    fig.add_trace(
        go.Scatter(x=plot_df["date"], y=plot_df["total protein"],
                   name="total protein",
                   mode="lines+markers",
                   line=dict(color=dark_blue, width=2),
                   marker=dict(color=dark_blue, size=8, opacity=0.8)),
        secondary_y=False)
    fig.add_trace(
        go.Scatter(x=plot_df["date"], y=plot_df["total carbs"],
                   name="total carbs",
                   mode="lines+markers",
                   line=dict(color=maroon, width=2),
                   marker=dict(color=maroon, size=8, opacity=0.8)),
        secondary_y=False)
    fig.add_trace(
        go.Scatter(x=plot_df["date"], y=plot_df["total fat"],
                   name="total fat",
                   mode="lines+markers",
                   line=dict(color=green, width=2),
                   marker=dict(color=green, size=8, opacity=0.8)),
        secondary_y=False)
    fig.add_trace(
        go.Scatter(x=kcal_plot_df["date"], y=kcal_plot_df["total kcal"],
                   name="total kcal",
                   mode="lines+markers",
                   line=dict(color=orange, width=4),
                   marker=dict(color=orange, size=16, opacity=0.8)),
        secondary_y=True,
    )
    
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        legend=dict(x=0.08,y=1,
            bgcolor='rgba(255,255,255,0.5)'),
        autosize=False,
        width=820,
        height=500,
        margin=dict(
        autoexpand=False,
        l=50,
        r=30,
        t=30,
        b=50),
        yaxis = dict(
            tickfont = dict(
              family = 'Old Standard TT, serif',
              size = 15,
              color = dark_blue)
            ),
        hovermode='x'
    )
    fig.update_xaxes(
        gridcolor="gray")
    fig.update_yaxes(
        nticks=12,
        range=[0, 550],
        title_text="<b>grams</b>",
        secondary_y=False,
        gridcolor="Silver ",
        zeroline=True,
        zerolinecolor="Silver ",
        fixedrange=True)
    fig.update_yaxes(
        dtick=400,
        range=[0, 4400],
        title_text="<b>kcal</b>",
        secondary_y=True,
        zeroline=False,
        fixedrange=True)
    fig['layout']['yaxis2']['showgrid'] = False
    fig['layout']['yaxis2']['nticks'] = 10
    fig.update_xaxes(
        dtick="d",
        tickformat="%d %b")
    
    return fig

@app.callback(
    Output('table-editing-simple-output', 'figure'),
    Input('food-types-table', 'data'),
    Input('food-types-table', 'columns'))
def update_table(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    return {
        'data': [{
            'type': 'parcoords',
            'dimensions': [{
                'label': col['name'],
                'values': df[col['id']]
            } for col in columns]
        }]
    }
# %%
if __name__ == '__main__':
    app.run_server(debug=False)