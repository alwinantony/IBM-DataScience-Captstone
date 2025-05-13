# Import required libraries
import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launchSiteList = spacex_df['Launch Site'].unique()
launchSiteList=np.append(launchSiteList,"ALL")
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
                                        {'label':i,'value':i} for i in launchSiteList
                                        ],
                                    placeholder='Select a Launch Site here',
                                    value='ALL',
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0, max=10000, step=1000, marks={0:'0', 100:'100'}, value=[400, 9600],id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selectedSite):
    if(selectedSite == 'ALL'):
        filtered_df=spacex_df[['Launch Site','class']]
        filtered_df=filtered_df.groupby('Launch Site', as_index=False).sum()
        fig = px.pie(filtered_df, values=filtered_df['class'], 
        names=filtered_df['Launch Site'], 
        title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selectedSite]
        successCounts = filtered_df['class'].value_counts()
        fig = px.pie(filtered_df, values=successCounts.values, 
        names=successCounts.index.values, 
        title='Total Success Launches for site ' + selectedSite)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value'),
)
def get_Scatter(selectedSite, payloadSlider):
    filtered_df = spacex_df
    if(selectedSite == 'ALL'):
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] >= payloadSlider[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] <= payloadSlider[1]]
        fig = px.scatter(x=filtered_df['Payload Mass (kg)'], y=filtered_df['class'], color=filtered_df['Launch Site'], title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selectedSite]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] >= payloadSlider[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] <= payloadSlider[1]]        
        fig = px.scatter(x=filtered_df['Payload Mass (kg)'], y=filtered_df['class'], labels={'x':'Payload (kg)', 'y':'Success'},symbol=filtered_df['Launch Site'], color=filtered_df['Launch Site'], title='Correlation between Payload and Success for ' + selectedSite)
        return fig

# Run the app
if __name__ == '__main__':
    app.run()
