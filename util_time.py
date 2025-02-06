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

def convert_to_local(timestamp, local_tz = TIMEZONE):
    """
    Converts a UTC timestamp string to local time.
    
    Args:
        timestamp (str): The UTC timestamp.
        local_tz (str): The target local timezone.
        
    Returns:
        datetime: Converted local time.
    """
    # Convert string to datetime object and set UTC timezone
    utc_dt = datetime.fromisoformat(timestamp).replace(tzinfo=ZoneInfo("UTC"))

    # Convert to local timezone
    local_dt = utc_dt.astimezone(ZoneInfo(local_tz))

    # Return as string in ISO 8601 format
    return local_dt.isoformat()
