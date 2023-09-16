import openai
from newsplease import NewsPlease

'''
GETTING NEWS TEXT FROM URL
'''
#url = input('enter your news url')
url = 'https://www.foxnews.com/politics/us-china-trade-war-larry-kudlow-chuck-grassley-donald-trump-roy-blunt-kevin-cramer'
print('getting news article for url', url)
article = NewsPlease.from_url(url)
text = article.maintext


'''
SETTING UP OPENAI
'''
# Your API key from OpenAI
try:
    with open('api_key.txt', 'r') as file:
        # Read the entire content of the file into a string
        api_key = file.read()

        # Print the string read from the file
        # print("String read from the file:")
        # print(api_key)
except FileNotFoundError:
    print("The file 'api_key.txt' was not found.")
except Exception as e:
    print("An error occurred:", str(e))

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


try:
    with open('prompt.txt') as promt_file:
        prompt = promt_file.read()
        user_input = prompt + article.maintext
        chatbot_response = chat_with_gpt3(user_input)
        print("Chatbot:", chatbot_response)
except FileNotFoundError:
    print("The file 'prompt.txt' was not found.")

#write me a program of a chatbot using the gpt-3.5-turbo model's API in python