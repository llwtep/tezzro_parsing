import json
import pandas as pd
import plotly.graph_objects as go

with open('tezzro_jsons/predictions.json') as file:
    predictions = json.load(file)

with open('tezzro_jsons/evaluations_with_order_cart.json') as file:
    eval_cart = json.load(file)
with open('tezzro_jsons/evaluations_with_lod2_transactions.json') as file:
    eval_lod = json.load(file)

list_orders = []
for i in range(0, 100):
    list_orders.append(eval_cart[i])

df = pd.DataFrame(list_orders)
df['order_time'] = pd.to_datetime(df['order_time'], format='ISO8601', utc=True)

fig = go.Figure()

df['order_text'] = df.apply(lambda
                                row: f'Order ID:{row["order_id"]}<br>Positive count:{row["true_positives_count"]}<br>False positive count:{row["false_positives_count"]}<br>False negative count:{row["false_positives_count"]}',
                            axis=1)

fig.add_trace(go.Scatter(
    x=df['order_time'],
    y=df['f1_score'],
    mode='lines+markers',
    text=df['order_text'],
    hoverinfo='text',
))

fig.update_layout(
    title="Score vs Time",
    xaxis_title="Time",
    yaxis_title="Score",
    template="plotly_dark",
    hovermode='closest',
)

fig.show()
