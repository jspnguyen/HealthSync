from uagents import Agent, Context
import random, string, os, requests, json
from dotenv import load_dotenv
from faker import Faker
import main

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")
fake = Faker()

def generate_random_string(length=128):
    letters = string.ascii_letters  
    return ''.join(random.choice(letters) for _ in range(length))

stress_level = Agent(name="stress_level", seed=generate_random_string())

prev_disaster = {'description' : ''}

@stress_level.on_interval(period=10.0)
async def stress_level(ctx: Context):
    with open("api/json/disasters.json", 'r') as file:
        data = json.load(file)
    
    if data['description'] != prev_disaster['description']:
        messages = [
            {"role": "system", "content": "Reply to me only the number of people who are injured from the following natural disaster."},
            {"role": "user", "content": f"{data['description']}"},
        ]

        payload = {
            "messages": messages,
            "stream": False,
            "max_new_tokens": 2048,
            "temperature": 0.2
        }

        res = requests.post(
            f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
            headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
            json=payload,
            stream=False
        )

        num_injured = int(res.text.strip('"'))
        ctx.logger.info(num_injured)
        
        for _ in range(len(num_injured)):
            patient_name = f"{fake.first_name()} {fake.last_name()}"
            urgency_score = random.random(8.5, 9.7)
            surgery_status = random.choice([True, False])
            equipment_status = random.choice(["None", "Defibrillator", "ECG Monitor"])
            main.add_patient_to_graph(patient_name, urgency_score, surgery_status, equipment_status)

if __name__ == "__main__":
    stress_level.run()