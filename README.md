[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9908682&assignment_repo_type=AssignmentRepo)

# Hot or Not: 
## Climate Change Anlaysis on Twitter Data with Disaster Events

## Description
Even though the more extreme weather events have been happening more frequently globally, there is still a portion of the population who are unaware that their lives are being impacted by climate change or are ignorant of the magnitude and reality of the issue. Thus, we plan to analyze climate change patterns to determine people's sentiments and understanding of climate change. We attempt to correlate people's awareness with the intensity of climate change’s impact in their area of residence. The data set we plan to use is a twitter collections dataset  regarding climate change and human opinions. We need to find additional third party API on extreme weather events to merge with the twitter data . Finally, we need to determine whether to study the U.S or developing countries since it might be easier to do the former depending on what data we can acquire. 

## Getting Started
To get started with the App, follow these steps:

1. Clone the repository: git clone https://github.com/uchicago-capp122-spring23/30122-project-hot-or-not.git
2. Run poetry install to install the necessary packages
3. Run poetry shell to activate the virtual environment
4. Run python -m main to open the dashboard

PS:
Due to the constraint of file size, to access the large dataset when running data_clean.py, click the following google drive to download the twitter dataset:
https://drive.google.com/drive/folders/1PU5ILt9Db1qrmUOgH_0lbAzGOOQovBca?usp=sharing
. Move the generated file called "twitter.csv" into the subdirectory called "sources". You would be able to run the data_clean.py.

## Analysis Map Road
Firstly, we will visualize the average sentiment across the United States from 2009 to 2019 using the Twitter collections dataset. This analysis will help us understand how people's sentiment towards climate change has evolved over time in different parts of the country. 

Secondly, we will create a word cloud for the most frequent words used in tweets related to climate change in 2009 compared to 2019. This analysis will help us understand how the public's vocabulary and attention towards climate change have evolved over the past decade. 

Lastly, we plan to conduct a regression analysis on sentiment change using an indicator of weather data. We will merge third-party API data on extreme weather events with the Twitter collections dataset to understand the correlation between climate change's impact in an area and people's sentiment towards the issue. We will also need to decide whether to study the U.S or developing countries, depending on the data we can acquire. 

This multi-faceted analysis will help us gain a comprehensive understanding of people's sentiments and awareness towards climate change, which can help inform effective climate change communication strategies.

## Demo on Visulization
#### Word Cloud Comparison
<p align="center">
<img src="/main/images/wordcloud_Fire_2019.png">
</p>

### Interactive Sentiment Map
<p align="center">
<img src= "./main/images/map_demo.png">
</p>

## Authors
Jonathan Juarez

Ridhi Purohit

Jaskirat Kaur

Grey Xu


