import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 检查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 1. 加载预训练模型和标记器
model_name = "/remote-home/modelscope/hub/Qwen/Qwen2___5-7B-Instruct"  # 替换为你的模型路径
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# 2. 加载LoRA配置
lora_config_path = "./output/lora_model"  # 替换为你的LoRA配置路径

# 3. 应用LoRA配置到模型
model = PeftModel.from_pretrained(model, lora_config_path).to(device)

# 4. 设置模型为评估模式
model.eval()

# 5. 保存融合后的模型
output_model_path = "./output/fused_model"  # 替换为你希望保存的路径
model.save_pretrained(output_model_path)
tokenizer.save_pretrained(output_model_path)

print(f"融合后的模型已保存到: {output_model_path}")
