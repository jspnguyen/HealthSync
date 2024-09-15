from uagents import Agent, Bureau, Context, Model
import random, string, os, requests, ast
from faker import Faker
from dotenv import load_dotenv
import main

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")
fake = Faker()

class Message(Model):
    message: str

def generate_random_string(length=128):
    letters = string.ascii_letters 
    return ''.join(random.choice(letters) for _ in range(length))

priority_agent = Agent(name="priority_level", seed=generate_random_string())
normal_add_agent = Agent(name="normal_add", seed=generate_random_string())
forced_add_agent = Agent(name="forced_add", seed=generate_random_string())

@priority_agent.on_interval(period=0.5)
async def priority_level(ctx: Context):
    messages = [
        {"role": "system", "content": "You are a patient priority decision system. Based on the following patient's priority, return only a number from 1-10 with up to 3 decimals on how prioritized the patient should be."},
        {"role": "user", "content": f"Patient has a paper cut"},
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

    urgency_score = float(res.text.strip('"'))
    ctx.logger.info(f"Patient Urgency Rating: {urgency_score}")
    
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
    
    messages = [
        {"role": "system", "content": "You are a hospital decision making system that chooses if a patient requires surgery. Reply with either True or False."},
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

    surgery_bool = res.text.strip('"')
    ctx.logger.info(f"Surgery Needed: {surgery_bool}")
    
    if urgency_score >= 9:
        await ctx.send(forced_add_agent.address, Message(message=f"{urgency_score}|{equipment}|{surgery_bool}"))
    else:
        await ctx.send(normal_add_agent.address, Message(message=f"{urgency_score}|{equipment}|{surgery_bool}"))

@normal_add_agent.on_message(model=Message)
async def normal_add_handler(ctx: Context, sender: str, msg: Message):
    value_list = msg.message.split("|")
    urgency_score = float(value_list[0])
    equipment = ast.literal_eval(value_list[1])
    surgery_bool = bool(value_list[2])
    
    patient_id = f"P{random.randint(1, 999999999)}"
    patient_name = f"{fake.first_name()} {fake.last_name()}"
    
    main.add_patient_to_graph(main.G, patient_id, patient_name, urgency_score, surgery_bool, equipment)
    
    ctx.logger.info(f"Normally added patient with {urgency_score} who needs {equipment} to the knowledge graph.")

@forced_add_agent.on_message(model=Message)
async def forced_add_handler(ctx: Context, sender: str, msg: Message):
    value_list = msg.message.split("|")
    urgency_score = float(value_list[0])
    equipment = ast.literal_eval(value_list[1])
    surgery_bool = bool(value_list[2])
    
    patient_id = f"P{random.randint(1, 999999999)}"
    patient_name = f"{fake.first_name()} {fake.last_name()}"
    
    main.add_patient_to_graph(main.G, patient_id, patient_name, urgency_score, surgery_bool, equipment)
    
    ctx.logger.info(f"Forced added patient with {urgency_score} who needs {equipment} to the knowledge graph.")

bureau = Bureau()
bureau.add(priority_agent)
bureau.add(normal_add_agent)
bureau.add(forced_add_agent)

if __name__ == "__main__":
    bureau.run()