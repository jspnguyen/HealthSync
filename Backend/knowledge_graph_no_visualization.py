import networkx as nx
import random
import json
from networkx.readwrite import json_graph

# Initialize the knowledge graph
G = nx.Graph()

# ---------------------------
# 1. Add Nodes (Patients, Doctors, Nurses, Rooms, Equipment, Beds)
# ---------------------------

# Define Patients
patients = [
    {
        "id": "P1",
        "type": "Patient",
        "priority": "Emergency",
        "severity": 5,
        "name": "John Doe",
        "needs_surgery": False,
    },
    {
        "id": "P2",
        "type": "Patient",
        "priority": "Regular",
        "severity": 2,
        "name": "Jane Smith",
        "needs_surgery": False,
    },
    {
        "id": "P3",
        "type": "Patient",
        "priority": "Surgery",
        "severity": 4,
        "name": "Alice Johnson",
        "needs_surgery": True,
    },
    {
        "id": "P4",
        "type": "Patient",
        "priority": "Emergency",
        "severity": 4,
        "name": "Bob Brown",
        "needs_surgery": False,
    },
]

# Define Doctors
doctors = [
    {
        "id": "D1",
        "type": "Doctor",
        "specialty": "Cardiology",
        "patients_per_hour": 6,
        "name": "Dr. Heart",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "D2",
        "type": "Doctor",
        "specialty": "Orthopedics",
        "patients_per_hour": 6,
        "name": "Dr. Bone",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "D3",
        "type": "Doctor",
        "specialty": "General Surgery",
        "patients_per_hour": 6,  # Adjusted to allow any doctor to perform surgery
        "name": "Dr. Surgeon",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "D4",
        "type": "Doctor",
        "specialty": "Emergency Medicine",
        "patients_per_hour": 6,
        "name": "Dr. Swift",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "D5",
        "type": "Doctor",
        "specialty": "Neurology",
        "patients_per_hour": 6,
        "name": "Dr. Brain",
        "current_patients": [],
        "time_busy": 0,
    },
]

# Define Nurses
nurses = [
    {
        "id": "N1",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Joy",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "N2",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Anna",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "N3",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Sam",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "N4",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Kim",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "N5",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Lee",
        "current_patients": [],
        "time_busy": 0,
    },
    {
        "id": "N6",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Pat",
        "current_patients": [],
        "time_busy": 0,
    },
]

# Define Equipment (Multiple instances of the same equipment type)
equipment_list = [
    {"id": "E1", "type": "Equipment", "scarcity": 1, "name": "Defibrillator"},
    {"id": "E2", "type": "Equipment", "scarcity": 3, "name": "X-Ray Machine"},
    {"id": "E3", "type": "Equipment", "scarcity": 2, "name": "MRI Scanner"},
    {"id": "E4", "type": "Equipment", "scarcity": 4, "name": "Ventilator"},
]

# Create multiple instances of equipment types
equipment = []
equipment_counter = 1
for eq in equipment_list:
    for i in range(eq["scarcity"]):
        equipment.append(
            {
                "id": f"{eq['id']}_{i+1}",
                "type": "Equipment",
                "name": eq["name"],
                "original_id": eq["id"],
            }
        )
        equipment_counter += 1

# Define Rooms
rooms = [
    {"id": "R1", "type": "Room", "name": "ER Room 1"},
    {"id": "R2", "type": "Room", "name": "ER Room 2"},
    {"id": "R3", "type": "Room", "name": "Surgery Room 1"},
    {"id": "R4", "type": "Room", "name": "Surgery Room 2"},
    {"id": "R5", "type": "Room", "name": "ICU Room 1"},
    {"id": "R6", "type": "Room", "name": "ICU Room 2"},
]

# Create a mapping from room IDs to rooms
rooms_dict = {room["id"]: room for room in rooms}

# Define bed counts per room
room_bed_counts = {
    "R1": 2,
    "R2": 2,
    "R3": 1,
    "R4": 1,
    "R5": 2,
    "R6": 2,
}

# Generate beds
beds = []

bed_id_counter = 1

for room_id, bed_count in room_bed_counts.items():
    for i in range(bed_count):
        bed_id = f"B{bed_id_counter}"
        bed = {
            "id": bed_id,
            "type": "Bed",
            "room_id": room_id,
            "name": f"Bed {i+1} in {rooms_dict[room_id]['name']}",
        }
        beds.append(bed)
        bed_id_counter += 1

