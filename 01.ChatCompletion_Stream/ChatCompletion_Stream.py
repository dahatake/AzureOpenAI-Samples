# Reference - https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb

# imports
import openai  # for OpenAI API calls
import time  # for measuring time duration of API calls
import json
import os

# Load config values
with open(r'config.json') as config_file:
    config_details = json.load(config_file)
    
# Setting up the deployment name
chatgpt_model_name = config_details['CHATGPT_MODEL']
openai.api_type = "azure"
openai.api_key = os.getenv('OPENAI_API_KEY') # export OPENAI_API_KEY=xxx
openai.api_base = config_details['OPENAI_API_BASE']
openai.api_version = config_details['OPENAI_API_VERSION']

message="100まで数えてください。数字と数字の間はカンマを入れて、改行はしないでください。例: 1, 2, 3, ..."

# 1. Start Typical
print(f"1. 典型的なCompletion呼び出し (stream=false - デフォルト)")
# record the time before the request is sent
start_time = time.time()


print(f"Prompt: {message}")
# send a ChatCompletion request to count to 100
response = openai.ChatCompletion.create(
    engine=chatgpt_model_name,
    messages=[
        {'role': 'user', 'content': '100まで数えてください。数字と数字の間はカンマを入れて、改行はしないでください。例: 1, 2, 3, ...'}
    ],
    temperature=0
)

# calculate the time it took to receive the response
response_time = time.time() - start_time

# print the time delay and text received
reply_content = response['choices'][0]['message']['content']
print(f"実行時間: {response_time:.2f}秒")
print(f"Response: \n{reply_content}\n")

# 2.Stream = true
print(f"#2. Stream オプション付き (stream=true)")

# Example of an OpenAI ChatCompletion request with stream=True
# https://platform.openai.com/docs/guides/chat

# record the time before the request is sent
start_time = time.time()

# send a ChatCompletion request to count to 100
response = openai.ChatCompletion.create(
    engine=chatgpt_model_name,
    messages=[
        {'role': 'user', 'content': '100まで数えてください。数字と数字の間はカンマを入れて、改行はしないでください。例: 1, 2, 3, ...'}
    ],
    temperature=0,
    stream=True  # we set stream=True
)

# create variables to collect the stream of chunks
collected_chunks = []
collected_messages = []
initial_response=True
# iterate through the stream of events
for chunk in response:
    chunk_time = time.time() - start_time  # calculate the time delay of the chunk
    collected_chunks.append(chunk)  # save the event response
    if 'choices' in chunk:
        if len(chunk['choices']) > 0:
            if 'delta' in chunk['choices'][0]:
                if 'content' in chunk['choices'][0]['delta']:
                    if initial_response:
                            initial_time = time.time() - start_time  # calculate the time delay of the chunk
                            print(f"初回待ち時間: {initial_time:.2f}秒")                        
                            initial_response=False
                    chunk_message = chunk['choices'][0]['delta']['content']  # extract the message
                    print(f"{chunk_message}", end='')  # print the delay and text
#                    collected_messages.append(chunk_message)  # save the message

# print the time delay and text received
response_time = time.time() - start_time
print(f"実行時間: {response_time:.2f}秒")

#full_reply_content = ''.join(collected_messages)
# full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
#print(f"Response: \n{full_reply_content}")