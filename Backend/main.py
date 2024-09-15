import networkx as nx
import random
import json
from networkx.readwrite import json_graph
import names
import time
import logging
import requests
from pydantic import BaseModel


# ==================================================================
# Hospital Simulation Using NetworkX
# ==================================================================
# This script simulates a hospital environment, dynamically generating
# doctors, nurses, beds, rooms, and equipment based on user input.
# It manages patient admissions, assignments, releases, and maintains
# counters for all entities and patients.
# ==================================================================
class Counts(BaseModel):
    total_doctors: int
    available_doctors: int
    total_nurses: int
    available_nurses: int
    total_equipment: int
    available_equipment: int
    patients_being_treated: int
    patients_in_waiting_room: int
    available_beds: int


# Initialize the knowledge graph
G = nx.Graph()

# Global Registries
all_doctors = {}
all_nurses = {}
all_equipment = {}

# ---------------------------
# Global Counters
# ---------------------------

# Entity Counters
total_doctors = 0
total_nurses = 0
total_beds = 0
total_rooms = 0
total_equipment = 0

# Patient Counters
total_patients = 0
patients_in_waiting_room = 0

# Unique ID Counters for Entities
global doctor_id_counter
doctor_id_counter = 0
nurse_id_counter = 0
bed_id_counter = 0
room_id_counter = 0
equipment_id_counter = 0
patient_id_counter = 0

# ---------------------------
# Entity Generation Functions
# ---------------------------


def generate_doctors(n):
    """
    Generates 'n' doctors with unique IDs and random specialties.
    Updates the global doctor counter.
    """
    global total_doctors, doctor_id_counter, all_doctors
    specialties = [
        "Cardiology",
        "Orthopedics",
        "General Surgery",
        "Emergency Medicine",
        "Neurology",
        "Pediatrics",
        "Oncology",
        "Radiology",
        "Dermatology",
        "Psychiatry",
    ]
    for _ in range(n):
        doctor_id_counter += 1
        doctor_id = f"D{doctor_id_counter}"
        doctor = {
            "id": doctor_id,
            "type": "Doctor",
            "specialty": random.choice(specialties),
            "patients_per_hour": 6,  # Doctors can see up to 6 patients per hour
            "name": f"Dr. {names.get_first_name()}",
            "current_patients": [],
            "attention_allocated": 0.0,
        }
        all_doctors[doctor_id] = doctor
        total_doctors += 1
    print(f"Generated {n} doctors. Total Doctors: {total_doctors}")


def generate_nurses(n):
    global total_nurses, nurse_id_counter, all_nurses
    for _ in range(n):
        nurse_id_counter += 1
        nurse_id = f"N{nurse_id_counter}"
        nurse = {
            "id": nurse_id,
            "type": "Nurse",
            "patients_per_hour": 3,  # Nurses can monitor up to 3 patients at a time
            "name": f"Nurse {names.get_first_name()}",
            "current_patients": [],
        }
        # Do not add to graph here
        all_nurses[nurse_id] = nurse
        total_nurses += 1
    print(f"Generated {n} nurses. Total Nurses: {total_nurses}")


def generate_beds(n):
    """
    Generates 'n' beds with unique IDs.
    Updates the global bed counter.
    """
    global total_beds, bed_id_counter
    for _ in range(n):
        bed_id_counter += 1
        bed_id = f"B{bed_id_counter}"
        bed = {
            "id": bed_id,
            "type": "Bed",
            "name": f"Bed {bed_id_counter}",
        }
        G.add_node(bed_id, **bed)
        total_beds += 1
    print(f"Generated {n} beds. Total Beds: {total_beds}")


def generate_rooms(n):
    """
    Generates 'n' rooms with unique IDs and connects them to the waiting room.
    Updates the global room counter.
    """
    global total_rooms, room_id_counter

    # Ensure the waiting room exists
    if "WaitingRoom" not in G.nodes:
        waiting_room = {
            "id": "WaitingRoom",
            "type": "WaitingRoom",
            "name": "Hospital Waiting Room",
        }
        G.add_node(waiting_room["id"], **waiting_room)
        print("Waiting Room created.")

    # Generate rooms and connect them to the waiting room
    for _ in range(n):
        room_id_counter += 1
        room_id = f"Room{room_id_counter}"
        room = {
            "id": room_id,
            "type": "Room",
            "name": f"Room {room_id_counter}",
        }
        G.add_node(room_id, **room)

        # Attach the room to the waiting room
        G.add_edge("WaitingRoom", room_id, relationship="contains", weight=1)

        total_rooms += 1
        print(f"Generated {room['name']} and attached it to the Waiting Room.")

    print(f"Total rooms generated: {n}, all connected to the Waiting Room.")


