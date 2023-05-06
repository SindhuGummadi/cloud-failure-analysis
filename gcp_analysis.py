
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import json

services_affected = []

with open('incident_report.json', encoding='utf-8') as f:
    data = json.load(f)



for incident in data:
    services_affected.extend(incident["services_affected"].split(", "))

service_counts = {}
for service in services_affected:
    if service in service_counts:
        service_counts[service] += 1
    else:
        service_counts[service] = 1
sorted_counts = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)

filtered_counts = [(service, count) for (service, count) in sorted_counts if count >= 5]

plt.barh([x[0] for x in filtered_counts], [x[1] for x in filtered_counts])

plt.title("Most affected services")
plt.xlabel("Number of occurrences")
plt.ylabel("Service name")
plt.yticks(fontsize=6)
plt.xticks(range(0, max(service_counts.values()) + 2, 2))
