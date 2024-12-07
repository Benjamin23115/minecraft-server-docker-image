import requests
from bs4 import BeautifulSoup
import re

def getPaperVersion():
    paperWebsite ="https://papermc.io/downloads/paper"
    try:
        response = requests.get(paperWebsite)
        if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                pattern = re.compile(r'Get Paper\s+(\d+(\.\d+)*)')
                matches = pattern.findall(text)
                if matches:
                    return(matches[0][0])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
