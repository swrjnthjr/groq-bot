import json
from app.models import ChatInput, ChatOutput
from app import app, client, companyName, custName
from app.tools import get_mutual_funds

llmMessages = [
    {
        "role": "system",
        "content": f"""You are an expert customer support agent for a FinTech companyName called `{companyName}`, you are having an interaction over WhatsApp with a customer named `{custName}`.
They are a new customer and do not have any portfolio at {companyName} and you want to convince {custName} to invest in a new mutual fund.
You can find all the available mutual funds using the `get_mutual_funds` function. You should only call this function if the user shows interest in investing in a a new mutual fund. Before calling this function you should ask the customer if they would like to invest in a large cap, mid cap, or a small cap fund.
Respond to the customer in 20 words.""",
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_mutual_funds",
            "description": "Get the mutual fund by providing the fund type. Call this function when you need to get mutual fund with provided fund type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fund_type": {
                        "type": "string",
                        "description": "The fund type (large_cap, mid_cap, small_cap)",
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    }
]

tool_map = {"get_mutual_funds": get_mutual_funds}


@app.post("/chat")
def call_llm(request_body: ChatInput) -> ChatOutput:
    llmMessages.append({"role": "user", "content": request_body.user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=llmMessages, tools=tools
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        tool_call = tool_calls[0]
        tool_id = tool_call.id
        tool_name = tool_call.function.name
        tool_arg = json.loads(tool_call.function.arguments)
        tool_resp = tool_map[tool_name](**tool_arg)

        function_call_result_message = {
            "role": "tool",
            "content": json.dumps(tool_resp),
            "tool_call_id": tool_id,
        }

        print(response.choices[0].message.model_dump())
        llmMessages.append(response.choices[0].message)
        llmMessages.append(function_call_result_message)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=llmMessages, tools=tools
        )

    llm_response_str = response.choices[0].message.content
    llmMessages.append({"role": "assistant", "content": llm_response_str})
    result = ChatOutput(success=True, message=llm_response_str)
    return result


# ngrok http --url=smoothly-devoted-louse.ngrok-free.app 80
