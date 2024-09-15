import networkx as nx
import random
import json
from networkx.readwrite import json_graph

# Initialize the knowledge graph
G = nx.Graph()

# ---------------------------
# 1. Add Nodes (Patients, Doctors, Nurses, Beds, Equipment)
# ---------------------------

# Define Patients
patients = [
    {
        "id": "P1",
        "type": "Patient",
        "priority_score": 0,  # Start with priority score of 0
        "severity": 5,  # Severity on a scale of 1-10
        "name": "John Doe",
        "needs_surgery": False,
        "time_waiting": 0,  # Initialize waiting time to 0
    },
    {
        "id": "P2",
        "type": "Patient",
        "priority_score": 0,  # Start with priority score of 0
        "severity": 2,  # Severity on a scale of 1-10
        "name": "Jane Smith",
        "needs_surgery": False,
        "time_waiting": 0,  # Initialize waiting time to 0
    },
    {
        "id": "P3",
        "priority_score": 0,  # Start with priority score of 0
        "type": "Patient",
        "severity": 4,  # Severity on a scale of 1-10
        "name": "Alice Johnson",
        "needs_surgery": True,
        "time_waiting": 0,  # Initialize waiting time to 0
    },
    {
        "id": "P4",
        "type": "Patient",
        "priority_score": 0,  # Start with priority score of 0
        "severity": 4,  # Severity on a scale of 1-10
        "name": "Bob Brown",
        "needs_surgery": False,
        "time_waiting": 0,  # Initialize waiting time to 0
    },
]

# Define Doctors
doctors = [
    {
        "id": "D1",
        "type": "Doctor",
        "specialty": "Cardiology",
        "patients_per_hour": 5,
        "name": "Dr. Heart",
        "current_patients": [],
        "attention_allocated": 0.0,
    },
    {
        "id": "D2",
        "type": "Doctor",
        "specialty": "Orthopedics",
        "patients_per_hour": 5,
        "name": "Dr. Bone",
        "current_patients": [],
        "attention_allocated": 0.0,
    },
    {
        "id": "D3",
        "type": "Doctor",
        "specialty": "General Surgery",
        "patients_per_hour": 5,
        "name": "Dr. Surgeon",
        "current_patients": [],
        "attention_allocated": 0.0,
    },
    {
        "id": "D4",
        "type": "Doctor",
        "specialty": "Emergency Medicine",
        "patients_per_hour": 5,
        "name": "Dr. Swift",
        "current_patients": [],
        "attention_allocated": 0.0,
    },
    {
        "id": "D5",
        "type": "Doctor",
        "specialty": "Neurology",
        "patients_per_hour": 5,
        "name": "Dr. Brain",
        "current_patients": [],
        "attention_allocated": 0.0,
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
    },
    {
        "id": "N2",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Anna",
        "current_patients": [],
    },
    {
        "id": "N3",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Sam",
        "current_patients": [],
    },
    {
        "id": "N4",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Kim",
        "current_patients": [],
    },
    {
        "id": "N5",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Lee",
        "current_patients": [],
    },
    {
        "id": "N6",
        "type": "Nurse",
        "patients_per_hour": 3,
        "name": "Nurse Pat",
        "current_patients": [],
    },
]

# Define Equipment (Multiple instances of the same equipment type)
equipment_list = [
    {"id": "E1", "type": "Equipment", "scarcity": 3, "name": "Ventilator"},
    {"id": "E2", "type": "Equipment", "scarcity": 2, "name": "Defibrillator"},
    {"id": "E3", "type": "Equipment", "scarcity": 4, "name": "ECG Monitor"},
    {"id": "E4", "type": "Equipment", "scarcity": 2, "name": "Ultrasound Machine"},
    {"id": "E5", "type": "Equipment", "scarcity": 5, "name": "Wheelchair"},
]

# Create multiple instances of equipment types
equipment = []
for eq in equipment_list:
    for i in range(eq["scarcity"]):
        equipment.append(
            {
                "id": f"{eq['id']}_{i+1}",
                "type": "Equipment",
                "name": eq["name"],
                "original_id": eq["id"],
                "available": True,
            }
        )

# Generate Beds
beds = []
for i in range(1, 11):
    bed = {
        "id": f"B{i}",
        "type": "Bed",
        "name": f"Bed {i}",
    }
    beds.append(bed)

