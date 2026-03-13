from model import call_llm
import json

class Executor:
    def __init__(self):
        pass

    def parse_json(self, text):
        if text is None:
            raise RuntimeError("LLM returned None (likely API failure)")
    
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print("JSON parsing failed, trying to clean it")
            cleaned = text.replace("```json", "").replace("```", "").strip()
            try:
                return json.loads(cleaned)
            except Exception as e:
                print("failed to parse")#probably ask the model to regenerate

    def executePrompt(self, system_prompt, user_prompt, temperature = 0.7, isJson = True):
        llm_ans = call_llm(system_prompt, user_prompt, temperature)
        if isJson:
            return self.parse_json(llm_ans)
        else:
            return llm_ans