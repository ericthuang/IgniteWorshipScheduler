from datetime import timedelta, datetime
import datetime as dt
import calendar as cal

MONTHS_IN_A_QUARTER = 3

ROLES = ["lead", "vocals", "leadKeys", "rhythmKeys", "acoustic",
         "leadElectric", "rhythmElectric", "bass", "drums", "percussion"]


def get_quarter_date_bounds(quarter_no, year_no):
    start_month = (quarter_no * MONTHS_IN_A_QUARTER) - (MONTHS_IN_A_QUARTER - 1)
    start = dt.datetime(year_no, start_month, 1)

    end_month = quarter_no * MONTHS_IN_A_QUARTER
    last_day_of_last_month = cal.monthrange(year_no, end_month)[1]
    end = dt.datetime(year_no, end_month, last_day_of_last_month)

    return (start, end)

def get_all_sundays_in_quarter(quarter_no, year_no):
    quarter_bounds = get_quarter_date_bounds(quarter_no, year_no)
    end_datetime = quarter_bounds[1]
    d = quarter_bounds[0]
    d += timedelta(days=6 - d.weekday())  # First Sunday
    while d <= end_datetime:
        yield d
        d += timedelta(days=7)

def datestring_to_datetime(datestring):
    return datetime.strptime(datestring, '%Y-%m-%d')

def datetime_to_datestring(datetime_obj):
    day = str(datetime_obj.day)
    if len(day) == 1:
        day = "0" + day
    month = str(datetime_obj.month)
    if len(month) == 1:
        month = "0" + month
    year = str(datetime_obj.year)
    return year + "-" + month + "-" + day

if __name__ == '__main__':
    for i in get_all_sundays_in_quarter(4, 2019):
        print(i)


    datetimetest = datestring_to_datetime("2019-05-27")
    print(str(datetimetest))

    print(datetime_to_datestring(datetimetest))