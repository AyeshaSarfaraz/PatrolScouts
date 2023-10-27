from pymavlink import mavutil
from time import sleep

the_connection = mavutil.mavlink_connection('/dev/serial0', 57600)

the_connection.wait_heartbeat()

print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

while True:
    try:
        longitude =  the_connection.messages['GPS_RAW_INT'].lon
        latitude =  the_connection.messages['GPS_RAW_INT'].lat
        timestamp = the_connection.time_since('GPS_RAW_INT')
        print(f"Coordinates: ({latitude/100},{longitude/100})")
        break
    except:
        print('No GPS_RAW_INT message received')
