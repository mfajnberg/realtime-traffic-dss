import traci
import sumolib
import socket

def send_to_prolog(pos, direction, speed):
    data = f"{pos},{direction},{speed}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.sendall(data.encode())
        response = s.recv(1024).decode()
    # Antwort verarbeiten (z.B.: "Decision: proceed, Speed: 45")
    response_parts = response.strip().split(", ")
    decision = response_parts[0].split(": ")[1]
    speed = int(response_parts[1].split(": ")[1])
    return decision, speed

sumoCmd = ["sumo", "-c", "config.sumocfg"]
traci.start(sumoCmd)

step = 0
while step < 1000:
    traci.simulationStep() 
    vehicles = traci.vehicle.getIDList()
    for vehicle in vehicles:
        pos = traci.vehicle.getPosition(vehicle)
        speed = traci.vehicle.getSpeed(vehicle)
        direction = traci.vehicle.getRoadID(vehicle)
        decision, speed = send_to_prolog("norden", "geradeaus", 45)
        traci.vehicle.setSpeed(vehicle, speed)
    step += 1

traci.close()