from bs4 import BeautifulSoup
import requests
import json
import re


data = []
base_url = "https://azure.status.microsoft/en-us/statushistoryapi/?serviceSlug=all&regionSlug=all&startDate=all" \
      "&shdrefreshflag=true "
def fetch_data():
    for i in range(1, 12):
        url = base_url + ('&page=' + str(i))
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        months = soup.find_all('div', class_='month-incident-container')
        for month in months:
            incidents = month.find_all('div', class_='row')
            for incident in incidents:
                start_time, start_date, end_time, end_date = "", "", "", ""
                main_tag = incident.find('div', class_="col-sm-11 incident-history-item")
                if main_tag is not None:
                    incident_title = incident.find('div', class_='col-md-8 incident-history-title').get_text().strip()
                else:
                    incident_body = incident.find('div', class_='card-body')
                    p_tags = incident_body.find_all('p')
                    failure_symptoms, root_cause, steps_taken_to_repair, mitigation_in_future = "", "", "", ""
                    for p in p_tags:
                        if "summary" in p.get_text().lower() and "impact" in p.get_text().lower():
                            start_time, start_date, end_time, end_date = get_timeframes(p.get_text())
                            if p.get_text().split(":", 1) is not None and len(p.get_text().split(":", 1)[1])>0:
                                failure_symptoms = p.get_text().split(":", 1)[1]
                        if "root cause:" in p.get_text().lower():
                            if p.get_text().split(":", 1) is not None and len(p.get_text().split(":", 1)[1])>0:
                                root_cause = p.get_text().split(":", 1)[1]
                        if "impact statement" in p.get_text().lower():
                            start_time, start_date, end_time, end_date = get_timeframes(p.get_text())
                            if p.get_text().split(":", 1) is not None and len(p.get_text().split(":", 1)[1])>0:
                                failure_symptoms = p.get_text().split(":", 1)[1]
                        if "Mitigation" in p.get_text():
                            if p.get_text().split(":", 1) is not None and len(p.get_text().split(":", 1)[1])>0:
                                steps_taken_to_repair = p.get_text().split(":", 1)[1]
                        if "next steps" in p.get_text().lower():
                            if p.get_text().split(":", 1) is not None and len(p.get_text().split(":", 1)) > 1 and len(p.get_text().split(":", 1)[1])>0:
                                mitigation_in_future = p.get_text().split(":", 1)[1]
                        if "What happened?" in p.get_text():
                            details = p.find_next(name='p').get_text()
                            start_time, start_date, end_time, end_date = get_timeframes(details)
                            failure_symptoms = details
                        if "What went wrong and why?" in p.get_text():
                            root_cause = p.find_next(name='p').get_text()
                        if "How did we respond?" in p.get_text():
                            steps_taken_to_repair = p.find_next(name='p').get_text()
                        if "How are we making incidents like this less likely or less impactful?" in p.get_text():
                            end_tag = p.find_next(name='p',
                                                  string='How can customers make incidents like this less impactful?')
                            if end_tag is None:
                                end_tag = p.find_next(name='p',
                                                      string='How can we make our incident communications more useful?')
                            if p and end_tag:
                                result = ''
                                tag = p.find_next_sibling()
                                while tag and tag != end_tag:
                                    result += str(tag.get_text())
                                    tag = tag.find_next_sibling()
                                mitigation_in_future = result

                    if None not in [incident_title, failure_symptoms, root_cause, steps_taken_to_repair,
                                    mitigation_in_future]:
                        data.append({
                            "incident_title": incident_title,
                            "start_time" : start_time,
                            "end_time" : end_time,
                            "start_date" : start_date,
                            "end_date" : end_date,
                            "failure_symptoms": failure_symptoms,
                            "root_cause": root_cause,
                            "steps_taken_to_repair": steps_taken_to_repair,
                            "maintenance_events": mitigation_in_future
                        })

    with open('incident_report_azure.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_timeframes(details):
    pattern_same_day = r"Between (\d{2}:\d{2})( UTC)? and(?: until)? (\d{2}:\d{2})( UTC)? on (\d{1,2} [A-Za-z]+ \d{4})"
    pattern_different_days = r"Between (\d{2}:\d{2})( UTC)? on (\d{1,2} [A-Za-z]+(?: \d{4})?) and (\d{2}:\d{2})( UTC)? on (\d{1,2} [A-Za-z]+(?: \d{4})?)"
    match_same_day = re.search(pattern_same_day, details)

    start_time, start_date, end_time, end_date = "", "", "", ""
    if match_same_day is None:
        match_different_day = re.search(pattern_different_days, details)
        if match_different_day is not None:
            start_time = match_different_day.group(1)
            start_date = match_different_day.group(3)
            end_time = match_different_day.group(4)
            end_date = match_different_day.group(6)
    else:
        start_time = match_same_day.group(1)
        start_date = match_same_day.group(5)
        end_time = match_same_day.group(3)
        end_date = match_same_day.group(5)
    return start_time, start_date, end_time, end_date

fetch_data()