# Add Patients and Beds to the graph
for entity in patients + beds:
    G.add_node(entity["id"], **entity)

# Define rooms
rooms = []
for i in range(1, 4):  # Assume we have 3 rooms
    room = {
        "id": f"Room{i}",
        "type": "Room",
        "name": f"Room {i}",
    }
    rooms.append(room)

# Define the waiting room
waiting_room = {
    "id": "WaitingRoom",
    "type": "WaitingRoom",
    "name": "Hospital Waiting Room",
}

# Add rooms and waiting room to the graph
G.add_node(waiting_room["id"], **waiting_room)
for room in rooms:
    G.add_node(room["id"], **room)
    G.add_edge(waiting_room["id"], room["id"], relationship="contains", weight=1)

# Add beds and assign them to rooms
beds_per_room = len(beds) // len(rooms)  # Integer division
extra_beds = len(beds) % len(rooms)  # Beds that remain after even division

room_index = 0
for i, bed in enumerate(beds):
    # After evenly distributing the beds, allocate the extra beds to rooms
    if i >= (room_index + 1) * beds_per_room + min(room_index, extra_beds):
        room_index += 1

    room_id = rooms[room_index]["id"]
    G.add_node(bed["id"], **bed)
    G.add_edge(room_id, bed["id"], relationship="contains", weight=1)

# ---------------------------
# Add Patients, Doctors, and Nurses to the graph
# ---------------------------

# Add Patients, Doctors, and Nurses
for entity in patients + doctors + nurses:
    G.add_node(entity["id"], **entity)

# ---------------------------
# 2. Assign Patients to Beds
# ---------------------------


def add_patient_to_graph(
    G, patient_id, name, severity, needs_surgery, required_equipment_names
):
    """
    Adds a patient to the graph with all necessary attributes and assigns required equipment.

    Parameters:
    - G: The graph.
    - patient_id: Unique ID for the patient.
    - name: Name of the patient.
    - severity: Severity of the patient's condition (1-10 scale).
    - needs_surgery: Boolean, if the patient requires surgery.
    - required_equipment_names: List of equipment names required for this patient.
    """

    # Create the patient node with a default priority score of 0
    patient = {
        "id": patient_id,
        "type": "Patient",
        "priority_score": 0,  # Default priority score (increases over time)
        "severity": severity,  # Severity on a scale from 1 to 10
        "name": name,
        "needs_surgery": needs_surgery,
        "time_waiting": 0,  # Track how long the patient has been waiting
    }

    G.add_node(patient_id, **patient)
    print(
        f"Patient {name} added with severity {severity} and default priority score 0."
    )

    # Assign required equipment to the patient and add equipment to the graph
    for equipment_name in required_equipment_names:
        available_equipment = [
            eq for eq in equipment if eq["name"] == equipment_name and eq["available"]
        ]

        if available_equipment:
            assigned_equipment = available_equipment[0]
            assigned_equipment["available"] = False  # Mark equipment as unavailable
            G.add_node(assigned_equipment["id"], **assigned_equipment)
            G.add_edge(
                assigned_equipment["id"],
                patient_id,
                relationship="used_by",
                weight=1,
            )
            print(f"Assigned {assigned_equipment['name']} to {name}.")
        else:
            print(f"No available {equipment_name} for patient {name}.")

    # Assign the patient to an available bed
    assign_patient_to_bed(patient, G, beds)


