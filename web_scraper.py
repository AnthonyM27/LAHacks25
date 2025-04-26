import requests
from bs4 import BeautifulSoup
import json

# Function to scrape labs based on the topic of interest
def scrape_labs_by_topic(topic):
    base_url = 'https://vcresearch.berkeley.edu'
    url = base_url + '/research-units/centers-and-institutes-by-subject-area'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the labs in the 'main-content' section
    labs = soup.find('div', {'class': 'main-content'})
    lab_links = labs.find_all('a', href=True)
    
    filtered_labs = []
    for lab in lab_links:
        lab_name = lab.text.strip()
        lab_url = lab['href']
        # If the URL is relative, prepend the base URL
        if not lab_url.startswith('http'):
            lab_url = base_url + lab_url
        # Check if the topic is present in the lab name (case-insensitive)
        if re.search(topic, lab_name, re.IGNORECASE):
            filtered_labs.append({'name': lab_name, 'url': lab_url})

    return filtered_labs


if __name__ == "__main__":
    scrape_lab_names_and_links()
