import os
import time
from google import genai  # your Gemini client here
from bs4 import BeautifulSoup
import json



GEMINI_API_KEY = "AIzaSyCMF3sf2BD9f1AZ1FdHIJgVCj5f03CQUes"  # Load API key from environment


class FetchLabsAgent:
    def __init__(self, fetch_interval_seconds=3600):
        api_key = GEMINI_API_KEY
        self.client = genai.Client(api_key=api_key)
        self.fetch_interval = fetch_interval_seconds
        self.running = False
        print("[Agent Initialized] Ready to fetch professors.")

    def fetch_professors(self, topic=None):
        
        try:
            print("[Fetching] Contacting Gemini API...")

            
            # Default prompt if none is provided
            prompt = f'''Research and summarize the different research centers at UC Berkeley that focus on {topic}. For each center, provide:

name: The center’s name
mission: A brief description of its mission or focus
link: A link to their official webpage if available.
Focus on accuracy and thoroughness, but keep each center’s summary concise and organized.
Return this in JSON format.'''
            response = self.client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt,
            )
            json_data = self.save_professors(response.text)
            print(json_data[4:])
            labs = json.loads(json_data[7:-3])
            print("[Success] Fetched and saved professors.")
            return labs
        except Exception as e:
            print(f"[Error] Failed to fetch: {e}")

    def save_professors(self, data):
        filename = "bair_professors.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"[Saved] {data} written to {filename}")
        return data

    def run_once(self, topic=None):
        return self.fetch_professors(topic)

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
    agent = FetchLabsAgent()
    # Choose one:
    print(agent.run_once(topic="Electronics"))     # Fetch once with a custom prompt
    # agent.run_forever(prompt=custom_prompt) # Or fetch forever with a custom prompt

    
