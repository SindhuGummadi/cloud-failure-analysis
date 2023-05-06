import numpy as np
from sklearn.cluster import KMeans
import json


import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


with open('incident_report_azure.json', encoding='utf-8') as f:
    data = json.load(f)

docs = [d["incident_title"] for d in data]

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(docs)
n_clusters = 8
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(X)
for i in range(len(docs)):
    kmeans.labels_[i]