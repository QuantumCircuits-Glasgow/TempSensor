import schedule
from temperature import read_temps

# Creating CSV file where this dates data will be written:
today = date.today()

try:
    csv_file = open(f"DATA//DATA:{today}.csv", "x")
    writer = csv.writer(csv_file)
    headings = [f"Pipe {i + 1}" for i in range(numberSensors)]
    headings.insert(0, "Date & Time")
    writer.writerow(headings)
except FileExistsError:
    csv_file = open(f"DATA//DATA:{today}.csv", "a", newline="\n")
    writer = csv.writer(csv_file)


try:
    schedule.every().day.at("06:00").do(load_daily_data.main())
except:
    print("Unable to schedule file upload, will attempt in 6 hours again")

while True:
    temps = [f"{datetime.now()}".split(".")[0]] + read_temps()
    writer.writerow(temps)
    schedule.run_pending()
    time.sleep(60)
