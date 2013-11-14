from dateutil.relativedelta import relativedelta

GRANULARITY_THRESHOLD = 3

def get_granularity(start_date, end_date):
    delta = relativedelta(end_date, start_date)

    if (delta.years > GRANULARITY_THRESHOLD):
        return 'years'
    elif (delta.months > GRANULARITY_THRESHOLD):
        return 'months'
    elif (delta.weeks > GRANULARITY_THRESHOLD):
        return 'weeks'
    else:
        return 'days'
