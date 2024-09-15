import networkx as nx
import matplotlib.pyplot as plt

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
    },
    {
        "id": "P2",
        "type": "Patient",
        "priority": "Regular",
        "severity": 2,
        "name": "Jane Smith",
    },
    {
        "id": "P3",
        "type": "Patient",
        "priority": "Surgery",
        "severity": 4,
        "name": "Alice Johnson",
    },
    {
        "id": "P4",
        "type": "Patient",
        "priority": "Emergency",
        "severity": 4,
        "name": "Bob Brown",
    },
]

# Define Doctors
doctors = [
    {
        "id": "D1",
        "type": "Doctor",
        "specialty": "Cardiology",
        "time_available": 3,
        "name": "Dr. Heart",
    },
    {
        "id": "D2",
        "type": "Doctor",
        "specialty": "Orthopedics",
        "time_available": 5,
        "name": "Dr. Bone",
    },
    {
        "id": "D3",
        "type": "Doctor",
        "specialty": "General Surgery",
        "time_available": 2,
        "name": "Dr. Surgeon",
    },
    {
        "id": "D4",
        "type": "Doctor",
        "specialty": "Emergency Medicine",
        "time_available": 1,
        "name": "Dr. Swift",
    },
    {
        "id": "D5",
        "type": "Doctor",
        "specialty": "Neurology",
        "time_available": 4,
        "name": "Dr. Brain",
    },
]

# Define Nurses
nurses = [
    {"id": "N1", "type": "Nurse", "time_available": 4, "name": "Nurse Joy"},
    {"id": "N2", "type": "Nurse", "time_available": 3, "name": "Nurse Anna"},
    {"id": "N3", "type": "Nurse", "time_available": 2, "name": "Nurse Sam"},
    {"id": "N4", "type": "Nurse", "time_available": 5, "name": "Nurse Kim"},
    {"id": "N5", "type": "Nurse", "time_available": 1, "name": "Nurse Lee"},
    {"id": "N6", "type": "Nurse", "time_available": 2, "name": "Nurse Pat"},
]

# Define Equipment (Multiple instances of the same equipment type)
equipment_list = [
    {"id": "E1", "type": "Equipment", "scarcity": 1, "name": "Defibrillator"},
    {"id": "E2", "type": "Equipment", "scarcity": 3, "name": "X-Ray Machine"},
    {"id": "E3", "type": "Equipment", "scarcity": 2, "name": "MRI Scanner"},
    {"id": "E4", "type": "Equipment", "scarcity": 4, "name": "Ventilator"},
]

# Let's create multiple instances of equipment types
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
    "R1": 1,
    "R2": 1,
    "R3": 2,
    "R4": 2,
    "R5": 1,
    "R6": 1,
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

# Create Waiting Room node
waiting_room = {"id": "WR", "type": "WaitingRoom", "name": "Waiting Room"}
G.add_node(waiting_room["id"], **waiting_room)

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
# 4. Define Weight Calculation
# ---------------------------


def calculate_weight(patient, resource, factor=1):
    """
    Calculate the weight based on time, priority, severity, and resource scarcity.
    Lower weights indicate better suitability.
    """
    # Time weight (more available time -> lower weight)
    time_weight = resource.get("time_available", 1)

    # Priority weight (Emergency: 1, Surgery: 2, Regular: 3)
    priority_mapping = {"Emergency": 1, "Surgery": 2, "Regular": 3}
    priority_weight = priority_mapping.get(patient["priority"], 3)

    # Severity weight (higher severity -> lower weight)
    severity_weight = 6 - patient["severity"]  # Assuming severity scale is from 1 to 5

    # Scarcity weight (scarce resources -> higher weight)
    scarcity_weight = resource.get("scarcity", 1)

    # Total weight calculation
    total_weight = (
        time_weight + priority_weight + scarcity_weight + severity_weight
    ) * factor
    return total_weight


# ---------------------------
# 5. Visualize the Knowledge Graph
# ---------------------------

# Define node colors based on type
color_map = {
    "Patient": "lightblue",
    "Doctor": "orange",
    "Nurse": "green",
    "Equipment": "red",
    "Room": "purple",
    "Bed": "brown",
    "AvailableResources": "gray",
    "WaitingRoom": "pink",
}


