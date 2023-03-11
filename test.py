from datetime import datetime
t = "11:21 AM EST, Sat March 11, 2023"

time = f"{t[18:21]} {t[24:26]} {t[28:32]}"
print(datetime.strptime(time, "%b %d %Y").date())