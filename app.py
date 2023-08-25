# FOR FRONT-END OPERATIONS

# Importing libraries
import streamlit as st
import pandas as pd
# to display plots
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
# for 'Athlete Analysis' graph
import plotly.figure_factory as ff


import os
# get the parent directory path
parent_directory = os.getcwd()

# paths
data_path = os.path.join(parent_directory, 'data')


# Read csv files
df = pd.read_csv(os.path.join(data_path, 'athlete_events.csv'))
region_df = pd.read_csv(os.path.join(data_path, 'noc_regions.csv'))


#----- front-end -----#

# side bar

# 1. Display title in sidebar
st.sidebar.title('Olympics Analysis')
st.sidebar.info("Welcome to the Olympics Analysis dashboard!")
st.sidebar.markdown("---")

# 2. Display user menu in sidebar
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

st.sidebar.markdown("---")

# Importing preprocessor file to form required dataframe
import preprocessor
df = preprocessor.preprocess(df, region_df)

# importing helper file to display records based on option selected
import helper

# If Medal Tally option is selected:
if user_menu == 'Medal Tally':
    # display header as 'Medal Tally' in sidebar
    st.sidebar.header('Medal Tally')

    # fetching years, country list from helper
    years, country = helper.country_year_list(df)
    # display year on sidebar
    selected_year = st.sidebar.selectbox("Select Year", years)
    # display country on sidebar
    selected_country = st.sidebar.selectbox("Select Country", country)

    # call fetch_medal_tally function from helper file
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # to display medal tally based on cases
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    # display medal_tally
    st.table(medal_tally)


# to display overall_analysis
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

# to display line graph between nations and time
    nations_over_time = helper.nations_over_time(df)
    fig = px.line(nations_over_time, x='Edition', y='Number of Countries')
    st.title('Participating Nation over the years')
    st.plotly_chart(fig)

# to display line graph between events and time
    events_over_time = helper.events_over_time(df)
    fig = px.line(events_over_time, x='Edition', y='Number of Events')
    st.title('Events over the years')
    st.plotly_chart(fig)

# to display line graph between athletes and time
    athletes_over_time = helper.athletes_over_time(df)
    fig = px.line(athletes_over_time, x='Edition', y='Number of Athletes')
    st.title('Athletes over the years')
    st.plotly_chart(fig)

# to display number of events in each sport over the years

    # display title
    st.title('Number of Events in each Sport over the years')
    # define figure size
    fig, ax = plt.subplots(figsize=(20, 20))
    # remove duplicate events in each sport in each year
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    # create a pivot table and fill Nan with 0 and convert all values to integer
    x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    # creating heatmap
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    # display figure
    st.pyplot(fig)


# to display most successful athletes
    # display title
    st.title('Most Successful Athletes Based on Sports')

    # creating drop-down to select sport name
    # forming a list of unique sports name
    sports_list = df['Sport'].unique().tolist()
    # sort the list
    sports_list.sort()
    # insert a row at starting for 'Overall'
    sports_list.insert(0, 'Overall')
    # creating drop-down
    selected_sport = st.selectbox('Select a Sport', sports_list)

    # fetching most_successful function from helper
    x = helper.most_successful_by_sport(df, selected_sport)
    # display as table
    st.table(x)


# If 'Country-wise Analysis' option is selected:
if user_menu == 'Country-wise Analysis':
    # display title in sidebar
    st.sidebar.title('Country-Wise Analysis')

    # creating drop-down to select country name
    # forming a list of unique country name
    country_list = df['region'].dropna().unique().tolist()
    # sort alphabetically
    country_list.sort()
    # creating drop-down in sidebar
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # calling 'year_wise_medal_tally' function from 'helper'
    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x = 'Year', y='Medals')
    st.title(selected_country + ' Medal Tally over the years')
    st.plotly_chart(fig)


# to display heatmap of country-wise medal_tally
    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    # define figure size
    fig, ax = plt.subplots(figsize=(20, 20))
    # creating heatmap
    sns.heatmap(pt, annot = True)
    # display figure
    st.pyplot(fig)


# to display most successful athletes country-wise
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)



# If 'Athlete wise Analysis' option is selected:
if user_menu == 'Athlete wise Analysis':
    # Removing duplicate names on each region
    athlete_df = df.drop_duplicates(['Name', 'region'])
    # Graphs for 'Age', 'Gold', 'Silver', 'Bronze'
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    # increase figure size
    fig.update_layout(autosize = False, width = 800, height = 600)
    # display title
    st.title('Distribution of Age')
    # show figure
    st.plotly_chart(fig)


with st.container():
    st.markdown("---")
    st.subheader("About the Dashboard")
    st.markdown("Welcome to the Olympics Analysis Dashboard!")
    st.markdown("This is an interactive and informative platform for visualizing and analyzing Olympic Games data. It provides various functionalities and insights related to different aspects of the Olympics.")
    st.markdown("---")
    st.subheader("Contact Information")
    st.markdown("Feel free to reach out to me if you have any questions or feedback. You can find me on:")
    st.markdown("Mail: [amanbhatt.1997.ab@gmail.com](mailto:amanbhatt.1997.ab@gmail.com)")
    st.markdown("Linkedin: [amanbhatt97](https://www.linkedin.com/in/amanbhatt1997/)")
    st.markdown("Github: [amanbhatt97](https://github.com/amanbhatt97)")
    st.markdown("Checkout my portfolio [here](https://amanbhatt97.github.io/portfolio/).")
    st.markdown("---")
    