def generate_equipment(n):
    global total_equipment, equipment_id_counter, all_equipment
    equipment_types = [
        "Ventilator",
        "Defibrillator",
        "ECG Monitor",
        "Ultrasound Machine",
        "Wheelchair",
        "X-Ray Machine",
        "MRI Scanner",
        "Infusion Pump",
        "Syringe Pump",
        "Dialysis Machine",
    ]
    for _ in range(n):
        equipment_id_counter += 1
        equipment_id = f"E{equipment_id_counter}"
        equipment = {
            "id": equipment_id,
            "type": "Equipment",
            "name": random.choice(equipment_types),
            "original_id": equipment_id,
            "available": True,
        }
        # Do not add to graph here
        all_equipment[equipment_id] = equipment
        total_equipment += 1
    print(f"Generated {n} equipment items. Total Equipment: {total_equipment}")


# ---------------------------
# Assign Beds to Rooms
# ---------------------------


def assign_beds_to_rooms():
    """
    Assigns beds to rooms evenly. Extra beds are distributed one by one to the first few rooms.
    """
    rooms = [node for node, attr in G.nodes(data=True) if attr["type"] == "Room"]
    beds = [node for node, attr in G.nodes(data=True) if attr["type"] == "Bed"]
    beds_per_room = len(beds) // len(rooms) if rooms else 0
    extra_beds = len(beds) % len(rooms) if rooms else 0

    bed_index = 0
    for room_index, room in enumerate(rooms):
        num_beds = beds_per_room + (1 if room_index < extra_beds else 0)
        for _ in range(num_beds):
            if bed_index < len(beds):
                bed = beds[bed_index]
                G.add_edge(room, bed, relationship="contains", weight=1)
                bed_index += 1
    print(f"Assigned {len(beds)} beds to {len(rooms)} rooms.")


# ---------------------------
# Define the Waiting Room
# ---------------------------

waiting_room = {
    "id": "WaitingRoom",
    "type": "WaitingRoom",
    "name": "Hospital Waiting Room",
}

G.add_node(waiting_room["id"], **waiting_room)
for room in [node for node, attr in G.nodes(data=True) if attr["type"] == "Room"]:
    G.add_edge(waiting_room["id"], room, relationship="contains", weight=1)
print("Waiting Room created and connected to all rooms.")

# ---------------------------
# Patient Management Functions
# ---------------------------


def add_patient_to_graph(name, severity, needs_surgery, required_equipment_name=None):
    """
    Adds a patient to the graph with necessary attributes and assigns them to a bed or waiting room.
    Assigns equipment only if the patient is placed in a bed.
    Updates patient counters accordingly.

    Parameters:
    - name: Name of the patient.
    - severity: Severity of the patient's condition (1-10 scale).
    - needs_surgery: Boolean, if the patient requires surgery.
    - required_equipment_name: Name of the equipment required, if any.
    """
    global total_patients, patients_in_waiting_room, patient_id_counter

    patient_id_counter += 1
    patient_id = f"P{patient_id_counter}"
    patient = {
        "id": patient_id,
        "type": "Patient",
        "priority_score": 0,  # Default priority score (increases over time)
        "severity": severity,  # Severity on a scale from 1 to 10
        "name": name,
        "needs_surgery": needs_surgery,
        "time_waiting": 0,  # Track how long the patient has been waiting
        "required_equipment": (
            required_equipment_name if required_equipment_name else None
        ),
    }

    G.add_node(patient_id, **patient)
    total_patients += 1
    print(f"Patient {name} (ID: {patient_id}) added with severity {severity}.")

    # Assign the patient to an available bed or waiting room
    assigned_bed = assign_patient_to_bed(patient)
    if assigned_bed:
        # Assign required equipment if needed
        if patient["required_equipment"]:
            assign_equipment_to_patient(patient, assigned_bed)
    else:
        # Add patient to waiting room
        G.add_edge("WaitingRoom", patient_id, relationship="waiting", weight=1)
        patients_in_waiting_room += 1
        print(
            f"Patient {name} is in the waiting room. Total Patients in Waiting Room: {patients_in_waiting_room}"
        )


