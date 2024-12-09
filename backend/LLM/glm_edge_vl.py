# https://huggingface.co/THUDM/glm-edge-v-2b

import torch
from PIL import Image
from transformers import (
    AutoTokenizer,
    AutoImageProcessor,
    AutoModelForCausalLM,
)

url = "img.png"
url = r"E:\ocr\data\note.jpg"

messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "tell me the content"}]}]
image = Image.open(url)

MODEL_PATH = "THUDM/glm-edge-v-5b"
local_model_dir = 'E:\llm\models'

# huggingface-cli download --resume-download --local-dir-use-symlinks False THUDM/glm-edge-v-5b --local-dir E:\llm\models\glm-edge-v-5b


tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, cache_dir=local_model_dir)
processor = AutoImageProcessor.from_pretrained(MODEL_PATH, trust_remote_code=True, cache_dir=local_model_dir)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True, cache_dir=local_model_dir)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    #device_map="auto",
    trust_remote_code=True,
    cache_dir=local_model_dir
)

inputs = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, return_dict=True, tokenize=True, return_tensors="pt"
).to(next(model.parameters()).device)

generate_kwargs = {
    **inputs,
    "pixel_values": torch.tensor(processor(image).pixel_values).to(next(model.parameters()).device),
}
output = model.generate(**generate_kwargs, max_new_tokens=100)
print(tokenizer.decode(output[0][len(inputs["input_ids"][0]):], skip_special_tokens=True))
