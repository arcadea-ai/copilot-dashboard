# app.py
import streamlit as st
import pandas as pd  
import plotly.express as px
from helper_functions import load_data, aggregate_weekly
from data_downloader import data_downloader

st.set_page_config(page_title="Metrics Dashboard", layout="wide")


def main():
    st.title("Metrics Dashboard")
    
    # Download data with streamlit spinner with cache
    with st.spinner("Downloading data..."):
        data_downloader()
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Failed to load metrics data")
        return
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            df['date'].min()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            df['date'].max()
        )
    
    # Filter data
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Key metrics
    st.subheader("Key Statistics")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    with metrics_col1:
        st.metric("Total Suggestions", filtered_df['suggestions'].sum())
    with metrics_col2:
        st.metric("Average Daily Active Users", 
                 int(filtered_df['active_users'].mean()))
    with metrics_col3:
        st.metric("Total Lines Accepted", filtered_df['lines_accepted'].sum())
    with metrics_col4:
        acceptance_rate = (filtered_df['lines_accepted'].sum() / filtered_df['suggestions'].sum() * 100).round()
        st.metric("Acceptance Rate", f"{acceptance_rate}%")
    
    # Time series plot
    st.subheader("Metrics Over Time")
    
    # Create a container with reduced width
    with st.container():
        col1, col2, col3 = st.columns([1, 6, 1])  # Creates side margins
        with col2:
            # Add time period selector
            time_period = st.radio("Select Time Period", ["Daily", "Weekly"])
            
            # Calculate metrics and create plot
            plot_df = filtered_df.copy()
            if time_period == "Weekly":
                plot_df = aggregate_weekly(filtered_df)
            else:
                plot_df['acceptance_rate'] = (plot_df['lines_accepted'] / plot_df['suggestions'] * 100).round()
            
            # Create and display chart
            fig = px.bar(plot_df, 
                        x='date',
                        y=['suggestions', 'lines_accepted'],
                        title=f'{time_period} Suggestions vs Accepted Lines',
                        barmode='group',
                        labels={'date': 'Date'})  # Add this line to change x-axis label
            
            fig.add_scatter(x=plot_df['date'], 
                        y=plot_df['acceptance_rate'],
                        name='Acceptance Rate',
                        yaxis='y2',
                        line=dict(color='red'))
            
            fig.update_layout(
                yaxis2=dict(
                    title='  Rate (%)',
                    overlaying='y',
                    side='right',
                    range=[0, 100]
                ),
                yaxis_title=f'{time_period} Count',
                legend_title='Metrics',
                legend=dict(
                    orientation="h",    # horizontal orientation
                    yanchor="bottom",   # anchor point
                    y=-0.3,            # position below plot
                    xanchor="center",   # center horizontally
                    x=0.5              # center position
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        # Data table
        st.subheader("Raw Data")
        st.dataframe(filtered_df)

    with col2:
        # Daily user count plot
        st.subheader("Daily Active Users")
        daily_users = filtered_df.groupby('date')['active_users'].mean()
        
        fig = px.bar(
            x=daily_users.index,
            y=daily_users.values,
            labels={'x': 'Date', 'y': 'Number of Users'}
        )
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Active Users',
            showlegend=False,
            bargap=0.2  # Add some gap between bars
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
