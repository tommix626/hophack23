import openai

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

# Main conversation loop
print("Chatbot: Hello! How can I assist you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    user_input = \
        """
        I am a person who does not know anything about the current news, and I am browsing through numerous news articles trying to discern truthful news from falsy ones. Pretend you were a news critic who analyzes news articles and cross compare it with other articles on the same topic. Your goal is not to be an AI assistant, I want you to fully immerse yourself into the role. When I give you a piece of text from a news article, I want you to analyze the following information on the news article. In addition, the article is from a website and may contain irrelevant information such as advertisement and image captions, I want you to ignore them.

For the analysis, I need you to provide it in a very specific format. This includes the use of special characters in your response. 
1. Accuracy Score on a scale of 1-10: I want you to tell me how similar this article is from what you already know about this topic. Remember that I do not want you to maintain neutral. I want you to be as critical as possible. 
I want you to provide the accuracy score in asterisks. For example, if the accuracy score is 7, I want you to write *7*.

2. I want you to provide quotes from the article. I want at least 3 quotes that are either truthful or misleading. For each quote, please explain why it is misleading or truthful. I do not want each quote to be too long, each quote must be less than 500 characters.
For each quote, I want you to provide the code in squared brackets and explanations in curly brackets. For example: [this is a quote]—{this is the explanation}.

3. Tone Score on a scale of 1-10: I want you to tell me how aggressive or exaggerating the language of the article is. I want you to find this information through the use of vocabulary in this article. Any use of strong action verbs or adjectives are all instances of strong aggressive language. Do not say that every article has a neutral tone. If an article has a slightly aggressive tone, I want you to say it is very aggressive. 
I want you to provide the tone score in tildes, for example, if the score is 3, then I want you to print ~3~.


4. I want you to provide at least 3 places in this article that has a strong tone compared to the rest of the article, as explained in number 3. For each quote, I want you to provide an explanation as to why it appears to have a strong language. I do not want each quote to be too long, each quote must be less than 500 characters.
For each quote, I want you to provide the code in vertical bars and explanations in forward slashing lines. For example: |this is a quote|—/this is the explanation/.

5. I want you to analyze the genre of this article. I want you to analyze the sectors that this article should be categorized in, such as economics, trade, sports, or feminism. I want you to provide the genre in 2-3 tags that consist of 1-2 words. The tags need to be preceded and ended by a semicolon. For example, I can write ;economics;,;international trade;,;abortion;

6. I want you to analyze the historical context of this article. I want you to analyze the events that led to the creation of this article. I want you to provide the historical context in a couple of tags that consist of a few words. The tags need to be preceded and ended by a colon. For example, I can write :China-US relations:,:trade war:,:trump presidency:

7. I want you to use 2-3 sentences to describe the intended audience and the purpose of this article. The intended audience needs to be as specific as possible, do not simply write something like “the readers of this article”. Make sure the audience is a very specific target group in society, for example, if the article is about the US-China trade war, the intended audience can be as specific as Chinese Immigrants in the US. I want you to provide this information in angled brackets. For example: <Chinese Immigrants in the US who are concerned about US relations with their home country>

"""
    chatbot_response = chat_with_gpt3(user_input)
    print("Chatbot:", chatbot_response)

#write me a program of a chatbot using the gpt-3.5-turbo model's API in python