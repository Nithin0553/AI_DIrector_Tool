class ScriptNormalizer:

    def normalize(self, parsed_units):
        """
        Convert parsed dialogue units into a scene structure.
        """

        scene = {
            "characters": set(),
            "dialogue_units": []
        }

        for unit in parsed_units:

            speaker = unit["speaker"]
            dialogue = unit["dialogue"]

            scene["characters"].add(speaker)

            scene["dialogue_units"].append({
                "speaker": speaker,
                "dialogue": dialogue,
                "emotion": None,
                "intent": None
            })

        scene["characters"] = list(scene["characters"])

        return scene