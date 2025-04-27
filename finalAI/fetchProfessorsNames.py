import os
import time
from google import genai  # your Gemini client here

GEMINI_API_KEY = "KEY"  # Load API key from environment


class FetchBairAgent:
    def __init__(self, fetch_interval_seconds=3600):
        api_key = GEMINI_API_KEY
        self.client = genai.Client(api_key=api_key)
        self.fetch_interval = fetch_interval_seconds
        self.running = False
        print("[Agent Initialized] Ready to fetch professors.")

    def fetch_professors(self, position_title=None, lab_name=None, past_experiences=None):
        
        try:
            print("[Fetching] Contacting Gemini API...")
            
            # Default prompt if none is provided
            prompt = f'''You are tasked with researching the {lab_name} at UC Berkeley.

Please return only the full names of all current PhD students affiliated with Autolab.
Format the list as simple plain text — one name per line.
Do not include descriptions, titles, or formatting.
Only the names.'''
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
    print(agent.run_once(lab_name="RISE Lab"))     # Fetch once with a custom prompt
    # agent.run_forever(prompt=custom_prompt) # Or fetch forever with a custom prompt