def assign_patient_to_bed(patient):
    """
    Assigns a patient to the first available bed.
    Returns the assigned bed node if successful, else None.
    """
    global total_beds, patients_in_waiting_room

    # Find all beds
    beds = [node for node, attr in G.nodes(data=True) if attr["type"] == "Bed"]
    for bed in beds:
        # Check if bed is occupied
        occupied = False
        for neighbor in G.neighbors(bed):
            if G.nodes[neighbor]["type"] == "Patient":
                occupied = True
                break
        if not occupied:
            # Assign patient to this bed
            G.add_edge(patient["id"], bed, relationship="assigned_to", weight=1)
            total_beds -= 1
            print(
                f"Assigned patient {patient['name']} to {G.nodes[bed]['name']}. Available beds: {total_beds}"
            )
            return bed
    # No beds available
    return None


def assign_equipment_to_patient(patient, bed):
    """
    Assigns required equipment to a patient who has been placed in a bed.
    """
    equipment_name = patient["required_equipment"]
    if not equipment_name:
        return

    # Find available equipment of the required type
    available_equipment = [
        (equipment_id, equipment_data)
        for equipment_id, equipment_data in all_equipment.items()
        if equipment_data["name"] == equipment_name and equipment_data["available"]
    ]

    if available_equipment:
        equipment_id, equipment_data = available_equipment[0]
        # Add equipment node to graph if not already present
        if equipment_id not in G.nodes:
            G.add_node(equipment_id, **equipment_data)
        # Assign equipment to patient
        G.add_edge(equipment_id, patient["id"], relationship="used_by", weight=1)
        equipment_data["available"] = False
        print(
            f"Assigned equipment {equipment_data['name']} to patient {patient['name']}."
        )
    else:
        print(
            f"No available equipment of type {equipment_name} for patient {patient['name']}."
        )


def get_patients_in_beds():
    """
    Retrieves all patients currently assigned to beds.
    """
    patients_in_beds_ids = [
        node1 if G.nodes[node1]["type"] == "Patient" else node2
        for node1, node2 in G.edges()
        if (
            (G.nodes[node1]["type"] == "Patient" and G.nodes[node2]["type"] == "Bed")
            or (G.nodes[node1]["type"] == "Bed" and G.nodes[node2]["type"] == "Patient")
        )
    ]
    patients_in_beds = [G.nodes[pid] for pid in patients_in_beds_ids]
    return patients_in_beds


def get_patients_in_waiting_room():
    """
    Retrieves all patients currently in the waiting room.
    """
    waiting_patients_ids = [
        n for n in G.neighbors("WaitingRoom") if G.nodes[n].get("type") == "Patient"
    ]
    waiting_patients = [G.nodes[pid] for pid in waiting_patients_ids]
    return waiting_patients


def calculate_priority_score(patient):
    """
    Calculates a priority score based on severity and waiting time.
    Severity has higher weight.
    """
    severity_weight = 2
    waiting_time_weight = 1
    return (patient["severity"] * severity_weight) + (
        patient["time_waiting"] * waiting_time_weight
    )


