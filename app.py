import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')

sheet_id = '1wNYvg_8BZUnhE2_-sU9zVUrYKremrt5yAlh04QRUsi4'
df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df.groupby(['year', 'month'])['startup'].count().reset_index()


def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())

    # maximum amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max(
    ).sort_values(ascending=False).head(1).values[0]

    # Average ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    # Total funded startups
    total_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total Amount ', str(total) + ' Cr')
    with col2:
        st.metric('Maximum Funding ', str(max_funding) + ' Cr')
    with col3:
        st.metric('Average Ticket Size ', str(avg_funding) + ' Cr')
    with col4:
        st.metric('Total Startups', str(total_startups))

    # Month on Month Graph
    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype(
        'str') + '-' + temp_df['year'].astype('str')

    fig, ax = plt.subplots()
    ax.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig)


def load_investor_details(investor):
    st.title(investor)

    # load recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head(
    )[['date', 'startup', 'vertical', 'city', 'round', 'amount']]

    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    # biggest investments
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investment')
        big_series = df[df['investors'].str.contains(investor)].groupby(
            'startup')['amount'].sum().sort_values(ascending=False).head()

        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    # Year on Year Investments
    with col2:
        st.subheader('YoY Investment')
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')[
            'amount'].sum()
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)

        st.pyplot(fig4)

    st.subheader('Investment in : ')
    pie_col1, pie_col2, pie_col3 = st.columns(3)
    with pie_col1:
        vertical_series = df[df['investors'].str.contains(
            investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors')

        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)

    with pie_col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('round')[
            'amount'].sum()
        st.subheader('Stage')

        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")

        st.pyplot(fig2)

    with pie_col3:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('city')[
            'amount'].sum()
        st.subheader('City')

        fig3, ax3 = plt.subplots()
        ax3.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")

        st.pyplot(fig3)


st.title('Startup Funding Analysis')

st.sidebar.subheader('Select One')
option = st.sidebar.selectbox("", ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup', sorted(
        df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup details')
else:
    selected_investor = st.sidebar.selectbox(
        'Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor details')
    if btn2:
        load_investor_details(selected_investor)
