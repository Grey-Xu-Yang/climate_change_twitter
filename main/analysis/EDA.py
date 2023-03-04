import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

### Part 1. EDA of Twitter Dataset
## Part 1.1 Summary Statistics
US_twitter_EDA = pd.read_csv("/content/drive/MyDrive/CS2_Project/twitter_archive/US_twitter.csv")
# Convert Categorical value to numerical value
US_twitter_EDA.loc[US_twitter_EDA['stance'] == "believer", 'stance'] = 1
US_twitter_EDA.loc[US_twitter_EDA['stance'] == "neutral", 'stance'] = 0
US_twitter_EDA.loc[US_twitter_EDA['stance'] == "denier", 'stance'] = -1
US_twitter_EDA.loc[US_twitter_EDA['aggressiveness'] == "not aggressive", 'aggressiveness'] = 0
US_twitter_EDA.loc[US_twitter_EDA['aggressiveness'] == "aggressive", 'aggressiveness'] = 1
US_twitter_EDA.loc[US_twitter_EDA['gender'] == "male", 'gender'] = 1
US_twitter_EDA.loc[US_twitter_EDA['gender'] == "female", 'gender'] = 0
US_twitter_EDA.loc[US_twitter_EDA['gender'] == "undefined", 'gender'] = 0

US_twitter_EDA['stance'] = US_twitter_EDA['stance'].astype(int)
US_twitter_EDA['aggressiveness'] = US_twitter_EDA['aggressiveness'].astype(int)
US_twitter_EDA['gender'] = US_twitter_EDA['gender'].astype(int)
# create a summary table using value_counts() for categorical variables
summary_num = US_twitter_EDA.describe()
# create a new dataframe with the summary statistics
summary_df = pd.DataFrame({'Variable': summary_num.columns,
                           'Count': summary_num.loc['count'].values,
                           'Mean': summary_num.loc['mean'].values,
                           'Std': summary_num.loc['std'].values,
                           'Min': summary_num.loc['min'].values,
                           '25%': summary_num.loc['25%'].values,
                           '50%': summary_num.loc['50%'].values,
                           '75%': summary_num.loc['75%'].values,
                           'Max': summary_num.loc['max'].values})

# add the summary statistics for categorical variables to the new dataframe
summary_df.iloc[3:-1,:].reset_index(drop=True)

## Part 1.2 Barchart on 10 highest state who tweets relvant information on Climate change
state_counts = US_twitter_EDA["state_name"].value_counts()
top_10_states = state_counts[:10]
# convert the index of the top 10 states series to a list
top_10_states_names = top_10_states.index.tolist()
top_10 = pd.DataFrame({'count': top_10_states.tolist()} , index=top_10_states_names)
# Draw the Graph
plt.figure(figsize=(13, 8))
sns.barplot(x=top_10.index, y='count', data=top_10, palette='viridis')
plt.xlabel('State')
plt.ylabel('Twitter Count')
plt.title("10 highest states who tweets relevant information on Climate Change")
plt.show()

## Part 1.3 Lineplot on number of tweets per year on Climate Change
year_counts = US_twitter_EDA["year"].value_counts()
# convert the index of the top 10 states series to a list
year_labels = year_counts.index.tolist()
year_twitter = pd.DataFrame({'count': year_counts.tolist()} , index=year_labels)
marker_style = dict(marker='o', markersize=8, linestyle='--')
# Draw the plot
plt.figure(figsize=(12, 8))
sns.lineplot(x=year_twitter.index, y = 'count', data=year_twitter, markers = True, **marker_style)
plt.xlabel('Year')
plt.ylabel('Twitter Count')
plt.title("Number of tweets per year on Climate Change")
plt.show()

### Part 2. EDA on FEMA Dataset
## Part 2.1 Diaster Type from 2006 to 2022 in FEMA dataset
df_disasters = pd.read_csv('/content/drive/My Drive/CS2_Project/twitter_archive/FEMA_disaster.csv')
disaster_counts = df_disasters['incidentType'].value_counts()
# convert the index of the top 10 states series to a list
disaster_names = disaster_counts.index.tolist()
disaster_EDA = pd.DataFrame({'count': disaster_counts.tolist()} , index=disaster_names)
plt.figure(figsize=(13, 8))
sns.barplot(x=disaster_EDA.index, y='count', data=disaster_EDA , palette='viridis')
plt.xlabel('Diaster Type')
plt.ylabel('Diaster Count')
plt.title("Diaster Type from 2006 to 2022 in FEMA dataset")
plt.show()