def assign_medical_staff_to_patients(patients):
    """
    Assigns available doctors and nurses to patients based on availability and capacity.
    """
    # Assign doctors
    for patient in patients:
        # Check if patient already has a doctor
        has_doctor = any(
            G.nodes[neighbor]["type"] == "Doctor"
            for neighbor in G.neighbors(patient["id"])
        )
        if has_doctor:
            continue  # Skip if already has a doctor

        if patient["needs_surgery"]:
            # Surgery requires full attention (1.0)
            available_doctors = [
                (doctor_id, doctor_data)
                for doctor_id, doctor_data in all_doctors.items()
                if (
                    doctor_id not in G.nodes
                    or doctor_data["attention_allocated"] == 0.0
                )
                and doctor_data["specialty"]
                in ["General Surgery", "Emergency Medicine"]
                and doctor_data["attention_allocated"] == 0.0  # Ensure doctor is idle
            ]
            if available_doctors:
                doctor_id, doctor_data = available_doctors[0]
                # Add doctor node to graph
                if doctor_id not in G.nodes:
                    G.add_node(doctor_id, **doctor_data)
                G.add_edge(
                    doctor_id, patient["id"], relationship="attending", attention=1.0
                )
                doctor_data["current_patients"].append(patient["id"])
                doctor_data["attention_allocated"] = 1.0
                print(
                    f"{doctor_data['name']} is performing surgery on {patient['name']}."
                )
            else:
                print(f"No available surgeons for patient {patient['name']}.")
        else:
            # Non-surgery patients
            available_doctors = [
                (doctor_id, doctor_data)
                for doctor_id, doctor_data in all_doctors.items()
                if doctor_data["attention_allocated"] < 1.0
            ]
            # Sort doctors by least attention allocated to balance load
            available_doctors.sort(key=lambda x: x[1]["attention_allocated"])
            assigned = False
            for doctor_id, doctor_data in available_doctors:
                attention_needed = 1.0 / doctor_data["patients_per_hour"]
                if doctor_data["attention_allocated"] + attention_needed <= 1.0:
                    if doctor_id not in G.nodes:
                        G.add_node(doctor_id, **doctor_data)
                    G.add_edge(
                        doctor_id,
                        patient["id"],
                        relationship="attending",
                        attention=attention_needed,
                    )
                    doctor_data["current_patients"].append(patient["id"])
                    doctor_data["attention_allocated"] += attention_needed
                    print(
                        f"{doctor_data['name']} is attending to {patient['name']} with attention {attention_needed:.2f}."
                    )
                    assigned = True
                    break
            if not assigned:
                print(f"No available doctors for patient {patient['name']}.")

    # Assign nurses
    for patient in patients:
        # Check if patient already has a nurse
        has_nurse = any(
            G.nodes[neighbor]["type"] == "Nurse"
            for neighbor in G.neighbors(patient["id"])
        )
        if has_nurse:
            continue  # Skip if already has a nurse

        available_nurses = [
            (nurse_id, nurse_data)
            for nurse_id, nurse_data in all_nurses.items()
            if len(nurse_data["current_patients"]) < 3
        ]
        # Sort nurses by least number of patients to balance load
        available_nurses.sort(key=lambda x: len(x[1]["current_patients"]))
        assigned = False
        for nurse_id, nurse_data in available_nurses:
            if len(nurse_data["current_patients"]) < 3:
                if nurse_id not in G.nodes:
                    G.add_node(nurse_id, **nurse_data)
                G.add_edge(nurse_id, patient["id"], relationship="assisting", weight=1)
                nurse_data["current_patients"].append(patient["id"])
                print(f"{nurse_data['name']} is assisting {patient['name']}.")
                assigned = True
                break
        if not assigned:
            print(f"No available nurses for patient {patient['name']}.")


# ---------------------------
# Assign Waiting Patients to Beds
# ---------------------------


def assign_waiting_patients_to_beds():
    """
    Assigns patients from the waiting room to available beds based on priority.
    """
    global total_beds, patients_in_waiting_room

    if total_beds <= 0:
        print("No available beds to assign waiting patients.")
        return

    # Get patients in waiting room with their priority scores
    waiting_patients = get_patients_in_waiting_room()
    if not waiting_patients:
        print("No patients in waiting room to assign.")
        return

    # Sort patients by priority score descending
    waiting_patients_sorted = sorted(
        waiting_patients, key=lambda p: calculate_priority_score(p), reverse=True
    )

    for patient in waiting_patients_sorted:
        if total_beds <= 0:
            break  # No more beds available

        # Assign patient to bed
        assigned_bed = assign_patient_to_bed(patient)
        if assigned_bed:
            # Assign equipment if required
            if patient["required_equipment"]:
                assign_equipment_to_patient(patient, assigned_bed)
            # Remove patient from waiting room
            G.remove_edge("WaitingRoom", patient["id"])
            patients_in_waiting_room -= 1
            print(
                f"Moved patient {patient['name']} from waiting room to {G.nodes[assigned_bed]['name']}. Available beds: {total_beds}"
            )
        else:
            # If unable to assign (shouldn't happen), continue
            continue


# ---------------------------
# Patient Release Functions
# ---------------------------


