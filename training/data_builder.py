import re


class DataBuilder:

    def __init__(self):
        pass

    def build_from_srt(self, file_path):
        """
        Reads an SRT file and converts it into structured training data.
        Each row contains:
        - dialogue
        - duration
        - word_count
        - punctuation features
        """

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        blocks = content.strip().split("\n\n")

        dataset = []

        for block in blocks:
            lines = block.strip().split("\n")

            if len(lines) < 3:
                continue

            # Extract timestamp
            time_line = lines[1]
            start, end = self._parse_time(time_line)

            duration = end - start

            # Extract dialogue (can be multi-line)
            dialogue = " ".join(lines[2:]).strip()

            # Clean dialogue
            dialogue = self._clean_text(dialogue)

            # Features
            word_count = len(dialogue.split())
            has_qmark = 1 if "?" in dialogue else 0
            has_exclaim = 1 if "!" in dialogue else 0
            has_ellipsis = 1 if "..." in dialogue else 0

            row = {
                "dialogue": dialogue,
                "duration": round(duration, 3),
                "word_count": word_count,
                "has_qmark": has_qmark,
                "has_exclaim": has_exclaim,
                "has_ellipsis": has_ellipsis
            }

            dataset.append(row)

        return dataset

    # ---------------------------
    # Helper Functions
    # ---------------------------

    def _parse_time(self, time_line):
        """
        Converts SRT time format to seconds
        Example: 00:01:15,123 --> 00:01:17,456
        """

        start_str, end_str = time_line.split(" --> ")

        start = self._time_to_seconds(start_str)
        end = self._time_to_seconds(end_str)

        return start, end

    def _time_to_seconds(self, time_str):
        """
        Converts HH:MM:SS,ms to seconds
        """

        hours, minutes, rest = time_str.split(":")
        seconds, millis = rest.split(",")

        total = (
                int(hours) * 3600 +
                int(minutes) * 60 +
                int(seconds) +
                int(millis) / 1000
        )

        return total

    def _clean_text(self, text):
        """
        Cleans subtitle noise
        """

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()