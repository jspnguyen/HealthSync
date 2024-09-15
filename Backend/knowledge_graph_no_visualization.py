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
    },
    {
        "id": "D2",
        "type": "Doctor",
        "specialty": "Orthopedics",
        "patients_per_hour": 6,
        "name": "Dr. Bone",
        "current_patients": [],
    },
    {
        "id": "D3",
        "type": "Doctor",
        "specialty": "General Surgery",
        "patients_per_hour": 6,
        "name": "Dr. Surgeon",
        "current_patients": [],
    },
    {
        "id": "D4",
        "type": "Doctor",
        "specialty": "Emergency Medicine",
        "patients_per_hour": 6,
        "name": "Dr. Swift",
        "current_patients": [],
    },
    {
        "id": "D5",
        "type": "Doctor",
        "specialty": "Neurology",
        "patients_per_hour": 6,
        "name": "Dr. Brain",
        "current_patients": [],
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
    {"id": "E1", "type": "Equipment", "scarcity": 1, "name": "Defibrillator"},
    {"id": "E2", "type": "Equipment", "scarcity": 3, "name": "X-Ray Machine"},
    {"id": "E3", "type": "Equipment", "scarcity": 2, "name": "MRI Scanner"},
    {"id": "E4", "type": "Equipment", "scarcity": 4, "name": "Ventilator"},
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

# Add Equipment to the graph (initially not assigned)
for eq in equipment:
    G.add_node(eq["id"], **eq)

# ---------------------------
# 2. Assign Patients to Beds
# ---------------------------


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
        if node["type"] in ["Doctor", "Nurse"] and len(node["current_patients"]) == 0:
            G.remove_node(node_id)

    # Assign doctors to patients
    for patient in patients:
        # Skip if patient already has a doctor assigned
        existing_doctors = [
            n for n in G.neighbors(patient["id"]) if G.nodes[n]["type"] == "Doctor"
        ]
        if existing_doctors:
            continue

        # Find an available doctor
        for doctor in doctors:
            if len(doctor["current_patients"]) < doctor["patients_per_hour"]:
                doctor["current_patients"].append(patient["id"])
                G.add_node(doctor["id"], **doctor)  # Add doctor to graph if not present
                G.add_edge(
                    doctor["id"], patient["id"], relationship="attending", weight=1
                )
                print(f"{doctor['name']} is attending to {patient['name']}")
                break
        else:
            print(f"No available doctors for {patient['name']}")

    # Assign nurses to patients
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
# 4. Assign Equipment to Patients
# ---------------------------


def assign_equipment_to_patients(G, equipment, patients):
    """
    Assigns equipment to patients based on availability.
    """
    for patient in patients:
        # Assume patients needing surgery require specific equipment
        required_equipment = []
        if patient["needs_surgery"]:
            required_equipment = [eq for eq in equipment if eq["name"] == "MRI Scanner"]
        else:
            required_equipment = [eq for eq in equipment if eq["name"] == "Ventilator"]

        for eq in required_equipment:
            if eq["available"]:
                eq["available"] = False
                G.add_edge(eq["id"], patient["id"], relationship="used_by", weight=1)
                print(f"Assigned {eq['name']} to {patient['name']}")
                break
        else:
            print(f"No available equipment for {patient['name']}")


assign_equipment_to_patients(G, equipment, patients)

# ---------------------------
# 5. Define Priority Calculation
# ---------------------------


def calculate_priority_score(patient):
    """
    Calculate a priority score for the patient based on severity and priority.
    Higher scores indicate higher priority.
    """
    priority_mapping = {"Emergency": 3, "Surgery": 2, "Regular": 1}
    priority_score = priority_mapping.get(patient["priority"], 1)
    severity_score = patient["severity"]

    total_score = priority_score * 10 + severity_score
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
    assign_equipment_to_patients(G, equipment, patients_sorted)

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
        if staff["type"] in ["Doctor", "Nurse"]:
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
time_steps = 5  # Number of hours to simulate
for t in range(time_steps):
    print(f"\n--- Hour {t+1} ---")
    # Simulate time step
    released_patients = simulate_time_step(G, doctors, nurses, patients, equipment)
    # Remove released patients from the list
    patients = [p for p in patients if p not in released_patients]
    # Break if no patients left
    if not patients:
        print("All patients have been treated and released.")
        break

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
