import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Function to load and display investor details
def load_investor_details(df, investor):
    # Filter out rows with None values and empty rows
    df = df.dropna(subset=['amount_inr'])
    df = df[df['amount_inr'] != 0]

    st.title(investor)

    st.subheader('Most Recent Investments')

    # Load recent 5 investments of the investor
    last5_df = df[df['investor_name'].str.contains(investor)].head(
        5)[['date', 'startup_name', 'industry_vertical', 'city_location', 'investment_type', 'amount_inr']]
    st.dataframe(last5_df)

    # Biggest investments
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investment')
        big_series = df[df['investor_name'].str.contains(investor)].groupby(
            'startup_name')['amount_inr'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(big_series.index, big_series.values, color='steelblue')
        ax.set_xlabel('Investment Amount (in crore INR)')
        ax.set_ylabel('Startup Name')
        ax.set_title('Top 5 Biggest Investments')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig)

    # Year on Year Investments
    with col2:
        st.subheader('YoY Investment')
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        year_series = df[df['investor_name'].str.contains(investor)].groupby('year')[
            'amount_inr'].sum()
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(year_series.index, year_series.values,
                 marker='o', linestyle='-', color='steelblue')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Total Investment Amount (in crore INR)')
        ax4.set_title('Year-on-Year Investments')
        ax4.grid(axis='both', linestyle='--', alpha=0.5)
        st.pyplot(fig4)

    try:
        st.subheader('Investment by Category')
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        # Sectors
        vertical_series = df[df['investor_name'].str.contains(investor)].groupby(
            'industry_vertical')['amount_inr'].sum().nlargest(3)
        ax1.pie(vertical_series, labels=vertical_series.index,
                autopct="%0.01f%%", colors=['#ff9999', '#66b3ff', '#99ff99'])
        ax1.set_title('Investment by Industry Vertical')

        # Stages
        stage_series = df[df['investor_name'].str.contains(investor)].groupby(
            'investment_type')['amount_inr'].sum().nlargest(3)
        ax2.pie(stage_series, labels=stage_series.index,
                autopct="%0.01f%%", colors=['#ffcc99', '#c2c2f0', '#ffb3e6'])
        ax2.set_title('Investment by Investment Type')

        # Cities
        city_series = df[df['investor_name'].str.contains(investor)].groupby(
            'city_location')['amount_inr'].sum().nlargest(3)
        ax3.pie(city_series, labels=city_series.index,
                autopct="%0.01f%%", colors=['#99ff99', '#ffcc99', '#c2c2f0'])
        ax3.set_title('Investment by City Location')

        plt.tight_layout()
        st.pyplot(fig)

    except:
        pass
