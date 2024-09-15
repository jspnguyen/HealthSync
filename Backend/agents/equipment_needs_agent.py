from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

def generate_random_string(length=128):
    letters = string.ascii_letters  
    return ''.join(random.choice(letters) for _ in range(length))

equipment_agent = Agent(name="equipment_needs", seed=generate_random_string())

@equipment_agent.on_interval(period=4.0)
async def equipment_needs(ctx: Context):
    messages = [
        {"role": "system", "content": "You are in charge of distributing equipment based on a patient's symptoms. Reply with what equipment(s) is needed from the following list in Python list format: Ventilator, Defibrillator, ECG Monitor, Ultrasound Machine, Wheelchair, None"},
        {"role": "user", "content": f"A heart attack"},
    ]

    payload = {
        "messages": messages,
        "stream": False,
        "max_new_tokens": 2048,
        "temperature": 0.9
    }

    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    equipment = res.text.strip('"')
    ctx.logger.info(f"Equipment Needed: {equipment}")

if __name__ == "__main__":
    equipment_agent.run()