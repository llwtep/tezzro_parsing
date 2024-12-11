import plotly.graph_objects as go
import pandas as pd

# Пример данных
data = {
    'order_id': [1, 2, 3, 4, 5],
    'sku_base_id': ['A101', 'A102', 'A103', 'A104', 'A105'],
    'score': [85, 90, 75, 88, 95],
    'time': ['2024-12-01T12:00:00', '2024-12-01T13:00:00', '2024-12-01T14:00:00', '2024-12-01T15:00:00', '2024-12-01T16:00:00']
}

# Преобразуем данные
df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'])

# Создаем график
fig = go.Figure()

# Добавляем точки на график
fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['score'],
    mode='markers',
    text=df.apply(lambda row: f"Order ID: {row['order_id']}<br>SKU Base ID: {row['sku_base_id']}", axis=1),
    hoverinfo='text',  # Всплывающее окно при наведении
))

# Настройки графика
fig.update_layout(
    title="Score vs Time",
    xaxis_title="Time",
    yaxis_title="Score",
    template="plotly_dark",  # Тема
    hovermode='closest',  # Интерактивность при клике
)

# Показать график
fig.show()
