from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
import random

SERVER_HOST_IP = "localhost"
SERVER_PORT = 502

# Create an instance of ModbusServer
server = ModbusServer(SERVER_HOST_IP, SERVER_PORT, no_block=True)

if __name__ == '__main__':
    try:
        print("Starting server...")
        server.start()
        print("Server online")

        # Server enable
        DataBank.set_bits(9901, [1])

        # Sample Rate (Hz)
        DataBank.set_words(39901, [2])

        # Fake sensor configuration (LANE 00)
        # Lane_Enable
        DataBank.set_bits(0, [1])
        # Sensor value
        DataBank.set_words(30001, [0])
        # Raw voltage value (0.1 mV)
        DataBank.set_words(30002, [0])
        # Sensor type
        DataBank.set_words(40001, [0])

        # Generate random data
        while True:
            DataBank.set_words(30002, [DataBank.get_words(30002)[0]+random.randint(-6, 8)])
            DataBank.set_words(30001, [DataBank.get_words(30002)[0]*1000])
            sleep(1/DataBank.get_words(39901)[0])

    except:
        print("Server Shutting down")
        server.stop()
        print("Server offline")