from dronekit import connect, VehicleMode

connection_string = "/dev/serial0"
baud_rate = 57600

print("Connecting to UAV.....")
vehicle = connect(connection_string, wait_ready=True, baud=baud_rate)

vehicle.wait_ready('autopilot_version')
print(f"Autopilot version: {vehicle.version}")

print(f"Attitude is: {vehicle.attitude}")

print(f"vehicle location: {vehicle.location.global_relative_frame}")