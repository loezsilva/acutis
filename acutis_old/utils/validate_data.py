from datetime import datetime

def validate_date_format(date_str):
    if not isinstance(date_str, str):
        return False
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False