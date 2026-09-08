import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from visionagent.tools import ToolRegistry,detect_objects,read_text,spatial_relation
from visionagent.agent import VisionAgent
scenes=json.loads(Path("data/scenes.json").read_text())
reg=ToolRegistry();reg.register("objects",detect_objects);reg.register("ocr",read_text);reg.register("spatial",spatial_relation)
a=VisionAgent(reg)
for q in ["read the alert number","what is left of the blue square","what objects do you see"]:
    print(q,"=>",a.run(scenes[0],q))
