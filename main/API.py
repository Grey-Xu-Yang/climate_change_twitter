import requests

# Set the API endpoint and parameters
url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
params = {
    "incidentType": "DR",       # Limit to disasters declared as major disasters
    "state": "US",             # Limit to natural disasters in the United States
    "incidentBeginDate": "2012-02-14T00:00:00.000Z",  # Start date for data retrieval
    "limit": 1000              # Maximum number of records to retrieve
}

# Make the request and print the response
response = requests.get(url, params=params)
print(response.json())
