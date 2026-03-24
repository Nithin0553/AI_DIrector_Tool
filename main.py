# main.py (UPDATED PIPELINE)

from ingest.script_loader import ScriptLoader
from normalize.script_parser import ScriptParser
from normalize.script_normalizer import ScriptNormalizer
from director.beat_planner import BeatPlanner
from editor.editor_engine import EditorEngine
from beatscript.beat_writer import BeatWriter

loader = ScriptLoader()
parser = ScriptParser()
normalizer = ScriptNormalizer()
planner = BeatPlanner()
editor = EditorEngine()
writer = BeatWriter()

# 📥 Load script
text = loader.load_script("data/raw_scripts/Interstellar.pdf")

# 🔍 Parse + normalize
parsed = parser.parse(text)
scene = normalizer.normalize(parsed)

# 🧠 LLM-based beat planning (core intelligence)
beats = planner.plan_beats(scene)

# ✂️ Final editing
beats = editor.edit_beats(beats)

# 💾 Save output
writer.write_beats(beats, "outputs/interstellar_beats.json")

print("✅ Beat script generated successfully!")