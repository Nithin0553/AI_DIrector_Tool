# editor/editor_engine.py
from training.train_model import DurationModel


class EditorEngine:
    def __init__(self):
        self.model = DurationModel()
        self.model.train("training/train.csv")

    def edit_beats(self, beats):
        for beat in beats:
            dialogue = beat["dialogue"]
            features = {
                "word_count": len(dialogue.split()),
                "has_qmark": 1 if "?" in dialogue else 0,
                "has_exclaim": 1 if "!" in dialogue else 0,
                "has_ellipsis": 1 if "..." in dialogue else 0
            }
            duration = self.model.predict(features)
            emotion = beat.get("emotion", "neutral")

            if emotion == "fear":
                duration *= 1.2
            elif emotion == "anger":
                duration *= 0.9

            beat["duration"] = round(duration, 3)
            beat["transition"] = self._get_transition(emotion)
        return beats

    def _get_transition(self, emotion):
        if emotion == "fear":
            return "quick_cut"
        if emotion == "anger":
            return "hard_cut"
        if emotion == "calm":
            return "fade"
        return "cut"