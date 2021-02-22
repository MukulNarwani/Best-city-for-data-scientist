import pandas as pd     #(version 1.0.0)
import plotly as py        #(version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio
import numpy as np
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output




app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.body(html),
        html.Div(html.Button('Refresh',id='button'),style={
                                                     "background-color": 'red'
                                                     }),
        html.Div(dcc.Graph(id='scatter-plot'),style={
                                                     "background-color": 'red'
                                                     }),
    ]
)
@app.callback(
    Output("scatter-plot", "figure"),
    [Input('button','n_clicks')]
)
def makeBarChart(n_clicks):
    df = cleanData(pd.read_excel('DataFiles/data copy.xls'))
    barchart = px.scatter(df,x='Salary',
                         y='Cost Of Living and Rent',
                         hover_data=[df.columns[0]],
                         color_continuous_scale=px.colors.sequential.YlOrRd)
    axes=[]
    #Make the axes a range of the min and the max vals
    for column in df.columns:
        if column != 'Unnamed: 0':
            max_val = math.ceil(pd.to_numeric(df[column]).max()/1000)*1000
            min_val=math.floor(pd.to_numeric(df[column]).min()/1000)*1000
            axes.append([min_val,max_val])
    barchart.update_xaxes(range=axes[1],type='linear',fixedrange=True)
    barchart.update_yaxes(range=axes[0],type='linear',fixedrange=True)
    return barchart

def cleanData(df):
    #Makes a list of rows that need to be filtered out
    bools =[]
    for column in df.columns:
        if column != 'Unnamed: 0': 
            #Clean data: remove errors 
        
            s=df[column]
            filter = s.str.find('Error:').astype(bool).tolist()
            bools.append(filter)
            #Clean data: remove non-numbers
            df[column] =df[column].str.replace(',','')
            df[column] =df[column].str.replace('$','')  
        if column == 'Cost Of Living and Rent':
            df[column] =df[column].str.replace('(','')  
            df[column] =df[column].str.split('+')  
    #Removes the error rows
    bools=np.array(bools)
    combined_filter=np.matrix([fil.all() for fil in np.matrix([*bools]).T]).A1
    df= df[pd.Series(combined_filter)]
    #Adds the Cost of living and the rent
    df['Cost Of Living and Rent'] =[float(cost[0])+float(cost[1]) for cost in df['Cost Of Living and Rent']] 
    return df
if __name__ == "__main__":
    app.run_server(debug=True)