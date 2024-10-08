from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

def generate_random_string(length=128):
    letters = string.ascii_letters  # Includes both uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))

doctor_agent = Agent(name="doctor_allocator", seed=generate_random_string())

@doctor_agent.on_interval(period=4.0)
async def doctor_allocator(ctx: Context):
    patients = random.randint(0, 30)
    
    messages = [
        {"role": "system", "content": "You are a professional hospital staff allocation manager. You should only respond with a number and nothing else."},
        {"role": "user", "content": f"Tell me how many doctors should be deployed to a room with {patients} patients"},
    ]

    payload = {
        "messages": messages,
        "stream": False,
        "max_new_tokens": 2048,
        "temperature": 0.9
    }

    # Call model endpoint
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    # Print the generated tokens as they get streamed
    num_doctors = int(res.text.strip('"'))
    ctx.logger.info(f"You should send {num_doctors} nurses to a room with {patients} patients.")

if __name__ == "__main__":
    doctor_agent.run()