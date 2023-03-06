
'''
Dashboard

JASKIRAT KAUR

File for subsisiary functions for dash

Run the app with `python3 app.py` and visit
http://127.0.0.1:8050/ in your web browser.
'''

import pandas as pd

def add_state_column(df):
    """
    Given a column of State FIPs, this function adds another column 
    for the state name corresponding to the FIP
    
    Jaskirat
    
    """
    fip_to_state = {
    '01': 'Alabama','02': 'Alaska','04': 'Arizona','05': 'Arkansas','06': 'California',
    '08': 'Colorado','09': 'Connecticut','10': 'Delaware','11': 'District of Columbia','12': 'Florida',
    '13': 'Georgia','15': 'Hawaii','16': 'Idaho','17': 'Illinois','18': 'Indiana','19': 'Iowa','20': 'Kansas',
    '21': 'Kentucky','22': 'Louisiana','23': 'Maine','24': 'Maryland','25': 'Massachusetts','26': 'Michigan',
    '27': 'Minnesota','28': 'Mississippi','29': 'Missouri','30': 'Montana','31': 'Nebraska','32': 'Nevada',
    '33': 'New Hampshire','34': 'New Jersey','35': 'New Mexico','36': 'New York','37': 'North Carolina',
    '38': 'North Dakota','39': 'Ohio','40': 'Oklahoma','41': 'Oregon','42': 'Pennsylvania','44': 'Rhode Island',
    '45': 'South Carolina','46': 'South Dakota','47': 'Tennessee','48': 'Texas','49': 'Utah','50': 'Vermont',
    '51': 'Virginia','53': 'Washington','54': 'West Virginia','55': 'Wisconsin','56': 'Wyoming'
    }
    
    df = df.dropna()
    df['state_FIP'] = df['state_FIP'].astype(str).str.zfill(2)
    df['state_name'] = df['state_FIP'].map(fip_to_state)
    
    return df

def extract_year_month(dataframe):
    cols = ['declarationTitle', 'declarationDate', 'Avg_Sentiment_Before', 'Avg_Sentiment_After']
    df_plt = dataframe.loc[:, cols]
    df = df_plt.sort_values(by="declarationDate", ascending=True)
    df['Year_Month'] = df['declarationDate'].apply(lambda x: x[:7])
    
    return df
