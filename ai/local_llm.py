from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LocalLLM:

    def __init__(self):
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )

    def analyze_scene(self, dialogue_units):

        combined_text = ""
        for i, unit in enumerate(dialogue_units[:10]):  # LIMIT for speed
            combined_text += f"{i+1}. {unit['speaker']}: {unit['dialogue']}\n"

        prompt = f"""
You are an expert film director AI.

Analyze each dialogue and return JSON list with:
emotion, intent, shot_type, camera_angle, camera_movement, duration

Dialogues:
{combined_text}

Return ONLY JSON list.
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        try:
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            return eval(response[json_start:json_end])
        except:
            return []