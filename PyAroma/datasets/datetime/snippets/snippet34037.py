from datetime import datetime


def part_of_day():
    current_hour = datetime.now().hour
    if (current_hour < 12):
        part_of_day = 'morning'
    elif (12 <= current_hour < 17):
        part_of_day = 'afternoon'
    else:
        part_of_day = 'evening'
    return part_of_day