## Part 2.2 Diaster Count from 2006 to 2022 in FEMA dataset
df_disasters['year'] = pd.to_datetime(df_disasters['declarationDate']).dt.year
disaster_counts = df_disasters['year'][df_disasters['year'] > 2005].value_counts()
# convert the index of the top 10 states series to a list
disaster_names = disaster_counts.index.tolist()
disaster_EDA = pd.DataFrame({'count': disaster_counts.tolist()} , index=disaster_names)
marker_style = dict(marker='o', markersize=8, linestyle='--')
plt.figure(figsize=(12, 8))
sns.lineplot(x=disaster_EDA.index, y='count',data=disaster_EDA, markers = True, **marker_style)
plt.xlabel('Year')
plt.ylabel('Diaster Count')
plt.title("Diaster Count from 2006 to 2022 in FEMA dataset")
plt.show()

### Part 3. EDA on Merged Data
# In this case, we take the average of merging since we convert categorical to numerical variables.
# Group data by date and county
grouped_df2_EDA = US_twitter_EDA.groupby(['date', 'state_FIP'])

# Define the aggregation functions for categorical and numerical variables
# For categorical value, take the most frequently occured type, for the numerical value, take the average
agg_dict2_EDA = {'topic': lambda x: x.value_counts().index[0], 
            'stance': 'mean', 
            'gender': 'mean', 
            'aggressiveness': 'mean', 
            'state_name': lambda x: x.iloc[0],
            'temperature_avg': 'mean',
            'sentiment': 'mean'}

# Apply the aggregation
result_df2_EDA = grouped_df2_EDA.agg(agg_dict2_EDA)
# Reset the index
result_df2_EDA = result_df2_EDA.reset_index()
# and we don't consider whether the twitter has the same county ID with the FEMA data 
df_disasters['declarationDate'] = pd.to_datetime(df_disasters['declarationDate']).dt.date
df_disasters['incidentBeginDate'] = pd.to_datetime(df_disasters['incidentBeginDate']).dt.date
df_disasters['incidentEndDate'] = pd.to_datetime(df_disasters['incidentEndDate']).dt.date
merged_df2_EDA = pd.merge(df_disasters, result_df2_EDA, left_on='fipsStateCode', right_on = 'state_FIP')
filtered_df2_EDA = merged_df2_EDA[(merged_df2_EDA['date'] >= merged_df2_EDA['incidentBeginDate']) & (merged_df2_EDA['date'] <= merged_df2_EDA['incidentEndDate'])]

## Part 3.1 Boxplot of sentiment by Incident Type in Merged Dataset on FEMA and US Twitter
plt.figure(figsize=(10, 8))
sns.boxplot(x="incidentType", y="sentiment", data=filtered_df2_EDA)
# add labels to the plot
plt.xlabel('Incident Type')
plt.ylabel('Sentiment')
plt.title("Sentiment by Incident Type in Merged Dataset on FEMA and US Twitter")
plt.show()

## Part 3.2 Heatmap of Count by Stance and Incident Type in Merged Dataset
ct = pd.crosstab(filtered_df2_EDA['stance'], filtered_df2_EDA['incidentType'])
plt.figure(figsize=(10, 8))
# create the heatmap using seaborn
sns.heatmap(ct, cmap='Blues', annot=True, fmt='d')
# add labels to the plot
plt.xlabel('Incident Type')
plt.ylabel('Stance')
plt.title("Count by Stance and Incident Type in Merged Dataset")
plt.show()

## Part 3.3 Heatmap of Count by Stance and Incident Type in Merged Dataset
ct = pd.crosstab(filtered_df2_EDA['aggressiveness'], filtered_df2_EDA['incidentType'])
plt.figure(figsize=(10, 8))
# create the heatmap using seaborn
sns.heatmap(ct, cmap='Blues', annot=True, fmt='d')
# add labels to the plot
plt.xlabel('Incident Type')
plt.ylabel('Stance')
plt.title("Count by Aggressiveness and Incident Type in Merged Dataset")
plt.show()

## Part 3.4 Pairplot of Five US twitter features in the merged Dataset
columns = ['stance', 'gender', 'aggressiveness', 'temperature_avg', 'sentiment']
sns.pairplot(filtered_df2_EDA.loc[:, columns], kind = "reg", plot_kws={"scatter_kws": {"s": 5}, "line_kws": {"color": "orange"}})