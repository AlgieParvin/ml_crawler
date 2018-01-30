from dateutil.parser import parse


class CheckTimeMixin(object):
    @staticmethod
    def posted_after(timestamp, last_timestamp):
        tm = parse(timestamp)
        return last_timestamp < tm

    @staticmethod
    def convert_time(timestamp):
        if 'UTC' in timestamp:
            index = timestamp.find('UTC')
            if index != -1:
                timestamp = timestamp[:index]
        return timestamp
