import json

def load(path):
    data = {}
    entities = []
    name = ""
    with open(path, "r") as file:
        data = json.loads(file.read())
        file.close()

    name = data["PROJECT"]["NAME"]

    for entity in data["ENTITIES"]:
        e = [entity["x"], entity["y"], entity["id"]]
        entities.append(e)

    return entities, name
