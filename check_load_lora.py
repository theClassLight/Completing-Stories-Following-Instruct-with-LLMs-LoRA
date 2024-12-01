import torch
from torch.cuda.amp import autocast
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 检查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 1. 加载预训练模型和标记器
model_name = "/remote-home/modelscope/hub/Qwen/Qwen2___5-3B-Instruct"  # 替换为你的模型路径
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# 2. 加载LoRA配置
lora_config_path = "./output_3b_1/lora_model"  # 替换为你的LoRA配置路径

# 3. 应用LoRA配置到模型
model = PeftModel.from_pretrained(model, lora_config_path).to(device)

# 4. 设置模型为评估模式
model.eval()

# 5. 使用模型进行推理
input_text = "请按照以下描述续写小说：背景：第二次世界大战北非战场\n剧情梗概：克里斯汀在得知盟军即将登陆后，决定独自驾机迎战敌方运输机群，临行前与地勤组告别并承诺如果情况危急请投降以保全性命。"
inputs = tokenizer(input_text, return_tensors="pt",max_length=5000).to(device)
with autocast():
    outputs = model.generate(**inputs,max_new_tokens=4000)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text)

# 释放缓存
torch.cuda.empty_cache()
