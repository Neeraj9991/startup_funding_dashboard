import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from wordcloud import WordCloud, STOPWORDS


def load_startup_details(df):

    # 'Funding Amount vs Number of Fundings'
    st.subheader('Funding Amount vs Number of Fundings')

    startup_data = df['startup_name'].value_counts().reset_index()
    startup_data.columns = ['startup_name', 'number_of_fundings']

    # Group by startup name and calculate the total funding amount
    funding_amount = df.groupby('startup_name')[
        'amount_inr'].sum().reset_index()

    # Merge the funding_amount DataFrame with the startup_data DataFrame
    startup_data = pd.merge(startup_data, funding_amount, on='startup_name')

    startup_data.sort_values(by='amount_inr', ascending=False, inplace=True)

    startup_data['amount_inr'] = startup_data['amount_inr'] / 100

    fig = px.scatter(startup_data, x='number_of_fundings', y='amount_inr', size='amount_inr', hover_name='startup_name',
                     labels={'number_of_fundings': 'Number of Fundings',
                             'amount_inr': 'Funding Amount (in crore INR)'})

    # Format the funding amount labels
    fig.update_traces(
        texttemplate='%{text:.2s} cr INR', textposition='top center')

    fig.update_layout(
        showlegend=False,
        xaxis=dict(title=dict(standoff=10)),
        yaxis=dict(title=dict(standoff=10)),
        height=600,
        hoverlabel=dict(font=dict(size=10)),
        width=900
    )

    st.plotly_chart(fig)

    # Industry Favored by Investors
    st.header('Industry Favored by Investors')

    vertical_filtered = df[df['industry_vertical'].notnull()]
    industry_vertical_counts = vertical_filtered['industry_vertical'].value_counts(
    ).head(10)

    # Calculate the total funding amount by industry vertical
    industry_vertical_amount = df.groupby('industry_vertical')[
        'amount_inr'].sum().nlargest(10)

    # Create the figure and axes for the subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Bar plot for industry vertical counts
    sns.barplot(x=industry_vertical_counts.values,
                y=industry_vertical_counts.index, ax=ax1, alpha=0.9)
    ax1.set_xlabel('Number of Fundings Made', fontsize=12)
    ax1.set_ylabel('Industry Vertical of Startups', fontsize=12)
    ax1.set_title('Top 10 Industries by Count', fontsize=14)

    # Bar plot for industry vertical funding amounts
    sns.barplot(x=industry_vertical_amount.values,
                y=industry_vertical_amount.index, ax=ax2, alpha=0.9)
    ax2.set_xlabel('Funding Amount (in crore INR)', fontsize=12)
    ax2.set_ylabel('Industry Vertical of Startups', fontsize=12)
    ax2.set_title('Top 10 Industries by Funding Amount', fontsize=14)

    plt.tight_layout()

    st.pyplot(fig)

    # Word Cloud
    st.header('Startups in India')

    names = df['startup_name'][~pd.isnull(df['startup_name'])]
    word_frequencies = names.value_counts().to_dict()

    additional_stopwords = {"Pvt", "Ltd", "Limited", "Private"}

    stopwords = set(STOPWORDS).union(additional_stopwords)

    wordcloud = WordCloud(
        max_font_size=50,
        width=800,
        height=400,
        background_color='rgb(0,0,0)',
        relative_scaling=0.5,
        stopwords=stopwords
    )
    wordcloud.generate_from_frequencies(word_frequencies)

    fig = plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    st.pyplot(fig)
