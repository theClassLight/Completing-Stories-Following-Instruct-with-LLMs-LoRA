import torch
from torch.amp import autocast
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

def generate_text(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=5000,truncation=True, truncation_strategy='longest_first', return_attention_mask=True).to(device)
    input_ids = inputs["input_ids"].to(device)  # 确保 device 是你的设备（CPU 或 GPU）

    # 确保 input_ids 是 Long 类型
    if not input_ids.dtype == torch.long:
        input_ids = input_ids.to(torch.long)
    with autocast(device.type):
        outputs = model.generate(input_ids=input_ids, max_new_tokens=1200)
        generated_inner_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_inner_text

# 5. 命令行交互
while True:
    input_text = input("请输入文本 (输入 'exit' 退出): ")
    if input_text.lower() == 'exit':
        break
    generated_text = generate_text(input_text)
    print(generated_text)

# 释放缓存
torch.cuda.empty_cache()
