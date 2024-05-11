from datetime import datetime


class TimeUtils:

    @staticmethod
    def utc_unix() -> int:
        return int(datetime.utcnow().timestamp())
