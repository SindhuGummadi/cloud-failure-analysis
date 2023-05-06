from bs4 import BeautifulSoup
import requests
import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

url = "https://status.cloud.google.com/summary"
response = requests.get(url)

html = response.content

soup = BeautifulSoup(html, 'html.parser')
incidents = soup.find_all('psd-product-table')

data = []
incident_list = []

# Loop through all the incidents and extract the relevant information
for incident in incidents:
    incident_type = incident.find('span', class_='nAlKgGlv8Vo__product-name').get_text()
    incident_info = incident.find('table', class_='ise88CpWulY__psd-table')
    incident_summary_info = incident_info.find('td', class_='ise88CpWulY__summary')

    if incident_summary_info is not None:
        start_day = incident_info.find('td', class_='ise88CpWulY__date').get_text()
        incident_duration = incident_info.find('span', class_='ise88CpWulY__duration-text').get_text()
        incident_url = 'https://status.cloud.google.com/' + incident_summary_info.find('a').get('href');
        incident_report = requests.get(incident_url).content
        inner_soup = BeautifulSoup(incident_report, 'html.parser')
        main = inner_soup.find('main')

        incident_summary = main.find('h2', class_='incident-header').get_text().strip()

        status_table = main.find('table', class_='status-updates psd-table')
        rows = status_table.find('tbody').find('tr')
        incident_start_time = rows.find('td', class_='time').get_text()
        incident_description = rows.find('td', class_='description').get_text()
        if "This incident is being merged with an existing incident" in incident_description:
            actual_incident_url = rows.find('a').get('href')
            actual_incident_report = requests.get(actual_incident_url).content
            inner_soup_2 = BeautifulSoup(actual_incident_report, 'html.parser')
            inner_table = inner_soup_2.find('table', class_ = 'status-updates psd-table')
            inner_rows = inner_table.find('tbody').find('tr')
            descr = inner_rows.find('td', class_ = 'description').get_text()

        data.append({
            'incident_type': incident_type,
            'start_date': start_day,
            'start_time': '',
            'end_time': incident_start_time,
            'duration': incident_duration,
            'services_affected': incident_summary,
            'description': incident_description
        })

# with open('incident_report.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

with open('incidents.txt', 'w') as f:
    for item in incident_list:
        f.write("%s\n" % item)