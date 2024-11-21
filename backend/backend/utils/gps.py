# we can use the tracker manual to set the server's IP and port as the target for data transmission.
# import socket

# HOST = '0.0.0.0'  # Listen on all interfaces
# PORT = 5000  # Port configured on the tracker

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen(5)

# print(f'Listening on {HOST}:{PORT}...')
# while True:
#     client, addr = server.accept()
#     print(f'Connection from {addr}')
#     while True:
#         data = client.recv(1024)
#         if not data:
#             break
#         print('Received:', data.decode('ascii'))
#     client.close()

# we can use serial tp connect to a gps
# import serial

# # Replace 'COM3' with your serial port name
# gps = serial.Serial(port="COM3", baudrate=9600, timeout=1)

# while True:
#     try:
#         line = gps.readline().decode('ascii', errors='ignore').strip()
#         if line.startswith("$GPRMC"):  # Filter for specific NMEA sentences
#             print("GPS Data:", line)
#     except KeyboardInterrupt:
#         print("Exiting...")
#         break
# gps.close()
