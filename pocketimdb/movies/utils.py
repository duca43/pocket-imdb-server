from datetime import datetime

seconds_min = 60
seconds_hour = seconds_min * 60
seconds_day = seconds_hour * 24
seconds_month = seconds_day * 30
seconds_year = seconds_day * 365

def get_timestamp_relative_diff(timestamp):
    
    diff = int((datetime.now() - timestamp).total_seconds())

    if (diff < seconds_min):
        return get_timestamp_relative_diff_desc(diff, 1, 'second')

    if (diff < seconds_hour):
        return get_timestamp_relative_diff_desc(diff, seconds_min, 'minute')

    if (diff < seconds_day):
        return get_timestamp_relative_diff_desc(diff, seconds_hour, 'hour')

    if (diff < seconds_month):
        return get_timestamp_relative_diff_desc(diff, seconds_day, 'day')

    if (diff < seconds_year):
        return get_timestamp_relative_diff_desc(diff, seconds_month, 'month')

    return get_timestamp_relative_diff_desc(diff, seconds_year, 'year')

def get_timestamp_relative_diff_desc(diff, seconds_period, word):
    period = int(diff / seconds_period)
    period_word = word + 's' if period > 1 else word
    return str(period) + ' ' + period_word + ' ago'
