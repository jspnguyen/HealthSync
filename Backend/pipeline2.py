from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv

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
    # CODE HERE
    
    # TODO: Prompts need reengineering
    messages = [
        {"role": "system", "content": "You are a professional hospital staff allocation manager working in a moment of high stress for a hospital. Given staffing levels, reply with what item needs to be increased if all levels are adequate say so. Nurse to patient ration should be at least 1:2, doctor to patient should be at least 1:1000, and beds should be at least 1:1. Reply in a short phrase."},
        {"role": "user", "content": f""},
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
    
    # TODO:
    # Make a call to knowledge base

if __name__ == "__main__":
    stres_level.run()