# Function to assign positions based on clusters (rooms and their resources)
def assign_cluster_positions(G, room_ids, available_resources_node_id, waiting_room_id):
    pos = {}
    layer_spacing = 10
    vertical_spacing = 5
    # Positions for rooms and their connected nodes
    for i, room_id in enumerate(room_ids):
        # Position rooms on the right side, spaced out vertically
        pos[room_id] = (layer_spacing * (i + 1), 0)
        # Position resources relative to the room
        connected_nodes = list(G.neighbors(room_id))
        resource_offset = 1
        for node in connected_nodes:
            node_type = G.nodes[node]["type"]
            if node_type in ["Doctor", "Nurse", "Equipment", "Bed"]:
                pos[node] = (
                    pos[room_id][0] + 1,
                    pos[room_id][1] + resource_offset,
                )
                resource_offset += vertical_spacing
            elif node_type == "Patient":
                # Find the bed the patient is assigned to
                bed_id = [n for n in G.neighbors(node) if G.nodes[n]["type"] == "Bed"]
                if bed_id:
                    bed_pos = pos[bed_id[0]]
                    pos[node] = (bed_pos[0] - 1, bed_pos[1])
                else:
                    # If the patient isn't in a bed, place them near the room
                    pos[node] = (
                        pos[room_id][0]
                        - 2,  # Slightly more space for unassigned patients
                        pos[room_id][1] + resource_offset,
                    )
                    resource_offset += vertical_spacing
    # Position the Available Resources node
    pos[available_resources_node_id] = (0, -10)
    # Position the available resources connected to it
    connected_resources = list(G.neighbors(available_resources_node_id))
    resource_offset = 1
    for node in connected_resources:
        pos[node] = (
            pos[available_resources_node_id][0] + 1,
            pos[available_resources_node_id][1] + resource_offset,
        )
        resource_offset += vertical_spacing
    # Position the Waiting Room node
    pos[waiting_room_id] = (0, 10)
    # Position the patients in the waiting room
    waiting_patients = list(G.neighbors(waiting_room_id))
    patient_offset = 1
    for node in waiting_patients:
        pos[node] = (
            pos[waiting_room_id][0] - 1,
            pos[waiting_room_id][1] + patient_offset,
        )
        patient_offset += vertical_spacing
    return pos


# Get all room IDs
room_ids = [room["id"] for room in rooms]

# Assign positions based on clusters
pos = assign_cluster_positions(
    G, room_ids, available_resources_node["id"], waiting_room["id"]
)

# Debugging step: Print all node positions and check if P1 is missing
print("\nAssigned positions for nodes:")
for node in G.nodes:
    if node in pos:
        print(f"{node} => {pos[node]}")
    else:
        print(f"Warning: {node} has no assigned position!")  # Debugging missing nodes

# Fallback: Ensure all nodes have positions (including patients)
for node in G.nodes:
    if node not in pos:
        print(f"Assigning default position to node: {node}")
        pos[node] = (0, 0)  # Default fallback position

# Generate node colors based on current graph
node_colors = [color_map.get(data["type"], "gray") for _, data in G.nodes(data=True)]
labels = {node: data.get("name", node) for node, data in G.nodes(data=True)}

# Draw the graph
plt.figure(figsize=(20, 15))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.9)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels, font_size=10)

# Create legend
for node_type, color in color_map.items():
    plt.scatter([], [], c=color, label=node_type)
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc="upper left")

plt.title("Hospital Resource Allocation Knowledge Graph")
plt.axis("off")
plt.show()

# ---------------------------
# 6. Simulate Routing a New Patient
# ---------------------------

# Add a new incoming patient
new_patient = {
    "id": "P5",
    "type": "Patient",
    "priority": "Emergency",
    "severity": 5,
    "name": "David King",
}
G.add_node(new_patient["id"], **new_patient)

# Assign the new patient to a bed
assigned_bed = assign_patient_to_bed(new_patient, G, beds)

# ---------------------------
# 7. Assign Resources from the Room to the Patient
# ---------------------------


