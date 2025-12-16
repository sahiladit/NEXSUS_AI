import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from agent.tools import run_verify_person, run_npi_lookup, run_crawl
from agent.extrainfo_agent import run_extrainfo


load_dotenv()

client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "verify_person",
            "description": "Runs full identity verification: NPI lookup + Web crawling.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "npi": {"type": "string"}
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "npi_lookup",
            "description": "Fetch raw NPI registry information.",
            "parameters": {
                "type": "object",
                "properties": {"npi": {"type": "string"}},
                "required": ["npi"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "quick_crawl",
        "description": "Perform web crawl and fuzzy match extra info",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "max_pages": {"type": "integer"},
                "extra_info": {
                    "type": "object",
                    "additionalProperties": {"type": "string"}
                }
            },
            "required": ["name"]
        }
    }
}


]




def call_model_and_act(user_text: str, model="gpt-4o-mini"):

    system_prompt = ("You are Nexsus-AI, an autonomous identity verification agent.\n\n"
    "The user provides:\n"
    "- name\n"
    "- optional NPI\n"
    "- optional extra_info (email, address, city, state, org)\n\n"
    "Your job:\n"
    "1. If NPI is provided, call npi_lookup.\n"
    "2. ALWAYS call quick_crawl and include extra_info in arguments.\n"
    "3. Use fuzzy matching to verify extra_info against scraped data.\n"
    "4. Return structured reasoning and results.\n\n"
    "IMPORTANT:\n"
    "- When calling quick_crawl, you MUST pass extra_info.\n" )


    # FIRST CALL — let the model choose which tool to use
    first = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        tools=TOOLS,
        tool_choice="auto"
    )

    first_msg = first.choices[0].message
    tool_calls = first_msg.tool_calls

    if not tool_calls:
        return json.dumps({
            "tool_selected": None,
            "agent_reasoning": first_msg.get("content", "")
        }, indent=4)

    # RUN THE TOOL(s)
    tool_outputs = []
    tool_messages = []

    if isinstance(user_text, str):
        try:
            user_data = json.loads(user_text)
        except Exception:
            user_data = {}
    else:
        user_data = user_text

    extra_info = user_data.get("extra_info", {})
    usr_add = extra_info.get("address")
    usr_city = extra_info.get("city")
    usr_state = extra_info.get("state")
    usr_email = extra_info.get("email")

    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Execute locally
        if name == "verify_person":
            output = run_verify_person(args.get("name"), args.get("npi"))
        elif name == "npi_lookup":
            output = run_npi_lookup(args.get("npi"))
        elif name == "quick_crawl":
              web_results = run_crawl(args["name"], args.get("max_pages", 5))

              extra_info = {
                "address": usr_add,
                "city": usr_city,
                "state": usr_state,
                "email": usr_email
              }   


              extrainfo_result = None
              if extra_info:
                  extrainfo_result = run_extrainfo(
                      args["name"],
                      extra_info,
                      web_results
                  )
              
              output = {
                    "web_results": web_results,
                    "fuzzy_score": extrainfo_result["score"] if extrainfo_result else 0,
                    "fuzzy_status": extrainfo_result["status"] if extrainfo_result else "NOT_RUN",
                    "fuzzy_report": extrainfo_result["report"] if extrainfo_result else [],
            }



        else:
            output = {"error": "unknown tool"}

        tool_outputs.append({"name": name, "args": args, "output": output})

        tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": name,
            "content": json.dumps(output)
        })

    # SECOND CALL — reasoning + final output
    second = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
            first_msg,
            *tool_messages,
            {"role": "system", "content": "Explain your reasoning then output final JSON."}
        ]
    )

    reasoning_text = second.choices[0].message.content

    return json.dumps({
        "tool_selected": [t["name"] for t in tool_outputs],
        "tool_arguments": [t["args"] for t in tool_outputs],
        "tool_output": [t["output"] for t in tool_outputs],
        "agent_reasoning": reasoning_text
    }, indent=4)

