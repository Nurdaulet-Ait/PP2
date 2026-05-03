import datetime

x = datetime.datetime.now()
print(x)


date1 = datetime.datetime(2024, 5, 17)
print(date1)


print(x.strftime("%A"))
print(x.strftime("%d %B %Y"))


start = datetime.datetime(2024, 1, 1)
end = datetime.datetime(2024, 1, 10)

difference = end - start

print(difference.days)


utc_time = datetime.datetime.now(datetime.timezone.utc)
print(utc_time)
#ex
import datetime

# 1
today = datetime.datetime.now()
new_date = today - datetime.timedelta(days=5)
print(new_date)


# 2
today = datetime.datetime.now()

yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


# 3
now = datetime.datetime.now()
print(now.replace(microsecond=0))


# 4
date1 = datetime.datetime(2024, 5, 1, 12, 0, 0)
date2 = datetime.datetime(2024, 5, 2, 12, 0, 0)

difference = date2 - date1

print(difference.total_seconds())