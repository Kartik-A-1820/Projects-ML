from visionagent.tools import ToolRegistry,detect_objects,read_text,spatial_relation
from visionagent.agent import VisionAgent
from visionagent.planner import choose_tools
SCENE={"objects":[{"name":"red_circle","x":20,"y":30},{"name":"blue_square","x":80,"y":30}],"text":["ALERT 42"]}
def agent():
    r=ToolRegistry();r.register("objects",detect_objects);r.register("ocr",read_text);r.register("spatial",spatial_relation);return VisionAgent(r,max_steps=3)
def test_ocr_routing(): assert choose_tools("read alert number")[0]=="ocr"
def test_spatial_answer():
    r=agent().run(SCENE,"what is left of the blue square")
    assert r["status"]=="grounded" and "left of" in r["answer"]
def test_step_budget():
    r=agent().run(SCENE,"read text and tell object relation")
    assert len(r["trace"])<=3
def test_memory_trace():
    r=agent().run(SCENE,"what objects do you see")
    assert r["memory"] and r["trace"]