def simulate_patient_release():
    """
    Simulates the release of patients based on probability.
    Updates patient and equipment statuses accordingly.
    """
    patients_in_beds = get_patients_in_beds()
    released_patients = []
    for patient in patients_in_beds:
        release_probability = calculate_release_probability(patient)
        if random.random() < release_probability:
            print(f"{patient['name']} has been treated and is ready for release.")
            release_patient(patient)
            released_patients.append(patient)
    return released_patients


def calculate_release_probability(patient):
    """
    Calculates the probability of a patient being released.
    Severity 1 has a 75% chance to be released, and higher severities decrease the probability.
    """
    # Base probability model: Severity 1 => 0.75, Severity 10 => lower probability
    severity = patient["severity"]

    # A simple linear formula to scale severity: higher severity means lower probability
    base_prob = max(
        0.75 - (severity - 1) * 0.075, 0.1
    )  # Severity 1 has 75%, Severity 10 has 10%

    # Modifier for surgery cases (less likely to be released if surgery is required)
    surgery_modifier = -0.2 if patient["needs_surgery"] else 0

    # Total probability after modifiers
    total_probability = base_prob + surgery_modifier
    total_probability = max(
        min(total_probability, 1.0), 0.0
    )  # Ensure it's between 0 and 1

    # Debugging output for probability
    print(
        f"Release Probability for {patient['name']} (Severity: {patient['severity']}, Surgery: {patient['needs_surgery']}): {total_probability:.2f}"
    )

    return total_probability


def release_patient(patient):
    global total_beds, patients_in_waiting_room, total_patients

    # Remove patient from bed
    bed_id = None
    for neighbor in G.neighbors(patient["id"]):
        if G.nodes[neighbor]["type"] == "Bed":
            bed_id = neighbor
            break
    if bed_id:
        G.remove_edge(patient["id"], bed_id)
        total_beds += 1
        print(
            f"{patient['name']} has been released from {G.nodes[bed_id]['name']}. Available beds: {total_beds}"
        )

    # Free up equipment
    equipment_assigned = [
        neighbor
        for neighbor in G.neighbors(patient["id"])
        if G.nodes[neighbor]["type"] == "Equipment"
    ]
    for eq in equipment_assigned:
        all_equipment[eq]["available"] = True
        G.remove_edge(eq, patient["id"])
        # Remove equipment node if not connected to any other patients
        if len(list(G.neighbors(eq))) == 0:
            G.remove_node(eq)
        print(f"Equipment {all_equipment[eq]['name']} is now available.")

    # Remove relationships with doctors and nurses
    staff_related = [
        neighbor
        for neighbor in G.neighbors(patient["id"])
        if G.nodes[neighbor]["type"] in ["Doctor", "Nurse"]
    ]
    for staff in staff_related:
        relationship = G.edges[staff, patient["id"]]["relationship"]
        if relationship == "attending":
            # For doctors
            all_doctors[staff]["current_patients"].remove(patient["id"])
            attention = G.edges[staff, patient["id"]]["attention"]
            all_doctors[staff]["attention_allocated"] -= attention
            G.remove_edge(staff, patient["id"])
            if len(all_doctors[staff]["current_patients"]) == 0:
                all_doctors[staff]["attention_allocated"] = 0.0
                print(
                    f"Doctor {all_doctors[staff]['name']} is now idle and removed from the graph."
                )
                G.remove_node(staff)
        elif relationship == "assisting":
            # For nurses
            all_nurses[staff]["current_patients"].remove(patient["id"])
            G.remove_edge(staff, patient["id"])
            if len(all_nurses[staff]["current_patients"]) == 0:
                print(
                    f"Nurse {all_nurses[staff]['name']} is now idle and removed from the graph."
                )
                G.remove_node(staff)

    # Remove patient node
    G.remove_node(patient["id"])
    total_patients -= 1
    print(f"Patient {patient['name']} has been fully released from the hospital.")


# ---------------------------
# Admission Function
# ---------------------------


def admit_n_patients(n):
    """
    Admits 'n' new patients to the hospital.
    Randomly determines severity and equipment requirements.
    """
    for _ in range(n):
        name = names.get_full_name()
        severity = random.randint(1, 10)
        needs_surgery = True if severity == 10 else False
        # Randomly assign equipment requirement
        equipment_options = [
            "Ventilator",
            "Defibrillator",
            "ECG Monitor",
            "Ultrasound Machine",
            "Wheelchair",
            None,
        ]
        required_equipment = random.choice(equipment_options)
        add_patient_to_graph(
            name=name,
            severity=severity,
            needs_surgery=needs_surgery,
            required_equipment_name=required_equipment,
        )


