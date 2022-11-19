import datetime


def check_if_link_start_with_http_https(link):
    if link.startswith('http://') or link.startswith('https://'):
        return True
    return False


def check_valid_link(link):
    if link is not None and check_if_link_start_with_http_https(link):
        return True
    return False


def date_convert(input_date):
    date = list(reversed(input_date.split('. ')))
    year, month, day = [int(d) for d in date]
    converted_date = datetime.date(year, month, day)
    return str(converted_date)
