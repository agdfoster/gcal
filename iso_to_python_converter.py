
import datetime
import dateutil.parser

def iso_to_python_converter(iso_date_time):
    converted = dateutil.parser.parse(iso_date_time)
    try:
        assert(isinstance(converted, datetime.date))
    except Exception as e:
        raise e
    return converted




if __name__ == '__main__':
    examples = [
        '2047-02-05',
        '2018-03-22T23:00:00Z',
        '2017-07-05T17:30:00Z',
        '2017-06-17',
        # '2017-07-01T25:00:00Z', # << should throw error
        '2017-07-01T12:00:00Z'
    ]
    for item in examples:
        converted = iso_to_python_converter(item)
        print(item)
        print(converted)
        print(isinstance(converted, datetime.date))

