from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LocalLLM:

    def __init__(self):
        model_name = "mistralai/Mistral-7B-Instruct-v0.2"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def analyze_dialogue(self, dialogue, speaker):

        prompt = f"""
You are an expert film director AI.

Analyze the dialogue and return ONLY JSON:

{{
  "emotion": "...",
  "intensity": 0.0-1.0,
  "intent": "...",
  "shot_type": "...",
  "camera_angle": "...",
  "camera_movement": "...",
  "duration": float (seconds)
}}

Dialogue:
Speaker: {speaker}
Text: {dialogue}
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120,
            temperature=0.3
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract JSON part
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            json_str = response[json_start:json_end]
            return eval(json_str)
        except:
            return {
                "emotion": "neutral",
                "intensity": 0.5,
                "intent": "statement",
                "shot_type": "medium",
                "camera_angle": "eye_level",
                "camera_movement": "static",
                "duration": 2.5
            }