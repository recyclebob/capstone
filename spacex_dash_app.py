# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
#max_payload = spacex_df['Payload Mass '].max()
#min_payload = spacex_df['PayloadMass'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                             ],
                                             #searchable=True,
                                             placeholder='select launch sites'
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
                Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value')
            )
def get_pie_chart(launch_site):
    if launch_site == 'ALL':
        classed_df = spacex_df.groupby('class')['Flight Number'].count().reset_index()
        classed_df.rename(columns={'Flight Number':'Count'}, inplace=True)
        #success_launches = spacex_df[spacex_df['class'] == 1]
        #fail_launches = spacex_df[spacex_df['class'] == 0]
        #launches = [success_launches, fail_launches]
        #labels = ['Successful Launches', 'Failed Launches']
        fig = px.pie(classed_df, 
        values='Count',
        names='class', 
        title='successful vs failed launches for all launch sites')
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == launch_site]
        classed_df = site_df.groupby('class')['Flight Number'].count().reset_index()
        classed_df.rename(columns={'Flight Number':'Count'}, inplace=True)
        #success_launches = site_df[site_df['class'] == 1]
        #fail_launches = site_df[site_df['class'] == 0]
        #launches = [success_launches, fail_launches]
        #labels = ['Successful Launches', 'Failed Launches']
        fig = px.pie(classed_df, 
        values='Count',
        names='class', 
        title='successful vs failed launches for launch site {}'.format(launch_site))
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
                Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id="payload-slider", component_property="value")]
            )
def get_scatter_chart(launch_site, payload_range):
    payload_min = payload_range[0]
    payload_max = payload_range[1]
    payload_df = spacex_df[(payload_min <= spacex_df['Payload Mass (kg)']) & (spacex_df['Payload Mass (kg)'] <= payload_max)]
    if launch_site == 'ALL':
        fig = px.scatter(payload_df, x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",
        title='payload vs launch success vs booster version for all launch\
             sites in payload range {} to {} kg'.format(payload_min, payload_max),
        )
        return fig
    else:
        site_df = payload_df[payload_df['Launch Site'] == launch_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",
        title='payload vs launch success vs booster version for launch site {}\
             in payload range {} to {} kg'.format(launch_site, payload_min, payload_max),
        )
        return fig
# Run the app
if __name__ == '__main__':
    print("min_payload", min_payload)
    app.run_server()
