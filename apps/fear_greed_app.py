import streamlit as st

def app():
    st.markdown("<h1 style='text-align: center; color: grey;'>Fear and Greed Index</h1>", unsafe_allow_html=True)

    import plotly.graph_objects as go
    import numpy as np

    # fear_and_greed index for stock market
    # import fear_and_greed
    # index_value = fear_and_greed.get().value

    # fear_and_greed index FOR crypto
    import requests 
    result = requests.get("https://api.alternative.me/fng/?limit=2")
    data = result.json()
    a = data['data']
    index_value = a[0]['value']


    # Plot Settings 

    # // Color
    plot_bgcolor = "black"
    quadrant_colors = [plot_bgcolor, "#f25829", "#f2a529", "#eff229", "#f2a529", "#f25829"] 
    quadrant_text = ["", "<b>Extreme Greed</b>", "<b>Greed</b>", "<b>Neutral</b>", "<b>Fear</b>", "<b>Extreme Fear</b>"]
    n_quadrants = len(quadrant_colors) - 1

    # Values
    current_value = float(index_value)
    min_value = 0
    max_value = 100
    hand_length = np.sqrt(2) / 10
    hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

    # Plotting
    fig = go.Figure(
        data=[
            go.Pie(
                values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                rotation=90,
                hole=0.5,
                marker_colors=quadrant_colors,
                text=quadrant_text,
                textinfo="text",
                hoverinfo="skip",
                textfont_size = 20
            ),
        ],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=0,t=50,l=10,r=10),
            width=750,
            height=750,
            paper_bgcolor=plot_bgcolor,
            annotations=[
                go.layout.Annotation(
                    text=f"<b>Current Value:</b><br>{current_value}",
                    font_size=25,
                    x=0.5, xanchor="center", xref="paper",
                    y=0.35, yanchor="bottom", yref="paper",
                    showarrow=False,
                )
            ],
            shapes=[
                go.layout.Shape(
                    type="circle",
                    x0=0.49, x1=0.51,
                    y0=0.49, y1=0.51,
                    fillcolor="white",
                    line_color="white",
                ),
                go.layout.Shape(
                    type="line",
                    x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                    y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                    line=dict(color="white", width=4)
                )
            ]
        )
    )


    st.plotly_chart(fig, use_container_width=True)
    link = '[Fear and Greed index explanation](https://www.cnn.com/markets/fear-and-greed#:~:text=FEAR%20%26%20GREED%20INDEX%20FAQs&text=The%20Fear%20%26%20Greed%20Index%20is,to%20have%20the%20opposite%20effect.)'
    st.markdown(link, unsafe_allow_html=True)