def assign_patient_to_bed(patient, G, beds):
    """
    Assigns a patient to a bed.
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
        return False

    # Assign the patient to the first available bed
    bed = available_beds[0]
    G.add_edge(patient["id"], bed["id"], relationship="assigned_to", weight=1)
    print(f"Assigned {patient['name']} to {bed['name']}")
    return True


# Assign existing patients to beds
for patient in patients:
    assign_patient_to_bed(patient, G, beds)

# ---------------------------
# 3. Assign Doctors and Nurses to Patients
# ---------------------------


def assign_medical_staff_to_patients(G, doctors, nurses, patients):
    """
    Assigns doctors and nurses directly to patients based on availability and capacity.
    """
    # Remove idle doctors and nurses from the graph
    for node_id in list(G.nodes()):
        node = G.nodes[node_id]
        if node["type"] == "Doctor" and len(node["current_patients"]) == 0:
            G.remove_node(node_id)
            node["attention_allocated"] = 0.0  # Reset attention allocated
        elif node["type"] == "Nurse" and len(node["current_patients"]) == 0:
            G.remove_node(node_id)

    # Assign doctors to patients
    for patient in patients:
        # Skip if patient already has a doctor assigned
        existing_doctors = [
            n for n in G.neighbors(patient["id"]) if G.nodes[n]["type"] == "Doctor"
        ]
        if existing_doctors:
            continue

        # If patient needs surgery
        if patient["needs_surgery"]:
            # Find a doctor who is not assigned to any other patients
            for doctor in doctors:
                if len(doctor["current_patients"]) == 0:
                    # Assign doctor to patient
                    doctor["current_patients"].append(patient["id"])
                    doctor["attention_allocated"] = 1.0  # Full attention
                    G.add_node(
                        doctor["id"], **doctor
                    )  # Add doctor to graph if not present
                    G.add_edge(
                        doctor["id"],
                        patient["id"],
                        relationship="attending",
                        attention=1.0,
                    )
                    print(
                        f"{doctor['name']} is performing surgery on {patient['name']}"
                    )
                    break
            else:
                print(f"No available doctors for surgery for {patient['name']}")
        else:
            # Patient does not need surgery
            # Find an available doctor
            assigned = False
            for doctor in doctors:
                attention_per_patient = 1.0 / doctor["patients_per_hour"]
                if doctor[
                    "attention_allocated"
                ] + attention_per_patient <= 1.0 and not any(
                    G.nodes[patient_id]["needs_surgery"]
                    for patient_id in doctor["current_patients"]
                ):
                    # Assign doctor to patient
                    doctor["current_patients"].append(patient["id"])
                    doctor["attention_allocated"] += attention_per_patient
                    G.add_node(
                        doctor["id"], **doctor
                    )  # Add doctor to graph if not present
                    G.add_edge(
                        doctor["id"],
                        patient["id"],
                        relationship="attending",
                        attention=attention_per_patient,
                    )
                    print(
                        f"{doctor['name']} is attending to {patient['name']} with attention {attention_per_patient}"
                    )
                    assigned = True
                    break
            if not assigned:
                print(f"No available doctors for {patient['name']}")

    # Assign nurses to patients (keeping original logic)
    for patient in patients:
        # Skip if patient already has a nurse assigned
        existing_nurses = [
            n for n in G.neighbors(patient["id"]) if G.nodes[n]["type"] == "Nurse"
        ]
        if existing_nurses:
            continue

        # Find an available nurse
        for nurse in nurses:
            if len(nurse["current_patients"]) < nurse["patients_per_hour"]:
                nurse["current_patients"].append(patient["id"])
                G.add_node(nurse["id"], **nurse)  # Add nurse to graph if not present
                G.add_edge(
                    nurse["id"], patient["id"], relationship="assisting", weight=1
                )
                print(f"{nurse['name']} is assisting {patient['name']}")
                break
        else:
            print(f"No available nurses for {patient['name']}")


assign_medical_staff_to_patients(G, doctors, nurses, patients)

# ---------------------------
# 4. Assign Equipment to Patients (Equipment added only in add_patient_to_graph)
# ---------------------------

# ---------------------------
# 5. Define Priority Calculation
# ---------------------------


def calculate_priority_score(patient):
    """
    Calculate a total priority score for the patient.
    The score is based on how long the patient has been waiting and their severity.
    Severity holds a higher precedence than waiting time.
    """
    # Weight for severity and waiting time
    severity_weight = 2  # Give severity higher precedence (multiply by 2)
    waiting_time_weight = 1  # Waiting time is weighted less

    # Calculate the priority score based on severity and waiting time
    severity_score = (
        patient["severity"] * severity_weight
    )  # Higher severity increases the score
    waiting_time_score = (
        patient["time_waiting"] * waiting_time_weight
    )  # Increase score as they wait longer

    # Total priority score
    total_score = severity_score + waiting_time_score

    return total_score


# ---------------------------
# 6. Simulate Time Steps
# ---------------------------


def simulate_time_step(G, doctors, nurses, patients, equipment, time_step=1):
    """
    Simulates a time step in the hospital.
    """
    print(f"\n--- Simulating time step of {time_step} hour(s) ---")

    # Sort patients based on priority score
    patients_sorted = sorted(
        patients, key=lambda p: calculate_priority_score(p), reverse=True
    )

    # Update medical staff assignments
    assign_medical_staff_to_patients(G, doctors, nurses, patients_sorted)

    # After time step, attempt to release patients
    released_patients = simulate_patient_release(G, patients, equipment)
    return released_patients


# ---------------------------
# 7. Simulate Patient Release
# ---------------------------


def simulate_patient_release(G, patients, equipment):
    released_patients = []
    for patient in patients:
        release_probability = calculate_release_probability(patient)
        if random.random() < release_probability:
            print(f"{patient['name']} has been treated and is ready for release.")
            release_patient(G, patient, equipment)
            released_patients.append(patient)
    return released_patients


def calculate_release_probability(patient):
    base_prob = 0.1
    severity_modifier = (5 - patient["severity"]) * 0.15
    surgery_modifier = -0.2 if patient["needs_surgery"] else 0
    total_probability = base_prob + severity_modifier + surgery_modifier
    total_probability = max(min(total_probability, 1.0), 0.0)
    return total_probability


def release_patient(G, patient, equipment):
    # Remove patient from bed
    bed_id = None
    for edge in G.edges(patient["id"]):
        if G.nodes[edge[1]]["type"] == "Bed":
            bed_id = edge[1]
            break
    if bed_id:
        G.remove_edge(patient["id"], bed_id)
        print(f"{patient['name']} has been released from {G.nodes[bed_id]['name']}")

    # Free up equipment
    for edge in list(G.edges(patient["id"])):
        neighbor_id = edge[1]
        if G.nodes[neighbor_id]["type"] == "Equipment":
            eq = G.nodes[neighbor_id]
            eq["available"] = True
            G.remove_edge(patient["id"], neighbor_id)
            print(f"Equipment {eq['name']} is now available")

    # Remove relationships with doctors and nurses
    for edge in list(G.edges(patient["id"])):
        staff_id = edge[1]
        staff = G.nodes[staff_id]
        if staff["type"] == "Doctor":
            staff["current_patients"].remove(patient["id"])
            # Update attention_allocated
            attention = G.edges[staff_id, patient["id"]]["attention"]
            staff["attention_allocated"] -= attention
            G.remove_edge(staff_id, patient["id"])
            # Remove staff from graph if they have no patients
            if len(staff["current_patients"]) == 0:
                G.remove_node(staff_id)
                staff["attention_allocated"] = 0.0  # Reset attention allocated
                print(
                    f"{staff['type']} {staff['name']} is now idle and removed from the graph"
                )
        elif staff["type"] == "Nurse":
            staff["current_patients"].remove(patient["id"])
            G.remove_edge(staff_id, patient["id"])
            # Remove staff from graph if they have no patients
            if len(staff["current_patients"]) == 0:
                G.remove_node(staff_id)
                print(
                    f"{staff['type']} {staff['name']} is now idle and removed from the graph"
                )

    # Remove patient node
    G.remove_node(patient["id"])


# ---------------------------
# 8. Main Simulation Loop
# ---------------------------

# Simulate over multiple time steps
# time_steps = 2  # Number of hours to simulate
# for t in range(time_steps):
#     print(f"\n--- Hour {t+1} ---")
#     # Simulate time step
#     released_patients = simulate_time_step(G, doctors, nurses, patients, equipment)
#     # Remove released patients from the list
#     patients = [p for p in patients if p not in released_patients]
#     # Break if no patients left
#     if not patients:
#         print("All patients have been treated and released.")
#         break

# # ---------------------------
# # 9. Export Graph Data
# # ---------------------------

# # Convert the graph to node-link data format
# graph_data = json_graph.node_link_data(G)

# # Convert the dictionary to a JSON object
# graph_json = json.dumps(graph_data, indent=4)

# # Save the JSON to a file
# with open("./data/graph_data.json", "w") as f:
#     f.write(graph_json)

# # Combine doctors, nurses, and equipment into a single resources dictionary
# resources = {"doctors": doctors, "nurses": nurses, "equipment": equipment}

# # Save the resources to a separate JSON file
# with open("./data/resources_backend.json", "w") as f:
#     json.dump(resources, f, indent=4)

# print("Resources have been saved to resources_backend.json")
# print("Graph exported to graph_data.json")