# Add all entities to the graph
for entity in patients + doctors + nurses + equipment + rooms + beds:
    G.add_node(entity["id"], **entity)

# Create Available Resources node
available_resources_node = {
    "id": "AR",
    "type": "AvailableResources",
    "name": "Available Resources",
}
G.add_node(available_resources_node["id"], **available_resources_node)

# Connect doctors, nurses, equipment to Available Resources node
for doctor in doctors:
    G.add_edge(
        doctor["id"], available_resources_node["id"], relationship="available", weight=1
    )
for nurse in nurses:
    G.add_edge(
        nurse["id"], available_resources_node["id"], relationship="available", weight=1
    )
for eq in equipment:
    G.add_edge(
        eq["id"], available_resources_node["id"], relationship="available", weight=1
    )

# Add beds to the graph and connect them to rooms
for bed in beds:
    G.add_edge(bed["id"], bed["room_id"], relationship="in_room", weight=1)

# ---------------------------
# 2. Assign Resources to Rooms
# ---------------------------

# Define room-specific resources
room_resources = {
    "R1": {"doctors": ["D4"], "nurses": ["N1", "N2"], "equipment": ["E1_1"]},
    "R2": {"doctors": ["D1"], "nurses": ["N3"], "equipment": ["E2_1"]},
    "R3": {"doctors": ["D3"], "nurses": ["N4"], "equipment": ["E3_1"]},
    "R4": {"doctors": ["D2"], "nurses": ["N5"], "equipment": ["E4_1"]},
    "R5": {"doctors": ["D5"], "nurses": ["N6"], "equipment": []},
    "R6": {"doctors": ["D1"], "nurses": ["N2"], "equipment": ["E1_2"]},
}


# Function to assign resources to rooms
def assign_resource_to_room(resource_id, resource_type, room_id):
    if G.has_edge(resource_id, available_resources_node["id"]):
        # Remove edge to 'Available Resources' node
        G.remove_edge(resource_id, available_resources_node["id"])
        # Add edge to the room
        if resource_type == "Doctor":
            G.add_edge(room_id, resource_id, relationship="has_doctor", weight=1)
        elif resource_type == "Nurse":
            G.add_edge(room_id, resource_id, relationship="has_nurse", weight=1)
        elif resource_type == "Equipment":
            G.add_edge(room_id, resource_id, relationship="has_equipment", weight=1)
        print(
            f"Assigned {resource_type} {G.nodes[resource_id]['name']} to {G.nodes[room_id]['name']}"
        )
        return True
    else:
        print(f"{resource_type} {resource_id} is already assigned to a room.")
        return False


# Assign resources to rooms
for room_id, resources in room_resources.items():
    # Assign Doctors
    for doctor_id in resources["doctors"]:
        assign_resource_to_room(doctor_id, "Doctor", room_id)

    # Assign Nurses
    for nurse_id in resources["nurses"]:
        assign_resource_to_room(nurse_id, "Nurse", room_id)

    # Assign Equipment
    for eq_id in resources["equipment"]:
        assign_resource_to_room(eq_id, "Equipment", room_id)

# ---------------------------
# 3. Connect Patients to Beds
# ---------------------------

# Add the waiting room node
waiting_room = {"id": "WR", "type": "WaitingRoom", "name": "Waiting Room"}
G.add_node(waiting_room["id"], **waiting_room)

# Create a path from the waiting room to each room by adding an edge between them
for room in rooms:
    G.add_edge(waiting_room["id"], room["id"], relationship="pathway", weight=1)
    print(f"Added a path from Waiting Room to {room['name']}")

# Waiting room priority queue
waiting_room_queue = []


