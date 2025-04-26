import os
import time
from google import genai  # your Gemini client here

GEMINI_API_KEY = "AIzaSyA3aikIB-WfqxjEWxC1bMUcOiqirRTkX24"  # Load API key from environment


class FetchBairAgent:
    def __init__(self, fetch_interval_seconds=3600):
        api_key = GEMINI_API_KEY
        self.client = genai.Client(api_key=api_key)
        self.fetch_interval = fetch_interval_seconds
        self.running = False
        print("[Agent Initialized] Ready to fetch BAIR professors.")

    def fetch_professors(self, position_title=None, lab_name=None, past_experiences=None):
        
        try:
            print("[Fetching] Contacting Gemini API...")
            
            # Default prompt if none is provided
            prompt = f'''You are a professional scientific writer specializing in crafting cover letters for research positions.
Your task is to generate a customized, highly personalized cover letter using the following inputs:
Inputs:
Intended Research Position Title: {position_title}
Target Research Lab Name: {lab_name}
Candidate's Past Research Experiences: {past_experiences} (include publications, methods used, major findings, skills developed)
Instructions:
Research the lab ({lab_name}) online. Find their current research focus, recent publications, methodologies, key themes, and overall mission.
Begin the cover letter with a strong, personalized opening expressing specific excitement for the lab’s work, mentioning one or two recent projects or themes.
In the body, highlight how the candidate’s past experiences align with the lab’s current research focus.
Focus on technical skills, methods, or problem-solving approaches that would add immediate value to the lab.
Include 1-2 sentences proposing how the candidate could contribute to the lab’s ongoing or future projects, based on recent lab developments.
Use a professional yet enthusiastic tone that conveys genuine interest and preparedness.
Keep the cover letter concise (roughly 300–400 words) unless otherwise requested.
Format:
Professional business letter format
3–4 paragraphs
Include formal salutation and closing
Constraints:

Avoid generic statements (e.g., "I am passionate about research") unless immediately linked to the lab’s specific mission.
Avoid repeating the resume — instead, synthesize experiences into a story tailored to the lab’s needs.
Make sure at least one recent project or publication from the lab is explicitly mentioned by name.
End with a polite, confident closing expressing eagerness to discuss further.'''
            response = self.client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt,
            )
            x = self.save_professors(response.text)
            print("[Success] Fetched and saved professors.")
            return x
        except Exception as e:
            print(f"[Error] Failed to fetch: {e}")

    def save_professors(self, data):
        filename = "bair_professors.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"[Saved] {data} written to {filename}")
        return data

    def run_once(self, position_title=None, lab_name=None, past_experiences=None):
        return self.fetch_professors(position_title, lab_name, past_experiences)

    def run_forever(self, prompt=None):
        self.running = True
        while self.running:
            self.fetch_professors(custom_prompt=prompt)
            print(f"[Sleeping] Waiting {self.fetch_interval} seconds before next fetch...")
            time.sleep(self.fetch_interval)

    def stop(self):
        self.running = False
        print("[Agent Stopped]")

if __name__ == "__main__":
    

    # Position title, research lab, experiences
    agent = FetchBairAgent()
    # Choose one:
    print(agent.run_once(position_title="Student Researcher", lab_name="BAIR", past_experiences="None"))     # Fetch once with a custom prompt
    # agent.run_forever(prompt=custom_prompt) # Or fetch forever with a custom prompt
