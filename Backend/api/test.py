import json
with open("./json/graph.json", 'r') as f:
        graph = json.load(f)
print(graph)