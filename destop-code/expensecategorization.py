#algorithm to categorize expenses by searching location of transaction on google, parsing the first result, and putting it into a gpt model with a specific prompt to get a keyword back.

import pandas as pd
import requests
from bs4 import BeautifulSoup
import openai
import os

df_transactions = pd.read_csv('/mnt/data/transactions.csv')

card_to_person = {3456: "Rebecca", 4444: "John", 3696: "Adam"}
df_transactions["Person"] = df_transactions["Card_Number"].map(card_to_person)

os.environ['OPENAI'] = 'key'
openai.api_key = os.getenv('OPENAI')

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_bio_from_google(soup):
    bio = ""
    try:
        bio_div = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
        if bio_div:
            bio = bio_div.text
        else:
            bio_span = soup.find('span', class_='BNeawe tAd8D AP7Wnd')
            if bio_span:
                bio = bio_span.text
            else:
                bio = "No bio found"
    except Exception as e:
        bio = "No bio found"
    return bio

def get_category_using_gpt(transaction_statement, location, bio):
    prompt = f"""
    Given the transaction statement "{transaction_statement}" in {location}, and the following business description:
    "{bio}", categorize the transaction into one of the following categories:
    1. Food
    2. Luxury
    3. Furniture
    4. Transportation
    5. Groceries
    6. Utilities
    7. Entertainment
    8. Travel
    9. Clothing
    10. Electronics
    11. Health
    12. Education
    13. Insurance
    14. Home Improvement
    15. Miscellaneous

    Transaction statement: "{transaction_statement}"
    Location: {location}
    Category:
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Example location
location = "New York"

def categorize_transaction(row):
    transaction_statement = row['Transaction_Statement']
    google_soup = google_search(transaction_statement + " " + location)
    bio = get_bio_from_google(google_soup)
    category = get_category_using_gpt(transaction_statement, location, bio)
    return category

df_transactions['Category'] = df_transactions.apply(categorize_transaction, axis=1)

categorized_csv_path = '/mnt/data/categorized_transactions.csv'
df_transactions.to_csv(categorized_csv_path, index=False)

df_transactions.head()
