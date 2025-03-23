from datetime import datetime, time
from zoneinfo import ZoneInfo

TIMEZONE = "America/Chicago"

def begin_today():
    return begin_day(get_now())

def end_today():
    return end_day(get_now())
    
def begin_day(local_start_date):
    # Set time to midnight (00:00:00)
    local_midnight = datetime.combine(local_start_date, time.min, tzinfo=ZoneInfo(TIMEZONE))
    
    # Convert to UTC
    utc_time = local_midnight
    
    return utc_time

def end_day(local_end_date):
    # Set time to one microsecond before midnight (23:59:59.999999)
    local_bf_midnight = datetime.combine(local_end_date, time.max, tzinfo=ZoneInfo(TIMEZONE))
    
    # Convert to UTC
    utc_time = local_bf_midnight
    
    return utc_time

def get_now():
    now = datetime.now(ZoneInfo(TIMEZONE))
    return now.replace(tzinfo=None).isoformat()

def get_time(timestamp_str):
    # returns the time in AM/PM format
    # from an iso timestamp string
    
    dt = datetime.fromisoformat(timestamp_str)
    return dt.strftime("%I:%M %p")
    
def get_today_formatted():  
    # Get the current local time
    local_time = datetime.now(ZoneInfo(TIMEZONE))
    # Format the datetime as desired
    formatted_time = local_time.strftime("%A, %B %-d, %Y")

    return formatted_time

def get_today_timestamp():
    return datetime.now(ZoneInfo(TIMEZONE)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
