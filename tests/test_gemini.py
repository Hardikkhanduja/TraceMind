from app.llm.gemini import llm

response = llm.invoke(
    "In one sentence, explain why an AI workflow might become slow."
)

print(response.content)
print(type(response.content))

print(response.content[0])
print(type(response.content[0]))