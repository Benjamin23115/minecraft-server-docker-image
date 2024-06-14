import requests

def getPaperVersion():
    url = "https://papermc.io/_next/data/S0cVqMWrriHKW0xvV3HXs/downloads/all.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Access the nested JSON structure correctly
        initial_project_version = data.get('pageProps', {}).get('initialProjectVersion')
        
        return initial_project_version
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None