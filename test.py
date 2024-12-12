import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import json
with open('tezzro_jsons/predictions.json') as file:
    predictions = json.load(file)

with open('tezzro_jsons/evaluations_with_order_cart.json') as file:
    eval_cart = json.load(file)
with open('tezzro_jsons/evaluations_with_lod2_transactions.json') as file:
    eval_lod = json.load(file)

list_orders=[order for order in eval_cart]
count = len(list_orders)
total_score=0.0
for i in list_orders:
    total_score+=i['f1_score']

df=pd.DataFrame(list_orders)
df['order_time']=pd.to_datetime(df['order_time'],format='ISO8601', utc=True)
df['date']=df['order_time'].dt.date
df['time']=df['order_time'].dt.date
df['order_status']=df['f1_score'].apply(lambda x: 'Correct' if x == 1 else 'Incorrect')
bar_data=df.groupby("date").size().reset_index(name="orders")

app= dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Order Statistics"),
    dcc.Graph(id='barchart'),  # График с количеством заказов по дням
    dcc.Graph(id='linechart'),# График с деталями для выбранного дня
    dcc.Graph(id='piechart')
])

@app.callback(
    Output('linechart', 'figure'),
    Input('barchart', 'clickData')
)

def update_linechart(clickData):
    if clickData is None:
        return px.line()#return empty graphic
    selected_date=clickData['points'][0]['x']
    filtered_data=df[df['date']==pd.to_datetime(selected_date).date()]
    fig=px.line(filtered_data,x='order_time', y='f1_score',
                title=f'Orders on {selected_date}',
                labels={'order_time': 'Time', 'f1_score': 'Score'},
                markers=True,
                )
    return fig

@app.callback(
    Output('piechart', 'figure'),
    Input('barchart', 'clickData')
)
def update_piechart(clickData):
    if clickData is None:
        pie_data=df.groupby('order_status').size().reset_index(name='count')
        title='Order status distribution(All period)'
    else:
        selected_date = clickData['points'][0]['x']
        filtered_data=df[df['date']==pd.to_datetime(selected_date).date()]
        pie_data=filtered_data.groupby('order_status').size().reset_index(name='count')
        title=f'Order_status distribution on {selected_date}'
    fig=px.pie(
        pie_data, names='order_status', values='count', title=title,
        color='order_status',
        color_discrete_map={'Correct':'green', 'Incorrect':'red'}
    )
    return fig


@app.callback(
    Output('barchart', 'figure'),
    Input('linechart', 'figure')  # Необязательно, если bar chart статичный
)
def update_barchart(_):
    fig = px.bar(bar_data, x='date', y='orders',
                 title='Orders by Day',
                 labels={'date': 'Date', 'orders': 'Number of Orders'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



