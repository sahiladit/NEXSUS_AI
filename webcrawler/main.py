from agent.agent import call_model_and_act
from agent.tools import run_verify_person, run_npi_lookup, run_crawl


if __name__ == "__main__":
    name = input("Enter person's name: ").strip()
    npi  = input("Enter NPI (optional): ").strip()

    if npi:
        user_prompt = f"Verify the person named '{name}' using NPI '{npi}' and web crawling. Return structured reasoning and results."
    else:
        user_prompt = f"Verify the person named '{name}' using web crawling and return structured reasoning and results."

    out = call_model_and_act(user_prompt)
    print(out)



# eg names : Male Names
# Ethan Miller
# Jacob Anderson
# Michael Thompson
# Daniel Harris
# Ryan Walker
# Female Names
# Emily Parker
# Sophia Bennett
# Olivia Carter
# Madison Lewis
# Grace Mitchell 