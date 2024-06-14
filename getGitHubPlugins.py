import requests
from bs4 import BeautifulSoup

def getLatestJarURL(base_url, base_download_url, filename_format):
  """Fetches the download URL for the latest JAR file from the releases page."""
  response = requests.get(base_url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the h1 element with class "d-inline mr-3"
  download_info = soup.find("h1", class_="d-inline mr-3")
  if not download_info:
    print("Error: Could not find element with latest release version.")
    return None

  # Extract the text content from the h1 element
  text = download_info.text.strip()

  # Construct the download URL using the base URL, extracted text, and filename format
  download_url = f"{base_download_url}/download/{text}/{filename_format.replace('{text}', text)}"

  return download_url