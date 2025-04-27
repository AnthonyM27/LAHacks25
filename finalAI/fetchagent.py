import os
import time
from google import genai  # your Gemini client here

class FetchBairAgent:
    def __init__(self, api_key, fetch_interval_seconds=3600):
        self.client = genai.Client(api_key=api_key)
        self.fetch_interval = fetch_interval_seconds
        self.running = False
        print("[Agent Initialized] Ready to fetch BAIR professors.")

    def fetch_professors(self):
        try:
            print("[Fetching] Contacting Gemini API...")
            response = self.client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=f'''
You are tasked with researching {1}the BAIR (Berkeley Artificial Intelligence Research) Lab at UC Berkeley.

Please return only the full names of all current professors affiliated with BAIR.
Format the list as simple plain text — one name per line.
Do not include descriptions, titles, or formatting.
Only the names.
'''
            )
            professors_list = response.text.strip()
            self.save_professors(professors_list)
            print("[Success] Fetched and saved professors.")
        except Exception as e:
            print(f"[Error] Failed to fetch: {e}")

    def save_professors(self, data):
        filename = "bair_professors.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"[Saved] Data written to {filename}")

    def run_once(self):
        self.fetch_professors()

    def run_forever(self):
        self.running = True
        while self.running:
            self.fetch_professors()
            print(f"[Sleeping] Waiting {self.fetch_interval} seconds before next fetch...")
            time.sleep(self.fetch_interval)

    def stop(self):
        self.running = False
        print("[Agent Stopped]")

if __name__ == "__main__":
    GEMINI_API_KEY = "AIzaSyA3aikIB-WfqxjEWxC1bMUcOiqirRTkX24"  # Load API key from environment

    agent = FetchBairAgent(api_key=GEMINI_API_KEY, fetch_interval_seconds=86400)  # 1 day default

    # Choose one:
    agent.run_once()      # Fetch once and exit
    # agent.run_forever() # Uncomment this to fetch periodically
