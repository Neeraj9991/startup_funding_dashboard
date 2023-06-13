import streamlit as st
import pandas as pd

from overall_analysis import perform_overall_analysis
from view_data import view_data_source
from startup_details import load_startup_details
from investor_details import load_investor_details

st.set_page_config(layout='wide', page_title='Startup Analysis')


def main():
    # Set app title
    st.title('Startup Funding Analysis')

    # Load dataset

    sheet_id = '1FUyALR6neIABaSoc4nx6g1e10F8i_4T4cYOqf8mYcrc'
    df = pd.read_csv(
        f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

    if df is not None:
        # Filter out investors with null values
        df = df.dropna(subset=['investor_name'])

        # Sidebar options
        st.sidebar.subheader('Select Option')
        option = st.sidebar.selectbox(
            "", ['Overall Analysis', 'Startup', 'Investor', 'View Data Source'])

        if option == 'Overall Analysis':
            perform_overall_analysis(df)

        elif option == 'View Data Source':
            st.title("Data Source")
            view_data_source(df)

        elif option == 'Startup':
            load_startup_details(df)

        else:
            investor = st.sidebar.selectbox('Select Investor', sorted(
                set(df['investor_name'].str.split(',').sum())))
            btn2 = st.sidebar.button('Find Investor Details')
            if btn2:
                load_investor_details(df, investor)


if __name__ == '__main__':
    main()
