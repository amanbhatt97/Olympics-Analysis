# FOR DISPLAYING RECORDS BASED ON SELECTED ITEM

# for fetching unique countries and unique years
def country_year_list(df):
    # Fetching unique years
    years = df['Year'].unique().tolist()
    # Sorting the years
    years.sort()
    # Inserting a header 'Overall'
    years.insert(0, 'Overall')

    # fetching unique countries
    country = df['region'].dropna().unique().tolist()
    # sorting the country names
    country.sort()
    # Inserting a header 'Overall'
    country.insert(0, 'Overall')

    return years, country


# for displaying medal_tally country and year wise
def fetch_medal_tally(df, year, country):
    flag = 0  # To print year wise Overall record for case 2
    medal_df = df.drop_duplicates(subset=['NOC', 'Year', 'Season', 'Event', 'Medal'])

    # CASE 1
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    # CASE 2
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    # CASE 3
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]

    # CASE 4
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]

    if flag == 1:
        # Group all records by year
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        # Group all records by gold, silver and bronze
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()

    # Make a column for total medals
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # converting medals data into integers
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


# function to form table between year and number of countries participated
def nations_over_time(df):
    # To find unique countries participating every year
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    # rename columns
    nations_over_time.rename(columns = {'Year': 'Edition', 'count': 'Number of Countries'}, inplace = True)

    return nations_over_time


# function to form table between year and number of countries participated
def events_over_time(df):
    # To find unique countries participating every year
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
    # rename columns
    events_over_time.rename(columns = {'Year': 'Edition', 'count': 'Number of Events'}, inplace = True)

    return events_over_time


# function to form table between year and number of athletes participated
def athletes_over_time(df):
    # To find unique athletes participating every year
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year')
    # rename columns
    athletes_over_time.rename(columns = {'Year': 'Edition', 'Year': 'Number of Athletes'}, inplace = True)

    return athletes_over_time


# function to find most successful athlete in each sport
def most_successful_by_sport(df, sport):
    # remove rows where medal is null
    temp_df = df.dropna(subset = 'Medal')

    # filter results when any sport is selected
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # count name and merge with df to find 'Sports' and 'region' then drop duplicates on 'index'
    x = temp_df['Name'].value_counts().reset_index().merge(df, on = 'Name', how = 'left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name').head(10)
    
    # rename columns
    x.rename(columns = {'count': 'Medals'}, inplace = True)
    
    return x


# function to find most successful athlete country-wise
def most_successful_by_country(df, country):
    # remove rows where medal is null
    temp_df = df.dropna(subset = 'Medal')

    # filter results when any sport is selected
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]
    
    # count name and merge with df to find 'Sports' and 'region' then drop duplicates on 'index'
    x = temp_df['Name'].value_counts().reset_index().merge(df, on = 'Name', how = 'left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name').head(10)
    
    # rename columns
    x.rename(columns = {'count': 'Medals'}, inplace = True)
    
    return x


# function to find year-wise medal tally of countries
def year_wise_medal_tally(df, country):
    # Select only players that have won medals i.e., dropping null values for medals
    temp_df = df.dropna(subset='Medal')
    # Consider 1 medal for each event for events that include teams
    temp_df.drop_duplicates(subset=['NOC', 'Year', 'Season', 'Event', 'Medal'], inplace=True)
    # fetching for selected country
    new_df = temp_df[temp_df['region'] == country]
    # group by 'year' and count medals
    x = new_df.groupby('Year').count()['Medal'].reset_index()
    final_df = x.rename(columns = {'Medal': 'Medals'})

    return final_df


# function to find country-wise sport medal_tally
def country_event_heatmap(df, country):
    # Select only players that have won medals i.e., dropping null values for medals
    temp_df = df.dropna(subset='Medal')
    # Consider 1 medal for each event for events that include teams
    temp_df.drop_duplicates(subset=['NOC', 'Year', 'Season', 'Event', 'Medal'], inplace=True)
    # fetching for selected country
    new_df = temp_df[temp_df['region'] == country]
    # creating a pivot table
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# function to display most successful athletes country-wise
def most_successful_countrywise(df, country):
    # Select only players that have won medals i.e., dropping null values for medals
    temp_df = df.dropna(subset=['Medal'])
    # fetching for selected country
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x