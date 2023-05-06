import re


def get_timeframes(details):
    pattern_same_day = r"Between (\d{2}:\d{2} UTC) and (\d{2}:\d{2} UTC) on (\d{1,2} [A-Za-z]+ \d{4})"
    pattern_different_days = r"Between (\d{2}:\d{2} UTC) on (\d{1,2} [A-Za-z]+ \d{4}) and (\d{2}:\d{2} UTC) on (\d{1,2} [A-Za-z]+ \d{4})"
    match_same_day = re.search(pattern_same_day, details)
    if match_same_day is None:
        match_different_day = re.search(pattern_different_days, details)
        start_time = match_different_day.group(1)
        start_date = match_different_day.group(2)
        end_time = match_different_day.group(3)
        end_date = match_different_day.group(4)
    else:
        start_time = match_same_day.group(1)
        start_date = match_same_day.group(3)
        end_time = match_same_day.group(2)
        end_date = match_same_day.group(3)

        return start_time, start_date, end_time, end_date