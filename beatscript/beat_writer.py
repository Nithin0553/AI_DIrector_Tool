import json
import os


class BeatWriter:

    def write_beats(self, beats, output_file):

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(beats, file, indent=4)

        print("Beat script saved to:", output_file)