import dash
from datetime import date
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import yfinance as yf
from dash.dependencies import Input, Output 
from src.data_visualisation import loss_for_client
from src.client import Client





tickers = ['GOOG','FB','AAPL','NFLX']
tickers_map  = {ticker : yf.Ticker(ticker).history(start = '2015-01-01', end = date.today().isoformat()[:10]) for ticker in tickers}



app = dash.Dash(
    "My app",
meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
external_stylesheets=[dbc.themes.LUX],)
app.title = "Almgren and Chriss Optimal Liquidation"

app.layout = html.Div(
children=[

        

        html.Div(
            children=[
                html.H1(
                    children="Optimal Liquidation", 
                    style = {"font-size": "50px","padding-left": "5px","color": "indigo"},
                ),
                html.P(
                    children="Choose your ticker,"
                    " the number of stocks you want to sell,"
                    " the aversion of risk,"
                    " the window of time to sell your stocks.",
                    style ={ "font-size" : "25px" , "padding-left" : "50px"},
                ),
            ],
            style = {'line-height' : '30px' },
        ),

        
    
        
    


        html.Div(
            children=[
                html.Div(children="Ticker", className="menu-title"),
                dcc.Dropdown(
                    id="stock-filter",
                    options=[
                        {"label": stock, "value": stock}
                        for stock in tickers
                    ],
                    value = 'GOOG'

                ),
            ]
        ),

        html.Div(
        children=[
            html.Div(
                children="Date Range",
                className="menu-title"
                ),
            dcc.DatePickerRange(
                id="date-range",
                start_date= '2022-01-01',
                end_date = '2022-01-10',
                



                ),

            ]
        ),

        html.Div(
                children=[
                    html.Div(
                        children="Number of Stocks To Sell",
                        className="menu-title"
                        ),
                    dcc.Input(
                        id="number-of-stocks-choice",
                        type = "number",
                        value = 1000
                        

                        ),

                    ]
                ),

        html.Div(
                children=[
                    html.Div(
                        children="Aversion For risk",
                        className="menu-title"
                        ),
                    dcc.Input(
                        id="risk-choice",
                        type = "number",
                        value = 0.0001


                        ),

                    ]
                ),


        # html.Div(
        #         children=[
        #             html.Div(
        #                 children="Number of Intervals",
        #                 className="menu-title"
        #                 ),
        #             dcc.Input(
        #                 id="N-choice",
        #                 type = "number",
        #                 value = 1,
                        

        #                 ),

        #             ]
        #         ),
    


    html.Div(
    children=[
        html.Div(
            children=dcc.Graph(
                id="price-chart", config={"displayModeBar": False},
            ),

        ),
        html.Div(
            children=dcc.Graph(
                id="volume-chart", config={"displayModeBar": False},
            ),

        ),
        html.Div(
            children=dcc.Graph(
                id="stocks-to-sell", config={"displayModeBar": False},
            ),
        ),
    ],
    className="wrapper",
),

    ]
)




@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure"), Output("stocks-to-sell", "figure")] ,
    
    [
        Input("stock-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("number-of-stocks-choice", "value"),
        Input("risk-choice","value"),
        #Input("N-choice","value")


    ],
)



def update_chart(stock, start_date, end_date,X,lamda):

    yf_ticker = tickers_map[stock]
    filtered_data = yf_ticker[start_date:end_date]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data.index,
                "y": filtered_data["Open"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price Of {} Stocks ".format(stock),
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data.index,
                "y": filtered_data["Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Volume of {} Stocks Sold During The Chosen Period".format(stock),
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },   
    }
    client = Client(stock,start_date,end_date,X,lamda)
    T = client.real_difference_time(start_date,end_date)
    x_values = [i for i in range(1,T+1)]
    y_values = loss_for_client(client,T)[0] 
    

    bars_plot = {
        "data": [
            {
                "x": x_values,
                "y": y_values,
                                
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Number Of {} Stocks To Sell Over Each Period ".format(stock),
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return price_chart_figure, volume_chart_figure , bars_plot


if __name__ == '__main__': 
    app.run_server()

