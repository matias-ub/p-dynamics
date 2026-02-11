"""Radar chart component for displaying test results."""
import reflex as rx
import plotly.graph_objects as go


def radar_chart(alignment: float, empathy: float, health: float) -> rx.Component:
    """Create a radar chart to visualize the three scores."""
    
    categories = ['Alineación', 'Empatía', 'Salud Relacional']
    values = [alignment, empathy, health]
    
    # Create radar chart using plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Scores',
        line=dict(color='rgb(99, 110, 250)', width=2),
        fillcolor='rgba(99, 110, 250, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%',
                tickfont=dict(size=12),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='black')
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return rx.box(
        rx.plotly(data=fig),
        width="100%",
        max_width="600px",
        margin="0 auto"
    )
