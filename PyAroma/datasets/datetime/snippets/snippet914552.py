from datetime import datetime


def unpackTimecode(timecode):
    'unpacks a timecode to minutes, seconds, and milliseconds'
    if ('.' in timecode):
        x = datetime.strptime(timecode, '[%M:%S.%f]')
    else:
        x = datetime.strptime(timecode, '[%M:%S]')
    minutes = x.minute
    seconds = x.second
    milliseconds = int((x.microsecond / 1000))
    return (minutes, seconds, milliseconds)
