from datetime import datetime, time
from zoneinfo import ZoneInfo

TIMEZONE = "America/Chicago"

def get_begin_today():
    # Get today's date in the local timezone
    local_now = datetime.now(ZoneInfo(TIMEZONE))
    
    # Set time to midnight (00:00:00)
    local_midnight = datetime.combine(local_now.date(), time.min, tzinfo=ZoneInfo(local_tz))
    
    # Convert to UTC
    utc_time = local_midnight.astimezone(ZoneInfo("UTC"))
    
    return utc_time

def get_end_today():
    # Get today's date in the local timezone
    local_now = datetime.now(ZoneInfo(TIMEZONE))
    
    # Set time to one microsecond before midnight (23:59:59.999999)
    local_midnight = datetime.combine(local_now.date(), time.max, tzinfo=ZoneInfo(local_tz))
    
    # Convert to UTC
    utc_time = local_midnight.astimezone(ZoneInfo("UTC"))
    
    return utc_time
