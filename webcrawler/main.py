from agent.agent import call_model_and_act
import json

if __name__ == "__main__":
    name = input("Enter person's name: ").strip()
    npi = input("Enter NPI : ").strip()

    email = input("Enter email : ").strip()
    practice_name = input("Enter Practice Name (Hospital) : ").strip()
    city = input("Enter city : ").strip()
    state = input("Enter state : ").strip()

    user_prompt = json.dumps({
    "task": "verify_identity",
    "name": name,
    "npi": npi,
    "extra_info": {
        "email": email,
        "practice_name": practice_name,
        "city": city,
        "state": state
    } }, indent=2)

    user_prompt = {
    "name": name,
    "npi": npi,
    "extra_info": {
        "practice_name": practice_name,
        "city": city,
        "state": state,
        "email": email
    }
}

    result = call_model_and_act(json.dumps(user_prompt))
    print(result)

#always do git push origin branch_name
