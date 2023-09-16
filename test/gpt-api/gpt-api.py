import openai

# Your API key from OpenAI
api_key = "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"

# Function to interact with the chatbot using a more powerful model and longer responses
def chat_with_gpt3(prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']

# Main conversation loop
print("Chatbot: Hello! How can I assist you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    chatbot_response = chat_with_gpt3("User: " + user_input)
    print("Chatbot:", chatbot_response)

#write me a program of a chatbot using the gpt-3.5-turbo model's API in python