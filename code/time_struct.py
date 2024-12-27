class TimeFormat:
    FORMAT_HM = "%H%M"


class TimeStruct:
    def __init__(self, str: str, t_format: TimeFormat):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.format = t_format
        self.get_time_struct(str, t_format)

    def __add__(self, other):
        minute = self.minute + other.minute
        hour = self.hour + other.hour
        day = self.day + other.day
        month = self.month + other.month
        year = self.year + other.year
        second = self.second + other.second
        # print(f"old{minute} {hour} {day} {month} {year}")
        if minute >= 60:
            minute -= 60
            hour += 1
        if hour >= 24:
            hour -= 24
            day += 1
        if month > 12:
            month -= 12
            year += 1
        if day > 31:
            day -= 31
            month += 1
        if month > 12:
            month -= 12
            year += 1
        if month < 1:
            month += 12
            year -= 1
        if year < 0:
            year = 0
        if month < 1:
            month = 1
        if day < 1:
            day = 1
        if hour < 0:
            hour = 0
        if minute < 0:
            minute = 0
        if second < 0:
            second = 0
        if self.format == TimeFormat.FORMAT_HM:
            return TimeStruct(f"{hour:02d}:{minute:02d}", TimeFormat.FORMAT_HM)

    def __str__(self):
        if self.format == TimeFormat.FORMAT_HM:
            return f"{self.hour:02d}:{self.minute:02d}"

    def __lt__(self, other):
        if self.format == TimeFormat.FORMAT_HM:
            return self.hour < other.hour

    def __le__(self, other):
        if self.format == TimeFormat.FORMAT_HM:
            return self.hour <= other.hour

    def __ge__(self, other):
        if self.format == TimeFormat.FORMAT_HM:
            return self.hour >= other.hour

    def __ne__(self, other):
        if self.format == TimeFormat.FORMAT_HM:
            return self.hour != other.hour

    def __gt__(self, other):
        if self.format == TimeFormat.FORMAT_HM:
            return self.hour > other.hour

    def __eq__(self, other):
        if self.format == TimeFormat.FORMAT_HM:
            return self.hour == other.hour

    def __sub__(self, other):
        minute = self.minute - other.minute
        hour = self.hour - other.hour
        day = self.day - other.day
        month = self.month - other.month
        year = self.year - other.year
        second = self.second - other.second
        if minute < 0:
            minute += 60
            hour -= 1
        if hour < 0:
            hour += 24
            day -= 1
        if month < 0:
            month += 12
            year -= 1
        if day < 0:
            day += 31
            month -= 1
        if month < 0:
            month += 12
            year -= 1
        if month > 12:
            month -= 12
            year += 1
        if year < 0:
            year = 0
        if month < 1:
            month = 1
        if day < 1:
            day = 1
        if hour < 0:
            hour = 0
        if minute < 0:
            minute = 0
        if second < 0:
            second = 0

        if self.format == TimeFormat.FORMAT_HM:
            return TimeStruct(f"{hour:02d}:{minute:02d}", TimeFormat.FORMAT_HM)

    def get_time_struct(self, str: str, format: TimeFormat) -> str:
        if format == TimeFormat.FORMAT_HM:
            words = str.split(":")
            self.hour = int(words[0])
            self.minute = int(words[1])
        # elif format == TimeFormat.FORMAT_YMDH:
        #     words = str.split(" ")
        #     self.year = int(words[0])
        #     self.month = int(words[1])
        #     self.day = int(words[2])
        #     words = words[3].split(":")
        #     self.hour = int(words[0])
        # elif format == TimeFormat.FORMAT_YMDHM:
        #     words = str.split(" ")
        #     self.year = int(words[0])
        #     self.month = int(words[1])
        #     self.day = int(words[2])
        #     words = words[3].split(":")
        #     self.hour = int(words[0])
        #     self.minute = int(words[1])
        # elif format == TimeFormat.FORMAT_YMDHMS:
        #     words = str.split("-")
        #     self.year = int(words[0])
        #     self.month = int(words[1])
        #     self.day = int(words[2])
        #     words = words[3].split(":")
        #     self.hour = int(words[0])
        #     self.minute = int(words[1])
        #     self.second = int(words[2])
        # elif format == TimeFormat.FORMAT_YMD:
        #     words = str.split("-")
        #     self.year = int(words[0])
        #     self.month = int(words[1])
        #     self.day = int(words[2])
        else:
            print("Invalid format")

        return


if __name__ == "__main__":
    t1 = TimeStruct("13:30", TimeFormat.FORMAT_HM)
    t2 = TimeStruct("01:40", TimeFormat.FORMAT_HM)
    print(t1 - t2)
