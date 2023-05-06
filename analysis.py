import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import cosine
import json
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt


with open('incident_report.json', encoding='utf-8') as f:
    data = json.load(f)

incident_title = []

for incident in data:
    incident_title.append(incident["services_affected"])

df = pd.DataFrame({'services_affected': incident_title})

vectorizer = CountVectorizer()

title_matrix = vectorizer.fit_transform(df['services_affected'])

correlations = pd.DataFrame(1 - cosine_similarity(title_matrix))

correlations.index = df['services_affected']
correlations.columns = df['services_affected']

heatmap = sns.heatmap(correlations, cmap='coolwarm')
heatmap.tick_params(axis='both', which='major', labelsize=4)
plt.title('Correlation Matrix of Services Affected')
plt.show()