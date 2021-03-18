# ---------------------------------------------------------------------------#
# Import libraries
# ---------------------------------------------------------------------------#
import csv
import random
import time
from datetime import datetime
from pyModbusTCP.client import ModbusClient

from pyModbusTCP.constants import READ_INPUT_REGISTERS

SERVER_HOST_IP = "localhost"
SERVER_PORT = 502

t = datetime.now()
x_1 = 0
x_2 = 0

fieldnames = ["datetime", "x_1", "x_2"]

with open('data.csv', 'w', newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

if __name__ == '__main__':
    
    try:
        try:
            client = ModbusClient()
            client.host(SERVER_HOST_IP)
            client.port(SERVER_PORT)
        except ValueError:
            print("Error with host or port parameters")
        
        client.open()

        while True:
            with open('data.csv', 'a', newline="") as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                t = datetime.now()
                x_1 = client.read_input_registers(30001)[0]
                x_2 = client.read_input_registers(30002)[0]

                if (x_1 is not None) and (x_2 is not None):
                    print("x_1: " + str(x_1) + ", x_2: " + str(x_2))

                    info = {
                        "datetime": t,
                        "x_1": x_1,
                        "x_2": x_2
                    }

                    csv_writer.writerow(info)
                    print('{}'.format(t), str(x_1),  str(x_2))

            time.sleep(0.25)

    except:
        print("Closing client connection")
        client.close()
        print("Client connection closed")
    


    


