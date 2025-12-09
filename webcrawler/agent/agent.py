# agent/agent.py
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from agent.tools import run_verify_person, run_npi_lookup, run_crawl

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
            "description": "Perform a basic web crawl.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "max_pages": {"type": "integer"}
                },
                "required": ["name"]
            }
        }
    }
]


def call_model_and_act(user_text: str, model="gpt-4o-mini"):

    system_prompt = (
        "You are Nexsus-AI autonomous agent. "
        "You must decide which tool to call, run it, analyze the result, "
        "and return your reasoning + structured output."
    )

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

    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Execute locally
        if name == "verify_person":
            output = run_verify_person(args.get("name"), args.get("npi"))
        elif name == "npi_lookup":
            output = run_npi_lookup(args.get("npi"))
        elif name == "quick_crawl":
            output = run_crawl(args.get("name"), args.get("max_pages", 5))
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