# Function to assign a patient to a bed
def assign_patient_to_bed(patient, G, beds):
    """
    Assigns a patient to a bed with required resources available.
    Returns the assigned bed ID.
    """
    # Get a list of occupied beds
    occupied_beds = [
        edge[1]
        for edge in G.edges()
        if G.nodes[edge[0]]["type"] == "Patient" and G.nodes[edge[1]]["type"] == "Bed"
    ]
    available_beds = [bed for bed in beds if bed["id"] not in occupied_beds]

    if not available_beds:
        print(f"No available beds for patient {patient['name']}")
        # Add to waiting room
        waiting_room_queue.append(patient)
        G.add_edge(
            patient["id"], waiting_room["id"], relationship="waiting_in", weight=1
        )
        return None

    # For each available bed, check if the required resources are assigned to the room
    for bed in available_beds:
        room_id = bed["room_id"]
        # Check if the room has a doctor and nurse assigned
        room_doctors = [
            n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Doctor"
        ]
        room_nurses = [n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Nurse"]
        # Assume every patient requires a doctor and a nurse
        if room_doctors and room_nurses:
            # Assign the patient to this bed
            G.add_edge(patient["id"], bed["id"], relationship="assigned_to", weight=1)
            print(f"Assigned {patient['name']} to {bed['name']}")
            return bed["id"]

    # If no suitable bed found, add patient to waiting room
    print(
        f"No suitable beds with required resources available for patient {patient['name']}"
    )
    waiting_room_queue.append(patient)
    G.add_edge(patient["id"], waiting_room["id"], relationship="waiting_in", weight=1)
    return None


# Assign existing patients to beds (for initial setup)
for patient in patients:
    assigned_bed = assign_patient_to_bed(patient, G, beds)

# ---------------------------
# 4. Define Priority Calculation
# ---------------------------


def calculate_priority_score(patient):
    """
    Calculate a priority score for the patient based on severity and priority.
    Higher scores indicate higher priority.
    """
    # Map priority to a numerical value
    priority_mapping = {"Emergency": 3, "Surgery": 2, "Regular": 1}
    priority_score = priority_mapping.get(patient["priority"], 1)
    severity_score = patient[
        "severity"
    ]  # Assuming severity is from 1 (low) to 5 (high)

    total_score = priority_score * 10 + severity_score  # Weight priority higher
    return total_score


# ---------------------------
# 5. Simulate Time Steps
# ---------------------------


def simulate_time_step(G, doctors, nurses, patients, time_step=1):
    """
    Simulates a time step in the hospital.
    """
    print(f"\n--- Simulating time step of {time_step} hour(s) ---")

    # Sort patients based on priority score
    patients_sorted = sorted(
        patients, key=lambda p: calculate_priority_score(p), reverse=True
    )

    # Assign attention to patients
    for patient in patients_sorted:
        # Get the bed the patient is assigned to
        bed_id = None
        for edge in G.edges(patient["id"]):
            if G.nodes[edge[1]]["type"] == "Bed":
                bed_id = edge[1]
                break
        if not bed_id:
            continue  # Patient not assigned to a bed

        room_id = G.nodes[bed_id]["room_id"]

        # Get doctor and nurse in the room
        room_doctors = [
            n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Doctor"
        ]
        room_nurses = [n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Nurse"]

        # Assign doctor
        for doctor_id in room_doctors:
            doctor = G.nodes[doctor_id]
            if doctor["time_busy"] > 0:
                continue  # Doctor is busy
            if patient["needs_surgery"]:
                # Surgery takes full attention
                doctor["current_patients"].append(patient["id"])
                doctor["time_busy"] = time_step  # Busy for the entire time step
                print(f"{doctor['name']} is performing surgery on {patient['name']}")
                G.add_edge(doctor_id, patient["id"], relationship="attending", weight=1)
                break
            elif len(doctor["current_patients"]) < doctor["patients_per_hour"]:
                # Assign doctor to patient
                doctor["current_patients"].append(patient["id"])
                print(f"{doctor['name']} is attending to {patient['name']}")
                G.add_edge(
                    doctor_id,
                    patient["id"],
                    relationship="attending",
                    weight=1 / doctor["patients_per_hour"],
                )
                break

        # Assign nurse
        for nurse_id in room_nurses:
            nurse = G.nodes[nurse_id]
            if nurse["time_busy"] > 0:
                continue  # Nurse is busy
            if len(nurse["current_patients"]) < nurse["patients_per_hour"]:
                nurse["current_patients"].append(patient["id"])
                print(f"{nurse['name']} is attending to {patient['name']}")
                G.add_edge(
                    nurse_id,
                    patient["id"],
                    relationship="assisting",
                    weight=1 / nurse["patients_per_hour"],
                )
                break

    # Update time_busy for doctors and nurses
    for doctor in doctors:
        if doctor["time_busy"] > 0:
            doctor["time_busy"] -= time_step
            if doctor["time_busy"] <= 0:
                doctor["time_busy"] = 0
                doctor["current_patients"] = []
    for nurse in nurses:
        if nurse["time_busy"] > 0:
            nurse["time_busy"] -= time_step
            if nurse["time_busy"] <= 0:
                nurse["time_busy"] = 0
                nurse["current_patients"] = []

    # After time step, attempt to release patients
    released_patients = simulate_patient_release(G, patients)
    return released_patients


# ---------------------------
# 6. Simulate Patient Release
# ---------------------------


def simulate_patient_release(G, patients):
    released_patients = []
    for patient in patients:
        release_probability = calculate_release_probability(patient)
        if random.random() < release_probability:
            print(f"{patient['name']} has been treated and is ready for release.")
            release_patient(G, patient)
            released_patients.append(patient)
    return released_patients


def calculate_release_probability(patient):
    """
    Calculates the probability that a patient can be released after a time step.
    """
    base_prob = 0.1  # Base probability
    severity_modifier = (
        5 - patient["severity"]
    ) * 0.15  # Higher severity, lower probability
    if patient["needs_surgery"]:
        surgery_modifier = (
            -0.2
        )  # Surgery patients are less likely to be released immediately
    else:
        surgery_modifier = 0
    total_probability = base_prob + severity_modifier + surgery_modifier
    total_probability = max(min(total_probability, 1.0), 0.0)  # Clamp between 0 and 1
    return total_probability


def release_patient(G, patient):
    # Remove patient from bed
    bed_id = None
    for edge in G.edges(patient["id"]):
        if G.nodes[edge[1]]["type"] == "Bed":
            bed_id = edge[1]
            break
    if bed_id:
        G.remove_edge(patient["id"], bed_id)
        print(f"{patient['name']} has been released from {G.nodes[bed_id]['name']}")

    # Remove relationships with doctors and nurses
    for neighbor in list(G.neighbors(patient["id"])):
        G.remove_edge(patient["id"], neighbor)
    # Remove patient node
    G.remove_node(patient["id"])


# ---------------------------
# 7. Main Simulation Loop
# ---------------------------

# Simulate over multiple time steps
time_steps = 5  # Number of hours to simulate
for t in range(time_steps):
    print(f"\n--- Hour {t+1} ---")
    # Simulate time step
    released_patients = simulate_time_step(G, doctors, nurses, patients)
    # Remove released patients from the list
    patients = [p for p in patients if p not in released_patients]
    # Assign waiting patients if beds become available
    if waiting_room_queue:
        for patient in list(waiting_room_queue):
            assigned_bed = assign_patient_to_bed(patient, G, beds)
            if assigned_bed:
                waiting_room_queue.remove(patient)
                patients.append(patient)
    # Break if no patients left
    if not patients and not waiting_room_queue:
        print("All patients have been treated and released.")
        break

# ---------------------------
# 8. Detect and Print Resource Strain
# ---------------------------


def detect_resource_strain(G):
    strained_resources = []

    for node_id, data in G.nodes(data=True):
        if data["type"] == "Doctor":
            if len(data["current_patients"]) >= data["patients_per_hour"]:
                strained_resources.append((node_id, data["name"], data["type"]))
        elif data["type"] == "Nurse":
            if len(data["current_patients"]) >= data["patients_per_hour"]:
                strained_resources.append((node_id, data["name"], data["type"]))

    return strained_resources


# Detect resource strain
strained_resources = detect_resource_strain(G)
print("\nResources experiencing strain:")
for node_id, name, res_type in strained_resources:
    print(f"  {name} ({res_type})")

# ---------------------------
# 9. Export Graph Data
# ---------------------------

# Convert the graph to node-link data format
graph_data = json_graph.node_link_data(G)

# Convert the dictionary to a JSON object
graph_json = json.dumps(graph_data, indent=4)

# Save the JSON to a file
with open("./data/graph_data.json", "w") as f:
    f.write(graph_json)

# Combine doctors, nurses, and equipment into a single resources dictionary
resources = {"doctors": doctors, "nurses": nurses, "equipment": equipment}

# Save the resources to a separate JSON file
with open("./data/resources_backend.json", "w") as f:
    json.dump(resources, f, indent=4)

print("Resources have been saved to resources_backend.json")
print("Graph exported to graph_data.json")
