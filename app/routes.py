from app.models import ChatInput, ChatOutput
from app import app, client, companyName, custName

llmMessages = [
    {
        "role": "system",
        "content": f"""You are an expert customer support agent for a FinTech companyName called `{companyName}`, you are having an interaction over WhatsApp with a customer named `{custName}`.
They are a new customer and do not have any portfolio at {companyName} and you want to convince {custName} to open a demat account at {companyName}.
Respond to the customer in 20 words.""",
    }
]


@app.post("/chat")
def call_llm(request_body: ChatInput) -> ChatOutput:

    llmMessages.append({"role": "user", "content": request_body.user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=llmMessages,
    )

    llm_response_str = response.choices[0].message.content
    llmMessages.append({"role": "assistant", "content": llm_response_str})
    result = ChatOutput(success=True, message=llm_response_str)
    return result
