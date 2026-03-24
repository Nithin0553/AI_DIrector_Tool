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
You are a professional film director.

For EACH dialogue:
- Detect emotion (happy, sad, anger, fear, neutral)
- Detect intensity (0–1)
- Detect intent (question, command, argument, etc.)

Also decide:
- shot_type:
    closeup → strong emotion
    medium → normal dialogue
    wide → environment/action

- camera_angle:
    low_angle → power
    high_angle → weakness
    eye_level → normal

- camera_movement:
    static → calm
    slow_zoom → emotional
    pan → conversation
    handheld → tension

- duration:
    based on speaking speed + pauses + emotion

VERY IMPORTANT:
Return DIFFERENT values for different dialogues.

Return JSON list.
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