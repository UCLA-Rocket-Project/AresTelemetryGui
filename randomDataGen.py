# ---------------------------------------------------------------------------#
# Import libraries
# ---------------------------------------------------------------------------#
import csv
import random
import time
from datetime import datetime

t = datetime.now()
x_1 = 1000
x_2 = 5000

fieldnames = ["datetime", "x_1", "x_2"]

# This code will later be replaced with a modbus client that writes to the CSV
with open('data.csv', 'w', newline="") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a', newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "datetime": t,
            "x_1": x_1,
            "x_2": x_2
        }

        csv_writer.writerow(info)
        print('{}'.format(t), x_1, x_2)

        t = datetime.now()
        x_1 = x_1 + random.randint(-6, 8)
        x_2 = x_2 + random.randint(-5, 6)

    time.sleep(0.25)