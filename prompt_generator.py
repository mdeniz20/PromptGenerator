from operator import ge
import os
from shlex import join
class Prompt_Generator:
    prompt_template_file = None
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompt_template_file = os.path.join(current_dir, "prompt_template.txt")
        
    def generate_prompt(self, concept, selected_topics, difficulty, note):
        if not self.prompt_template_file:
            return "Prompt template file not found."
        with open(self.prompt_template_file, "r") as f:
            prompt_template = f.read()
        prompt_template = prompt_template.replace("<topic>", ", ".join(selected_topics))
        prompt_template = prompt_template.replace("<difficulty>", difficulty)
        prompt_template = prompt_template.replace("<concept>", concept)
        prompt_template = prompt_template.replace("<additional_notes>", note if note != "" else "No additional notes.")
        return prompt_template
        
        