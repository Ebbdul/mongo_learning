import pandas as pd
from pandas import json_normalize

# Sample dictionary with a nested JSON object
data = {
    'id': 1,
    'name': 'John',
    'address': {
        'street': '123 Main St',
        'city': 'Example City',
        'zipcode': '12345'
    }
}

# Use json_normalize to flatten the nested JSON object
df = json_normalize(data, sep='_')

# Print the resulting DataFrame
print(df)