def assign_resources_to_patient(patient, bed_id, G):
    """
    Assigns a doctor, nurse, and equipment from the bed's room to the patient.
    Updates resource availability accordingly.
    """
    # Get the room ID from the bed
    bed = G.nodes[bed_id]
    room_id = bed["room_id"]

    # Get resources in the room
    resources = {
        "doctors": [n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Doctor"],
        "nurses": [n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Nurse"],
        "equipment": [
            n for n in G.neighbors(room_id) if G.nodes[n]["type"] == "Equipment"
        ],
    }

    # Assign Doctor
    assigned_doctor = None
    for doc_id in resources["doctors"]:
        # Check if doctor is available (time_available > 0)
        if G.nodes[doc_id]["time_available"] > 0:
            assigned_doctor = doc_id
            break
    if assigned_doctor:
        G.add_edge(
            patient["id"],
            assigned_doctor,
            relationship="attended_by",
            weight=calculate_weight(patient, G.nodes[assigned_doctor]),
        )
        # Update doctor's availability
        G.nodes[assigned_doctor]["time_available"] -= 1
        print(
            f"Assigned Doctor {G.nodes[assigned_doctor]['name']} to {patient['name']}"
        )
    else:
        print(
            f"No available doctors in {G.nodes[room_id]['name']} for {patient['name']}"
        )

    # Assign Nurse
    assigned_nurse = None
    for nurse_id in resources["nurses"]:
        if G.nodes[nurse_id]["time_available"] > 0:
            assigned_nurse = nurse_id
            break
    if assigned_nurse:
        G.add_edge(
            patient["id"],
            assigned_nurse,
            relationship="assisted_by",
            weight=calculate_weight(patient, G.nodes[assigned_nurse]),
        )
        # Update nurse's availability
        G.nodes[assigned_nurse]["time_available"] -= 1
        print(f"Assigned Nurse {G.nodes[assigned_nurse]['name']} to {patient['name']}")
    else:
        print(
            f"No available nurses in {G.nodes[room_id]['name']} for {patient['name']}"
        )

    # Assign Equipment
    assigned_equipment = None
    for eq_id in resources["equipment"]:
        assigned_equipment = eq_id
        break  # For simplicity, assign the first equipment
    if assigned_equipment:
        G.add_edge(
            patient["id"],
            assigned_equipment,
            relationship="needs",
            weight=calculate_weight(patient, G.nodes[assigned_equipment]),
        )
        print(
            f"Assigned Equipment {G.nodes[assigned_equipment]['name']} to {patient['name']}"
        )
    else:
        print(
            f"No available equipment in {G.nodes[room_id]['name']} for {patient['name']}"
        )


# Assign resources to the new patient if assigned to a bed
if assigned_bed:
    assign_resources_to_patient(new_patient, assigned_bed, G)

# ---------------------------
# 8. Reassign Positions After Adding New Patient
# ---------------------------

# Reassign positions to include the new patient
pos = assign_cluster_positions(
    G, room_ids, available_resources_node["id"], waiting_room["id"]
)

# Remove nodes from 'pos' that no longer exist in the graph
pos = {node: pos[node] for node in pos if node in G}

# Ensure only nodes with valid positions are drawn
valid_nodes = [node for node in G.nodes if node in pos]

# Filter node colors to only include colors for valid nodes
node_colors = [color_map.get(G.nodes[node]["type"], "gray") for node in valid_nodes]

# Update labels to match only valid nodes
labels = {node: G.nodes[node].get("name", node) for node in valid_nodes}

# ---------------------------
# 9. Filter edges to include only valid ones
# ---------------------------

# Filter edges: only include edges where both endpoints have valid positions
valid_edges = [(u, v) for u, v in G.edges() if u in pos and v in pos]

# ---------------------------
# 10. Visualize the Updated Knowledge Graph
# ---------------------------

plt.figure(figsize=(20, 15))

# Draw only valid nodes that exist in both the graph and positions
nx.draw_networkx_nodes(
    G, pos, node_color=node_colors, node_size=800, alpha=0.9, nodelist=valid_nodes
)

# Draw only valid edges
nx.draw_networkx_edges(G, pos, edgelist=valid_edges, width=1.0, alpha=0.5)

# Draw the labels for valid nodes
nx.draw_networkx_labels(G, pos, labels, font_size=10)

# Create legend
for node_type, color in color_map.items():
    plt.scatter([], [], c=color, label=node_type)
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc="upper left")

plt.title("Hospital Resource Allocation Knowledge Graph")
plt.axis("off")
plt.show()

# ---------------------------
# 10. Detect and Visualize Resource Strain
# ---------------------------


def detect_resource_strain(G):
    strained_resources = []

    for node_id, data in G.nodes(data=True):
        if data["type"] in ["Doctor", "Nurse"]:
            time_available = data.get("time_available", 0)
            if time_available <= 0:
                strained_resources.append((node_id, data["name"], data["type"]))

    return strained_resources


# Detect resource strain
strained_resources = detect_resource_strain(G)
print("\nResources experiencing strain:")
for node_id, name, res_type in strained_resources:
    print(f"  {name} ({res_type})")

# Visualizing resource strain
strained_nodes = [node_id for node_id, _, _ in strained_resources if node_id in pos]

# Filter node colors to include only nodes with valid positions
node_colors_strain = [
    "red" if node in strained_nodes else color_map.get(G.nodes[node]["type"], "gray")
    for node in pos  # Only include nodes that have valid positions
]
# Ensure that 'labels' only includes nodes with valid positions
filtered_labels = {node: G.nodes[node].get("name", node) for node in pos}

# ---------------------------
# Drawing the Graph
# ---------------------------

plt.figure(figsize=(20, 15))

# Draw only valid nodes that exist in both the graph and the positions dictionary
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors_strain,
    node_size=800,
    alpha=0.9,
    nodelist=list(pos.keys()),
)

# Filter edges: only include edges where both endpoints have valid positions
valid_edges = [(u, v) for u, v in G.edges() if u in pos and v in pos]

# Draw only valid edges
nx.draw_networkx_edges(G, pos, edgelist=valid_edges, width=1.0, alpha=0.5)

# Draw the labels for valid nodes
nx.draw_networkx_labels(G, pos, labels=filtered_labels, font_size=10)

# Create legend
for node_type, color in color_map.items():
    plt.scatter([], [], c=color, label=node_type)
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc="upper left")

plt.title("Resource Strain Visualization")
plt.axis("off")
plt.show()
