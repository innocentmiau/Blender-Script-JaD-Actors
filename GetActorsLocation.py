import bpy
from pathlib import Path

path = Path.home() / 'Desktop' / 'blenderActors.txt'

actors = {
    "money": [],
    "buzzer": [],
    "eco-blue": [],
    "eco-yellow": [],
    "eco-red": [],
    "ropebridge": [],
    "crate": [],
    "plat-eco": []
}

heightAdded = {
    "money": 1.5,
    "buzzer": 0,
    "eco-blue": 0,
    "eco-yellow": 0,
    "eco-red": 0,
    "ropebridge": 0,
    "crate": 0,
    "plat-eco": 0
}

contentTypes = {
    "eco_yellow": 1,
    "eco_red": 2,
    "eco_blue": 3,
    "eco_green": 4,
    "orbs": 5,
    "power_cell": 6,
    "green_pill": 7,
    "buzzer": 8
}

crateTypes = {
    "crate-wood": "wood",
    "crate-iron": "iron",
    "crate-steel": "steel",
    "crate-bucket": "bucket",
    "crate-barrel": "barrel",
    "crate-darkeco": "darkeco"
}

def transform_location(location):
    x, z, y = location
    return [x, y, -z]

def transform_quat(quat):
    w, x, z, y = quat
    return [x, y, -z, w]

objectsToUseAsReference = {}
for obj in bpy.context.scene.objects:
    if "-final" not in obj.name:
        continue
    location = transform_location([round(coord, 3) for coord in obj.location])
    objectsToUseAsReference.update({obj.name: location})

def collect_object_locations():
    for collection_name in bpy.data.collections.keys():
        if collection_name in actors:
            collection = bpy.data.collections[collection_name]
            for obj in collection.objects:
                location = transform_location([round(coord, 3) for coord in obj.location])
                quat = transform_quat([round(coord, 3) for coord in obj.rotation_quaternion])
                actors[collection_name].append((location, quat, obj.name))

def generate_text():
    lines = []
    for actor_type, objects in actors.items():
        for count, (location, quat, name) in enumerate(objects, start=1):
            
            etype = "crate" if actor_type == "buzzer" else actor_type
            
            lump_extra = ""
            if actor_type == "buzzer":
                lump_extra = f""",
        "crate-type": "'iron",
        "eco-info": ["int32", 8, 1]"""
            if actor_type == "crate":
                crateType = "wood"
                for crate_key in crateTypes:
                    if crate_key in name:
                        crateType = crateTypes[crate_key]
                        break
                contentType = 1
                contentAmount = 1
                for content_type in contentTypes:
                    if content_type in name:
                        contentType = contentTypes[content_type]
                        start_index = name.index(content_type) + len(content_type)
                        number = name[start_index:]
                        numb = ""
                        for char in number:
                            if char.isdigit():
                                numb += char
                            else:
                                break
                        if numb.isnumeric():
                            contentAmount = int(numb)
                lump_extra = f""",
        "crate-type": "'{crateType}",
        "eco-info": ["int32", {contentType}, {contentAmount}]"""
            if actor_type == "ropebridge":
                art_name = None
                if "ropebridge-52" in name:
                    art_name = "ropebridge-52"
                if "ropebridge-70" in name:
                    art_name = "ropebridge-70"
                if art_name != None:
                    heightAdded[actor_type] = -2
                    lump_extra = f""",
        "art-name": "{art_name}" """

            coords = [location[0], (location[1] + heightAdded[actor_type]), location[2]]
            coords2 = coords.copy()
            coords2.append(10)

            if actor_type == "plat-eco":
                pathCoords = coords.copy()
                pathCoords.append(1.0)
                pathCoordsFinal = coords.copy()
                reference = name + "-final"
                velocity = 10
                for obj in objectsToUseAsReference.keys():
                    if reference in obj:
                        pathCoordsFinal = objectsToUseAsReference[obj]
                        pathCoordsFinal.append(1.0)
                        start_index = obj.index("-final") + len("-final")
                        number = obj[start_index:]
                        numb = ""
                        for char in number:
                            if char.isdigit():
                                numb += char
                            else:
                                break
                        if numb.isnumeric():
                            velocity = int(numb)
                        break
                lump_extra = f""",
        "path":["vector4m",
          {pathCoords},
          {pathCoordsFinal}],
        "sync": ["float", {velocity}.0, 0.0],
        "notice-dist":["meters", 1.0] """
            
            lines.append(f"""    {{
      "trans": {coords},
      "etype": "{etype}",
      "game_task": 0,
      "quat": {quat},
      "bsphere": {coords2},
      "lump": {{
        "name": "{actor_type}-{count}"{lump_extra}
      }}
    }},
""")
    return ''.join(lines)

def write_to_file(text):
    with open(path, "w") as file:
        file.write(text)

collect_object_locations()

text_content = generate_text()

write_to_file(text_content)