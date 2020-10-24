
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table as dt
import re

# Global variables
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) # [dbc.themes.BOOTSTRAP]
project_name = None


def load_data():

  #the variable inside a function is local by default. 
  call_dataset_name = "Call_data.csv"
  service_dataset_name = "Service_data.csv"
  device_dataset_name = "Device_data.csv"
  
  
  # We use a global keyword for a variable which is inside a function so that it can be modified.
  global call_data
  call_data = pd.read_csv(call_dataset_name)
  
  
  global service_data
  service_data = pd.read_csv(service_dataset_name)
  
  
  global device_data
  device_data = pd.read_csv(device_dataset_name)

  # [{'label': '2019-06-20', 'value': '2019-06-20'} ]
  global start_date_list
  temp_list = sorted(call_data['date'].dropna().unique().tolist())
  start_date_list = [{"label": str(i), "value": str(i)}  for i in temp_list ]

  # [{'label': '2019-06-20', 'value': '2019-06-20'} ]
  global end_date_list
  end_date_list = start_date_list

  
  # [{'label': 'Hourly', 'value': 'Hourly'} ]
  temp_list = ["Hourly", "Daywise", "Weekly"]
  global report_type
  report_type = [{"label": str(i), "value":str(i)} for i in temp_list ]
 
def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')

# Layout of your page
def create_app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div([
    
    html.H1('CDR Analysis with Insights', id='Main_title'),
    
    dcc.Tabs(id="Tabs", value="tab-1",children=[
    dcc.Tab(label="Call Analytics tool" ,id="Call Analytics tool",value="tab-1", children = [
    html.Br(),
    html.Br(),
    
    dcc.Dropdown(
          id='start-date-dropdown', 
          options=start_date_list,
          placeholder = "Select Starting Date here",
          value = "2019-06-20"
    ),
            
    dcc.Dropdown(
           id='end-date-dropdown', 
                  options=end_date_list,
                  placeholder = "Select Ending Date here",
                  value = "2019-06-25"
    ),
            
            
    dcc.Dropdown(
                  id='group-dropdown', 
                  placeholder = "Select group here",
                  multi = True
    ),
            
            
    dcc.Dropdown(
                  id='Report-type-dropdown', 
                  options=report_type,
                  placeholder = "Select Report Type",
                  value = "Hourly"
    )]),
    dcc.Tab(label = "Device Analytics tool", id="Device Analytics tool", value="tab-2", children = [            
    html.Br(),
    dcc.Dropdown(
      id='device-date-dropdown', 
      options=start_date_list,
      placeholder = "Select Date here",
      multi = True
        ), 
    html.Br()]),
  
    dcc.Tab(label = "Service Analytics tool", id="Service Analytics tool", value="tab-3", children = [            
    html.Br(),
    dcc.Dropdown(
      id='service-date-dropdown', 
      options=start_date_list,
      placeholder = "Select Date here",
      multi = True
        ), 
    html.Br()])
    ]),
    html.Br(),
    dcc.Loading(html.Div(id='visualization-object',children='Graph,Card, Table')),
    
    ])

    return main_layout



def create_card(title, content, color):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.Br(),
                html.Br(),
                html.H2(content, className="card-subtitle"),
                html.Br(),
                ]
        ),
        color=color, inverse=True
    )
    return(card)


def count_devices(data):
    
    # Various devices used for VoIP calls
    device_dict = {"Polycom" :0,
    "Windows" : 0,
    "iphone" : 0,
    "Android" : 0,
    "Mac" : 0,
    "Yealink" : 0,
    "Aastra" : 0,
    "Others" : 0}
    
    
    
    reformed_data = data["UserDeviceType"].dropna().reset_index()
    for var in reformed_data["UserDeviceType"]:
        if re.search("Polycom", var) :
            device_dict["Polycom"]+=1
        elif re.search("Yealink", var):
            device_dict["Yealink"]+=1
        elif re.search("Aastra", var):
            device_dict["Aastra"]+=1
        
        elif re.search("Windows", var):
            device_dict["Windows"]+=1
        elif re.search("iPhone|iOS", var):
            device_dict["iphone"]+=1
        elif re.search("Mac", var):
            device_dict["Mac"]+=1
        elif re.search("Android", var):
            device_dict["Android"]+=1
            
        else:
            device_dict["Others"]+=1
    final_data = pd.DataFrame()
    final_data["Device"] = device_dict.keys()
    final_data["Count"] = device_dict.values()
    return final_data




# Callback of your page
@app.callback(
    Output('visualization-object', 'children'),
    [
    Input("Tabs", "value"),
    Input('start-date-dropdown', 'value'),
    Input('end-date-dropdown', 'value'),
    Input("group-dropdown", 'value'),
    Input('Report-type-dropdown', 'value'),
    Input('device-date-dropdown', 'value'),
    Input('service-date-dropdown', 'value')
    
    ]
    )