# ---------------------------
# Simulation Loop
# ---------------------------


def simulate_time_step(time_step=1):
    print(f"\n--- Simulating time step: Hour {time_step} ---")

    # Increase time_waiting for patients in waiting room
    waiting_patients = get_patients_in_waiting_room()
    for patient in waiting_patients:
        patient["time_waiting"] += time_step
        print(
            f"Patient {patient['name']} has been waiting for {patient['time_waiting']} hour(s)."
        )

    # Simulate patient releases
    released_patients = simulate_patient_release()

    # Assign waiting patients to available beds
    assign_waiting_patients_to_beds()

    # Get all patients currently in beds to assign medical staff
    current_patients = get_patients_in_beds()

    # Assign medical staff
    assign_medical_staff_to_patients(current_patients)


def get_available_doctor_count():
    available = sum(
        1 for doctor in all_doctors.values() if doctor["attention_allocated"] < 1.0
    )
    return available


def get_available_nurse_count():
    available = sum(
        1 for nurse in all_nurses.values() if len(nurse["current_patients"]) < 3
    )
    return available


def get_available_equipment_count():
    available = sum(1 for equipment in all_equipment.values() if equipment["available"])
    return available


def get_patients_being_treated_count():
    patients_in_beds = [
        node1 if G.nodes[node1]["type"] == "Patient" else node2
        for node1, node2 in G.edges()
        if (
            (G.nodes[node1]["type"] == "Patient" and G.nodes[node2]["type"] == "Bed")
            or (G.nodes[node1]["type"] == "Bed" and G.nodes[node2]["type"] == "Patient")
        )
    ]
    return len(patients_in_beds)


def get_patients_in_waiting_room_count():
    waiting_patients = get_patients_in_waiting_room()
    return len(waiting_patients)


# ---------------------------
# Main Simulation Execution
# ---------------------------


def main_simulation():
    global total_doctors, total_nurses, total_beds, total_rooms, total_equipment

    print("Welcome to the Hospital Simulation!")

    # Generate entities based on user input
    num_doctors = 15
    num_nurses = 30
    num_beds = 30
    num_rooms = 10
    num_equipment = 30
    simulation_hours = 100

    generate_doctors(num_doctors)
    generate_nurses(num_nurses)
    generate_beds(num_beds)
    generate_rooms(num_rooms)
    generate_equipment(num_equipment)

    # Assign beds to rooms
    assign_beds_to_rooms()

    # Simulate over specified time steps
    for hour in range(1, simulation_hours + 1):
        print(f"\n=== Hour {hour} ===")
        simulate_time_step(time_step=hour)
        # Admit new patients
        admit_n_patients(random.randint(5, 13))

        # Convert the graph to node-link data format
        graph_data = json_graph.node_link_data(G)

        # Convert the dictionary to a JSON object
        graph_json = json.dumps(graph_data, indent=4)

        # Save the JSON to a file
        import os

        os.makedirs("./api/json/", exist_ok=True)  # Ensure the output directory exists
        with open("./api/json/graph.json", "w") as f:
            f.write(graph_json)
        print("Simulation complete. Graph data saved to ./api/json/graph.json")

        API_URL = "http://your.api.endpoint/counts"

        counts = Counts(
            total_doctors=total_doctors,
            available_doctors=get_available_doctor_count(),
            total_nurses=total_nurses,
            available_nurses=get_available_nurse_count(),
            total_equipment=total_equipment,
            available_equipment=get_available_equipment_count(),
            patients_being_treated=get_patients_being_treated_count(),
            patients_in_waiting_room=get_patients_in_waiting_room_count(),
            beds_available=total_beds - get_patients_being_treated_count(),
        )

        try:
            response = requests.post(API_URL, json=counts.model_dump_json())
            response.raise_for_status()  # Raises HTTPError for bad responses
            logging.info(f"Successfully sent counts: {counts}")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")  # HTTP error
        except Exception as err:
            logging.error(f"An error occurred: {err}")  # Other errors

        time.sleep(5)
    # ==================================================================
    # END OF SIMULATION
    # ==================================================================


# ---------------------------
# Run the Simulation
# ---------------------------

if __name__ == "__main__":
    main_simulation()
