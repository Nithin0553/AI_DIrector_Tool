from ai.local_llm import LocalLLM


class BeatPlanner:

    def __init__(self):
        self.llm = LocalLLM()

    def plan_beats(self, scene):

        beats = []
        beat_id = 1
        current_time = 0.0

        for unit in scene["dialogue_units"]:

            speaker = unit["speaker"]
            dialogue = unit["dialogue"]

            # 🔥 Call LLM for cinematic analysis
            result = self.llm.analyze_dialogue(dialogue, speaker)

            # ✅ Safe fallback (in case LLM fails)
            emotion = result.get("emotion", "neutral")
            intent = result.get("intent", "statement")
            shot_type = result.get("shot_type", "medium")
            camera_angle = result.get("camera_angle", "eye_level")
            camera_movement = result.get("camera_movement", "static")

            try:
                duration = float(result.get("duration", 2.5))
            except:
                duration = 2.5

            # 🎬 Build beat
            beat = {
                "scene_id": scene.get("scene_id", 1),
                "beat_id": beat_id,
                "speaker": speaker,
                "dialogue": dialogue,

                # 🧠 AI outputs
                "emotion": emotion,
                "intent": intent,

                # 🎥 Cinematography
                "shot_type": shot_type,
                "camera_angle": camera_angle,
                "camera_movement": camera_movement,

                # ⏱ Timing
                "start_time": round(current_time, 2),
                "duration": round(duration, 2)
            }

            beats.append(beat)

            # ⏳ Update timeline
            current_time += duration
            beat_id += 1

        return beats