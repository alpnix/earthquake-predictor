from dotenv import load_dotenv
load_dotenv()

import requests
from bs4 import BeautifulSoup
import re

import os
from supabase import create_client

from datetime import datetime


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

URL = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"

def get_earthquake_data(URL):
    """
    Fetches earthquake data from the specified URL and returns it as a string.
    """

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    data = soup.find("pre").text

    return data


def sanitize_data(raw_data): 
    """
    Cleans the earthquake data by removing unnecessary characters and formatting.
    """

    pattern = re.compile(r'(\d{4}\.\d{2}\.\d{2}) (\d{2}:\d{2}:\d{2})\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)\s+-\.-\s+([\d\.]+)\s+-\.-\s+(.+?)\s{2,}İlksel')
    matches = pattern.findall(raw_data)

    return matches


def save_data_to_database(data): 
    counter = 0

    for row in data:
        try: 
            supabase.table("earthquakes").insert({
                "date": row[0],
                "time": row[1],
                "latitude": float(row[2]),
                "longitude": float(row[3]),
                "depth": float(row[4]),
                "magnitude": float(row[5]),
                "place": row[6]
            }).execute()
            counter += 1
        except Exception as e:
            print(f"Error inserting data: {e}")

    print(f"Data saved to database successfully with {counter} records.")


raw_data = get_earthquake_data(URL)
matches = sanitize_data(raw_data)
save_data_to_database(matches)