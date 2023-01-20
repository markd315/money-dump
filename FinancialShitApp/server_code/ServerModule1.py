import json
import os

import anvil.server

@anvil.server.callable
def get_lesson(unitId, lessonNm):
    folder = "lessons/" + unitId
    if not os.path.exists(folder):
        # If the folder does not exist, create it
        os.makedirs(folder)
    print(folder)
    with open(os.path.join(folder, lessonNm + ".json"), "r") as f:
        ret = f.read()
        f.close()
        return json.loads(ret)

@anvil.server.callable
def get_available_lessons(unitId, lessonNm):
    folder = "lessons/" + unitId
    if not os.path.exists(folder):
        # If the folder does not exist, create it
        os.makedirs(folder)
    with open(os.path.join(folder, lessonNm + ".json"), "r") as f:
        ret = f.read()
        f.close()
        return json.loads(ret)