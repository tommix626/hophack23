import openai
from newsplease import NewsPlease
from newsapi import NewsApiClient
import re

# url = input('enter your news url')
url = 'https://www.foxnews.com/politics/us-china-trade-war-larry-kudlow-chuck-grassley-donald-trump-roy-blunt-kevin-cramer'


class GPTReader:
    def __init__(self):
        self.url = None
        self.title = 'Title'
        self.api_key = None
        self.response = None
        self.accuracy_score = 5
        self.aggressive_score = 5
        self.satire_score = 5
        self.credibility_score = 5
        self.objective_score = 5
        self.accuracy_pair = []  # contains pairs (text, explanation)
        self.aggressive_pair = []
        self.genre = []
        self.context = []
        self.audience = ""
        self.topic = ""

        try:
            with open('api_key_private.txt', 'r') as file:
                # Read the entire content of the file into a string
                self.api_key = file.read()

                # Print the string read from the file
                # print("String read from the file:")
                # print(api_key)
        except FileNotFoundError:
            print("The file 'api_key.txt' was not found.")
        except Exception as e:
            print("An error occurred:", str(e))

    def run(self, url):

        print('getting news article for url', url)
        article = NewsPlease.from_url(url)
        if article == {}:
            raise ValueError('invalid URL')

        self.url = url
        try:
            with open('prompt.txt') as prompt_file:
                prompt = prompt_file.read()
                user_input = prompt + article.maintext
                self.title = article.title
                openai.api_key = self.api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input},
                    ]
                )
                chatbot_response = response['choices'][0]['message']['content']
                print("Chatbot:", chatbot_response)
                self.response = chatbot_response
                '''
                try:
                with open('sample_gpt_response.txt') as f:
                self.response = f.read()'''
                self.__parse_response()
        except FileNotFoundError:
            print("The file 'prompt.txt' was not found.")
            return "error"

    def __parse_response(self):
        text = self.response

        print('getting accuracy score...')
        accuracy_score_text = re.findall(r'!!([a-zA-Z0-9\s]+)!!', text, re.MULTILINE)
        self.accuracy_score = int(accuracy_score_text[0])
        print('accuracy_score: ', self.accuracy_score)

        print('getting aggressive score...')
        aggressive_score_text = re.findall(r'~([a-zA-Z0-9\s]+)~', text, re.MULTILINE)
        self.aggressive_score = int(aggressive_score_text[0])
        print('aggressive score:', self.aggressive_score)

        print('getting satire score...')
        satire_score_text = re.findall(r'\^([a-zA-Z0-9\s]+)\^', text, re.MULTILINE)
        self.satire_score = int(satire_score_text[0])
        print('satire score:', self.satire_score)

        print('getting credibility score...')
        credibility_score_text = re.findall(r'\\\\([a-zA-Z0-9\s]+)\\\\', text, re.MULTILINE)
        self.credibility_score = int(credibility_score_text[0])
        print('credibility score: ', self.credibility_score)

        print('getting objectivity score...')
        objective_score_text = re.findall(r'@@([a-zA-Z0-9\s]+)@@', text, re.MULTILINE)
        self.objective_score = int(objective_score_text[0])
        print('objective score: ', self.objective_score)

        print('getting accuracy texts and explanations...')
        accuracy_texts = re.findall(r'\[([a-zA-Z0-9.,$%@&\'\-"\s]+)\]', text, re.MULTILINE)
        accuracy_explanations = re.findall(r'\{([a-zA-Z0-9.,$%\'\-"\s]+)\}', text, re.MULTILINE)
        self.accuracy_pair = list(zip(accuracy_texts, accuracy_explanations))
        print('accuracy texts and explanations...', self.accuracy_pair)

        print('getting aggressive texts and explanations...')
        aggressive_texts = re.findall(r'\|\|([a-zA-Z0-9.,$%@&\'\-"\s]+)\|\|', text, re.MULTILINE)
        aggressive_explanations = re.findall(r'//([a-zA-Z0-9.,$%\'\-"\s]+)//', text, re.MULTILINE)
        self.aggressive_pair = list(zip(aggressive_texts, aggressive_explanations))
        print('aggressive texts and explanations...', self.aggressive_pair)

        print('getting genre...')
        self.genre = re.findall(r';;([a-zA-Z0-9.,&%$@\'\-"\s]+);;', text, re.MULTILINE)
        self.genre = [e.capitalize() for e in self.genre]
        print('genre: ', self.genre)

        print('getting context...')
        self.context = re.findall(r'\$\$([a-zA-Z0-9.,&%@\'\-"\s]+)\$\$', text, re.MULTILINE)
        self.context = [e.capitalize() for e in self.context]
        print('context: ', self.context)

        print('getting audience...')
        self.audience = re.findall(r'<<([a-zA-Z0-9.,&%$@\'\-"\s]+)>>', text, re.MULTILINE)[0]
        print('audience: ', self.audience)

        print('getting topic...')
        self.topic = re.findall(r'%%([a-zA-Z0-9.,&$@\'\-"\s]+)%%', text, re.MULTILINE)[0]
        print('topic: ', self.topic)

    def get_similar_sources(self):
        assert(self.topic != '')

        similar = NewsApiClient(api_key='c7e38430c3ba4f0fbc698db57ea9ad7c').get_everything(q=self.topic)['articles']
        similar_url = [e['url'] for e in similar[:min(len(similar), 10)]]
        similar_title = [e['title'] for e in similar[:min(len(similar), 10)]]

        return list(zip(similar_title, similar_url))
