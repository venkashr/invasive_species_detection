from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('/dev/ttyACM0', baud="115200")

# Make sure the connection is valid
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % 
      (master.target_system, master.target_component))

# Receive a message
while True:
    time.sleep(0.1)
    msg = master.recv_match()
    if not msg:
        continue
    print(msg)
    if msg.get_type() == 'TERRAIN_REPORT':
        print(msg)
    if msg.get_type() == 'ATTITUDE':
        print(msg)

