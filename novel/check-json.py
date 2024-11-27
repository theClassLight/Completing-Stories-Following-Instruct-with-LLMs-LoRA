import json
import pandas as pd

file_path = 'segment_label/corpus_processed.json'

try:
   with open(file_path, 'r', encoding='utf-8') as f:
       data = json.load(f)
   df = pd.DataFrame(data)
except json.JSONDecodeError as e:
   print(f"JSON 解码错误: {e}")
except FileNotFoundError:
   print(f"文件 {file_path} 不存在")
