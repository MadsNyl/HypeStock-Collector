import time, datetime

first = "2020-01-02"
second = "2020-01-03"

first_object = datetime.datetime.strptime(first, "%Y-%m-%d").date()
second_object = datetime.datetime.strptime(second, "%Y-%m-%d").date()

diff = second_object - first_object
print(diff.days)