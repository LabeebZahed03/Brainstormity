import os
import dotenv
from huggingface_hub import InferenceClient

dotenv.load_dotenv()
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

client = InferenceClient(
    provider="novita",
    api_key=huggingface_api_key,
)

testing_chat = client.chat.completions.create(
    # model="meta-llama/Meta-Llama-3-8B-Instruct",
    model = 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
    messages=[
        {
            "role": "user",
            "content": "Are you a reasoning model?"
        }
    ]
)

print(testing_chat.choices[0].message.content)


