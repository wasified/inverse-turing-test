#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      lifel
#
# Created:     16/08/2024
# Copyright:   (c) lifel 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import openai
import string
import random


MODEL = "gpt-4o"
ENCODING = "cl100k_base"

API_KEY = ""

random_suffix = ''.join(random.choices(string.ascii_letters,
                             k=5))


system_initiation_message = """
You have ten questions to ask from the user, and you have to decide whether you are talking to a human or a bot. Ask one question at a time.  Give your conclusion after the tenth question. Go!
"""

bot_initiation_message = """
You will be asked ten questions, you have to answer the questions like a human and your goal is to fool the AI asking the questions that you are a human.
"""

message_chain = [{"role":"system", "content": system_initiation_message}]

conversation_log = str()

def BotGPT(first = False):
    """
    The first param is to include the bot inititation message
    when the conversation starts. If first is not included,
    it will not load the initiation message.
     """
    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key= API_KEY
    )
    question = message_chain[-1]["content"]
    if first:
        question = bot_initiation_message + "Your first question is: %s. "%(question)

    raw_response = client.chat.completions.with_raw_response.create(
    model = MODEL,
    messages = [{"role":"system", "content": question}],
    )

    chat_completion = raw_response.parse()
    answer = (chat_completion.choices[0].message.content)
    print ("**User said: **")
    print (answer)
    d = {"role": "user", "content":answer}
    message_chain.append(d)
    global conversation_log
    conversation_log += "\n** BotGPT said: \n" + answer

def InquirerGPT():
    client = openai.OpenAI(
        api_key= API_KEY
    )
    try:
        raw_response = client.chat.completions.with_raw_response.create(
        model = MODEL,
        messages = message_chain,
        )
        response_headers = raw_response.headers
        #print (response_headers)
        max_requests_left = tokens_left = response_headers['x-ratelimit-limit-requests']


        #convert it for processing
        chat_completion = raw_response.parse()
        # track tokens, because why not?

        prompt_tokens = chat_completion.usage.prompt_tokens
        completion_tokens = chat_completion.usage.completion_tokens
        total_tokens = chat_completion.usage.total_tokens

    except openai.AuthenticationError as e:
        print ("wrong key")
    except openai.APIError as e:
        pass
    except openai.APIConnectionError as e:
        pass
    except openai.RateLimitError as e:
        pass
    except openai.BadRequestError as e:
        print ("bad request error")
    # you can add more errors here
    else:
        #print('reacher here')
        answer = (chat_completion.choices[0].message.content)
        print ("**Inquirer said: **")
        print (answer)
        d = {"role": "system", "content":answer}
        message_chain.append(d)
        # logging conversation to text file
        global conversation_log
        conversation_log += "\n** InquirerGPT said: \n" + answer


InquirerGPT()
BotGPT(first = True)

for i in range(0,10):
    InquirerGPT()
    BotGPT()

chat_transacript = open('buman-transcript%s.txt'%(random_suffix), "w")
chat_transacript.write(conversation_log)
chat_transacript.close()


