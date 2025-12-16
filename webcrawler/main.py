from agent.agent import call_model_and_act
import json

if __name__ == "__main__":
    name = input("Enter person's name: ").strip()
    npi = input("Enter NPI (optional): ").strip()

    email = input("Enter email (optional): ").strip()
    address = input("Enter address (optional): ").strip()
    city = input("Enter city (optional): ").strip()
    state = input("Enter state (optional): ").strip()

    user_prompt = json.dumps({
    "task": "verify_identity",
    "name": name,
    "npi": npi,
    "extra_info": {
        "email": email,
        "address": address,
        "city": city,
        "state": state
    } }, indent=2)

    user_prompt = {
    "name": name,
    "npi": npi,
    "extra_info": {
        "address": address,
        "city": city,
        "state": state,
        "email": email
    }
}

    result = call_model_and_act(json.dumps(user_prompt))
    print(result)