def update_app_ui(Tabs, start_date, end_date, group, report_type,device_date,service_date):
    
    print("Data Type of start_date value = " , str(type(start_date)))
    print("Data of start_date value = " , str(start_date))
    
    print("Data Type of end_date value = " , str(type(end_date)))
    print("Data of end_date value = " , str(end_date))
    
    
    print("Data Type of group value = " , str(type(group)))
    print("Data of group value = " , str(group))
    
    print("Data Type of report_type value = " , str(type(report_type)))
    print("Data of report_type value = " , str(report_type))
    
    print("Data Type of device_date value = " , str(type(device_date)))
    print("Data of device_date value = " , str(device_date))

    print("Data Type of service_date value = " , str(type(service_date)))
    print("Data of service_date value = " , str(service_date))


    if Tabs == "tab-1":
        
        # Filter the data as per the selection of the drop downs
        
        call_analytics_data = call_data[ (call_data["date"]>=start_date) & (call_data["date"]<=end_date) ]
         
        if group  == [] or group is None:
           pass
        else:
           call_analytics_data = call_analytics_data[call_analytics_data["Group"].isin(group)]
         
    
    
        graph_data = call_analytics_data
        # Group the data based on the drop down     
        if report_type == "Hourly":
            graph_data = graph_data.groupby("hourly_range")["Call_Direction"].value_counts().reset_index(name = "count")
            x = "hourly_range"
            
            content = call_analytics_data["hourly_range"].value_counts().idxmax()
            title =  "Busiest Hour"
        
            
        elif report_type == "Daywise":
            graph_data = graph_data.groupby("date")["Call_Direction"].value_counts().reset_index(name = "count")
            x = "date"
            
            content = call_analytics_data["date"].value_counts().idxmax()
            title =  "Busiest Day"
            
        else:
            graph_data = graph_data.groupby("weekly_range")["Call_Direction"].value_counts().reset_index(name = "count")
            x = "weekly_range"
            
            content = call_analytics_data["weekly_range"].value_counts().idxmax()
            title =  "Busiest WeekDay"
            
           
        # Graph Section
        figure = px.area(graph_data, 
                         x = x, 
                         y = "count",
                         color = "Call_Direction",
                         hover_data=[ "Call_Direction", "count"], 
                         template = "plotly_dark")
        figure.update_traces(mode = "lines+markers")
      
      
      
        # Card Section
        total_calls = call_analytics_data["Call_Direction"].count()
        card_1 = create_card("Total Calls",total_calls, "success")
          
        incoming_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Incoming"].count()
        card_2 = create_card("Incoming Calls", incoming_calls, "primary")
          
        outgoing_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Outgoing"].count()
        card_3 = create_card("Outgoing Calls", outgoing_calls, "primary")
          
        missed_calls = call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"] == 19].count()
        card_4 = create_card("Missed Calls", missed_calls, "danger")
          
        max_duration = call_analytics_data["duration"].max()
        card_5 = create_card("Max Duration", f'{max_duration} min', "dark")
        
        card_6 = create_card(title, content, "primary")
             
      
    
        graphRow0 = dbc.Row([dbc.Col(id='card1', children=[card_1], md=3), dbc.Col(id='card2', children=[card_2], md=3)])
        graphRow1 = dbc.Row([dbc.Col(id='card3', children=[card_3], md=3), dbc.Col(id='card4', children=[card_4], md=3)])
        graphRow2 = dbc.Row([dbc.Col(id='card5', children=[card_5], md=3), dbc.Col(id='card6', children=[card_6], md=3)])
     
        cardDiv = html.Div([graphRow0,html.Br(), graphRow1,html.Br(), graphRow2])
        
    
    
    
    
        # Data Table Section
    
        datatable_data = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Call_Direction"].value_counts().unstack(fill_value = 0).reset_index()
        if call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"]==19].count()!=0:
            datatable_data["Missed Calls"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Missed Calls"].value_counts().unstack()[19]
        else:
            datatable_data["Missed Calls"] = 0
            
        datatable_data["Total_call_duration"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["duration"].sum().tolist()
        
      
    
        datatable = dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in datatable_data.columns],
        data=datatable_data.to_dict('records'),
        page_current=0,
        page_size=5,
        page_action='native',
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
        )
        
            
        return [
                dcc.Graph(figure = figure), 
                html.Br() ,
                cardDiv, 
                html.Br(),
                datatable
               ]
    
    elif Tabs == "tab-2":
        if device_date is None or device_date == []: 
            device_analytics_data = count_devices(device_data)
        else:
            device_analytics_data = count_devices(device_data[device_data["DeviceEventDate"].isin(device_date)])
          
        fig = px.pie(device_analytics_data, names = "Device", values = "Count", color = "Device", hole = .3)
        fig.update_layout(autosize=True,
                          margin=dict(l=0, r=0, t=25, b=20),
                          )
        return dcc.Graph(figure = fig)
    
    
    
    
    elif Tabs == "tab-3":
        if service_date is None or service_date == []:
            service_analytics_data = service_data["FeatureName"].value_counts().reset_index(name = "Count")
        else:
            service_analytics_data = service_data["FeatureName"][service_data["FeatureEventDate"].isin(service_date)].value_counts().reset_index(name = "Count")
        fig = px.pie(service_analytics_data, names = "index", values = "Count",color = "index")
        
        fig.update_layout(autosize=True,
                          margin=dict(l=0, r=0, t=25, b=20),
                          )
        return dcc.Graph(figure = fig)
    
    else:
        return None
    
    
@app.callback(
    Output("group-dropdown", "options"),
    [
    Input('start-date-dropdown', 'value'),
    Input('end-date-dropdown', 'value')
    ]
    )
def update_groups(start_date, end_date): 
    reformed_data = call_data[(call_data["date"]>=start_date) & (call_data["date"]<=end_date)]
    group_list = reformed_data["Group"].unique().tolist()
    group_list = [{"label":m, "value":m} for m in group_list]
    return group_list



# Flow of your Project
def main():
    load_data()
    
    open_browser()
    
    global app, project_name
    project_name = "CDR Analysis with Insights"
    app.layout = create_app_ui()
    app.title = project_name

    
    # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
    app.run_server() # debug=True
    
    
    print("This would be executed only after the script is closed")
    
    app = None
    project_name = None
    
    global call_data,service_data,start_date_list,end_date_list,report_type
    call_data = None
    service_data = None
    start_date_list = None
    end_date_list = None
    report_type = None  
    
    

if __name__ == '__main__':
    main()




