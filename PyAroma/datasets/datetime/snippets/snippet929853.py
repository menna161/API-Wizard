import datetime
import os
import sys


def extract_seconds(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    log_created_year = get_log_created_year(input_file)
    start_datetime = get_start_time(lines, log_created_year)
    assert start_datetime, 'Start time not found'
    out = open(output_file, 'w')
    for line in lines:
        line = line.strip()
        if (line.find('Iteration') != (- 1)):
            dt = extract_datetime_from_line(line, log_created_year)
            elapsed_seconds = (dt - start_datetime).total_seconds()
            out.write(('%f\n' % elapsed_seconds))
    out.close()
