from model import call_llm
import json

class Executor:
    def __init__(self):
        pass

    def parse_json(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print("JSON parsing failed")
            cleaned = text.replace("```json", "").replace("```", "").strip()
            try:
                return json.loads(cleaned)
            except Exception as e:
                print("failed to parse")#probably ask the model to regenerate

    def executePrompt(self, prompt):
        llm_ans = call_llm(prompt)
        f_ans = self.parse_json(llm_ans)#maybe add a way check whether the output reuqested before was in json or not
        #add a way to understand json here, maybe add some way to add prompt to give output in a particular way
        return f_ans