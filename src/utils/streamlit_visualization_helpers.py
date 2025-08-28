import streamlit as st
import plotly.graph_objects as go

def create_metric_section(title, value, data_df, chart_columns=None, y_min=None, y_max=None):
    st.write(f"### {title}")
    st.write(value)

    if chart_columns is None:
        chart_columns = list(data_df.columns)
        chart_columns.remove('Timestamp')

    # Create container for parameter selection
    select_container = st.container()
    plot_container = st.empty()

    with select_container:
        selected_param = st.selectbox(f"Select parameter for {title}", chart_columns)

    # Create the chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data_df['Timestamp'],
        y=data_df[selected_param],
        name=selected_param,
        mode='lines'
    ))

    fig.update_layout(
        title=f'{selected_param} Over Time',
        yaxis_title=selected_param,
        xaxis_title='Timestamp',
        width=900,
        height=570
    )

    if y_min is not None and y_max is not None:
        fig.update_yaxes(range=[y_min, y_max])

    st.write(fig)
    st.write(data_df)

def create_interactive_chart(df, title, y_col=None, y_min=None, y_max=None):
    """Create an interactive Plotly chart with parameter selection."""
    # Create containers
    select_container = st.container()
    plot_container = st.empty()

    # Get available parameters
    param_lst = list(df.columns)
    # param_lst.remove('Timestamp')

    # Parameter selection
    with select_container:
        selected_param = y_col if y_col else st.selectbox(f"Select parameter for {title}", param_lst)

    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[selected_param],
        name=selected_param,
        mode='lines'
    ))

    fig.update_layout(
        title=f'{selected_param} Over Time',
        yaxis_title=selected_param,
        xaxis_title='Timestamp',
        width=900,
        height=570
    )

    if y_min is not None and y_max is not None:
        fig.update_yaxes(range=[y_min, y_max])

    st.write(fig)
    st.write(df)