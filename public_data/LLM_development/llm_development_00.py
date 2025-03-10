# Building a Local LLM

# Package
from gpt4all import GPT4All
from nomic import embed

# Model
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf") # downloads / loads a 4.66GB LLM
with model.chat_session():
    print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))


output = embed.text(
    texts=['Nomic Embedding API', '#keepAIOpen'],
    model='nomic-embed-text-v1.5',
    task_type='search_query',
    inference_mode='dynamic',
)

mode = output['inference_mode']  # 'local'

output = embed.text(
    texts=['Nomic Embedding API'] * 50,
    model='nomic-embed-text-v1.5',
    task_type='search_query',
    inference_mode='remote',
)

mode = output['inference_mode']  # 'remote'