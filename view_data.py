import streamlit as st

# Filter the data
def view_data_source(df):
    # Filter options
    filter_vertical = st.selectbox(
        'Filter by Vertical', ['All'] + df['industry_vertical'].unique().tolist())
    filter_round = st.selectbox('Filter by Funding Round', [
                                'All'] + df['investment_type'].unique().tolist())
    filter_city = st.selectbox(
        'Filter by City', ['All'] + df['city_location'].unique().tolist())

    # Apply filters to the DataFrame
    filtered_df = df.copy()
    if filter_vertical != 'All':
        filtered_df = filtered_df[filtered_df['industry_vertical']
                                  == filter_vertical]
    if filter_round != 'All':
        filtered_df = filtered_df[filtered_df['investment_type']
                                  == filter_round]
    if filter_city != 'All':
        filtered_df = filtered_df[filtered_df['city_location'] == filter_city]

    # Display filtered results
    st.dataframe(filtered_df)

