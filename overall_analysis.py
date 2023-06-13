import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go



def perform_overall_analysis(df):
    st.title('Overall Analysis')

    # Total invested amount
    total_invested = round(df['amount_inr'].sum(), 2)

    # Maximum amount infused in a startup
    max_funding = round(df.groupby('startup_name')[
                        'amount_inr'].max().max(), 2)

    # Average ticket size
    avg_funding = round(df['amount_inr'].mean(), 2)

    # Total funded startups
    total_startups = df['startup_name'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label='Total Invested Amount (in Cr)', value=total_invested)
    with col2:
        st.metric(label='Maximum Funding in a Startup (in Cr)',
                  value=max_funding)
    with col3:
        st.metric(label='Average Ticket Size (in Cr)', value=avg_funding)
    with col4:
        st.metric(label='Total Funded Startups', value=total_startups)

    # ---------------- Graphs------------------ #

    # Number of fundings over the years
    st.header('Trend in Funding')

    # Line plot for number of fundings by year
    fundings_by_year = df['year'].value_counts().sort_index()
    fig_num_fundings = go.Figure(data=go.Scatter(
        x=fundings_by_year.index, y=fundings_by_year.values))
    fig_num_fundings.update_layout(
        title='Number of Fundings Over the Years',
        xaxis_title='Year',
        yaxis_title='Number of Fundings'
    )

    # Line plot for amount of funding by year
    df_year = df.groupby('year', as_index=False)['amount_inr'].sum()
    fig_funding_amount = go.Figure(data=go.Scatter(
        x=df_year.year, y=df_year.amount_inr))
    fig_funding_amount.update_layout(
        title='Amount of Funding Over the Years',
        xaxis_title='Year',
        yaxis_title='Amount of Funding (in crore INR)'
    )

    st.plotly_chart(fig_num_fundings, use_container_width=True)
    st.plotly_chart(fig_funding_amount, use_container_width=True)

    # Biggest Investor in India
    st.header('Biggest Investors in India')
    filtered_investors = df[df['investor_name'] != 'Undisclosed investors']
    investors = filtered_investors['investor_name'].value_counts().head(
        10).reset_index()
    investors.columns = ['Investor Name', 'Number of Fundings Made']

    fig = px.bar(investors, x='Investor Name', y='Number of Fundings Made',
                 labels={'Number of Fundings Made': 'Number of Fundings Made'},
                 )

    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title='Investor Name',
        yaxis_title='Number of Fundings Made',
        height=500
    )

    st.plotly_chart(fig)

    # Do cities play a major role in funding ?

    st.header('Distribution of startups across Top 10 Cities')
    city_filtered = df[df['city_location'].notnull()]
    count = city_filtered['city_location'].value_counts().head(
        10).reset_index()
    count.columns = ['City', 'Count']

    fig = px.treemap(count, path=['City'], values='Count',
                     color='City', color_continuous_scale='viridis',
                     labels={'Count': 'Number of Startups'})

    fig.update_layout(height=600)

    fig.data[0].textinfo = 'label+text+value'
    fig.update_traces(textfont=dict(size=22, color='Black'))

    st.plotly_chart(fig, use_container_width=True)
