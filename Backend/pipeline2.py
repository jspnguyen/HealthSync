from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv
import main

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

def generate_random_string(length=128):
    letters = string.ascii_letters  
    return ''.join(random.choice(letters) for _ in range(length))

stres_level = Agent(name="stress_level", seed=generate_random_string())

@stres_level.on_interval(period=10.0)
async def stress_level(ctx: Context):
    # TODO: Get staffing and equipments levels here
    doctors = 0
    nurses = 0
    beds = 0
    patients = 0
    
    messages = [
        {"role": "system", "content": "Given certain supply levels of staff and equipment, reply with a boolean (True or False) if there should be worry in terms of level of availability."},
        {"role": "user", "content": f"Doctors: {doctors} Nurses: {nurses} Beds: {beds} Patients in Hospital: {patients}"},
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

    response = res.text.strip('"')
    ctx.logger.info(response)
    
    # TODO: Add a notification of some sort
    if True:
        pass
    else:
        pass
    
    # TODO:
    # Make a call to knowledge base

if __name__ == "__main__":
    stres_level.run()