from datetime import datetime, time
from zoneinfo import ZoneInfo

TIMEZONE = "America/Chicago"

def begin_day(local_start_date):
    # Set time to midnight (00:00:00)
    local_midnight = datetime.combine(local_start_date, time.min, tzinfo=ZoneInfo(TIMEZONE))
    
    # Convert to UTC
    utc_time = local_midnight.astimezone(ZoneInfo("UTC"))
    
    return utc_time

def end_day(local_end_date):
    # Set time to one microsecond before midnight (23:59:59.999999)
    local_bf_midnight = datetime.combine(local_end_date, time.max, tzinfo=ZoneInfo(TIMEZONE))
    
    # Convert to UTC
    utc_time = local_bf_midnight.astimezone(ZoneInfo("UTC"))
    
    return utc_time
