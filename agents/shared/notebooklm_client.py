from google import genai

class NotebookLMClient:
    def __init__(self, project_id):
        self.client = genai.GenerativeModel("notebooklm-bison")

    def ask(self, query):
        response = self.client.generate_content([query])
        return response.candidates[0].content.parts[0].text
