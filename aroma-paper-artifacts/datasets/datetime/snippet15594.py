


def iso_datetime():
    ' Return validation schema for datetime '
    return {'format': '\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{3}Z', 'format_error': 'Invalid date format'}
