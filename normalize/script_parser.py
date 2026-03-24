import re
import spacy


class ScriptParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, raw_text):
        lines = raw_text.split("\n")
        parsed_units = []
        current_speaker = None
        buffer_dialogue = []

        for raw_line in lines:
            line = self._clean_line(raw_line)
            if not line:
                self._flush_dialogue(parsed_units, current_speaker, buffer_dialogue)
                current_speaker = None
                buffer_dialogue = []
                continue

            if self._is_scene_heading(line) or self._is_transition(line) or self._is_page_number(line):
                self._flush_dialogue(parsed_units, current_speaker, buffer_dialogue)
                current_speaker = None
                buffer_dialogue = []
                continue

            inline_match = re.match(r"^([A-Z][A-Z0-9 .'\-()]+):\s*(.+)$", line)
            if inline_match:
                self._flush_dialogue(parsed_units, current_speaker, buffer_dialogue)
                speaker = self._clean_speaker(inline_match.group(1))
                dialogue = inline_match.group(2).strip()
                if self._is_real_speaker(speaker) and dialogue:
                    parsed_units.append({
                        "speaker": speaker,
                        "dialogue": dialogue
                    })
                current_speaker = None
                buffer_dialogue = []
                continue

            if self._looks_like_speaker(line):
                self._flush_dialogue(parsed_units, current_speaker, buffer_dialogue)
                current_speaker = self._clean_speaker(line)
                buffer_dialogue = []
                continue

            if current_speaker:
                if not self._is_parenthetical(line):
                    buffer_dialogue.append(line)

        self._flush_dialogue(parsed_units, current_speaker, buffer_dialogue)
        return parsed_units

    def _flush_dialogue(self, parsed_units, current_speaker, buffer_dialogue):
        if current_speaker and buffer_dialogue:
            dialogue = " ".join(buffer_dialogue).strip()
            dialogue = re.sub(r"\s+", " ", dialogue)
            if dialogue:
                parsed_units.append({
                    "speaker": current_speaker,
                    "dialogue": dialogue
                })

    def _clean_line(self, line):
        line = re.sub(r"<.*?>", "", line)
        line = re.sub(r"\s+", " ", line)
        return line.strip()

    def _clean_speaker(self, line):
        speaker = re.sub(r"\(.*?\)", "", line).strip()
        speaker = re.sub(r"\s+", " ", speaker)
        return speaker

    def _looks_like_speaker(self, line):
        clean = line.strip()
        if len(clean) > 35:
            return False
        if not re.match(r"^[A-Z][A-Z0-9 .'\-()]+$", clean):
            return False
        return self._is_real_speaker(self._clean_speaker(clean))

    def _is_real_speaker(self, line):
        clean = line.strip()
        if not clean:
            return False
        if clean.startswith(("INT.", "EXT.", "INT/EXT.", "FADE", "CUT TO", "DISSOLVE TO", "INSERT", "ANGLE ON")):
            return False
        if len(clean.split()) > 3:
            return False
        doc = self.nlp(clean.title())
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return True
        words = clean.split()
        if 1 <= len(words) <= 2 and all(word.isupper() for word in words):
            return True
        return False

    def _is_parenthetical(self, line):
        return line.startswith("(") and line.endswith(")")

    def _is_scene_heading(self, line):
        return bool(re.match(r"^(INT\.|EXT\.|INT/EXT\.)", line))

    def _is_transition(self, line):
        return bool(re.match(r".*(CUT TO:|FADE IN:|FADE OUT:|DISSOLVE TO:)$", line))

    def _is_page_number(self, line):
        return bool(re.match(r"^\d+\.?$", line))