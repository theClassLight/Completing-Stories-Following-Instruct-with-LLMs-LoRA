import json

file_path = 'segment_label/corpus_processed.json'
output_file_path = 'segment_label/corpus_processed.json'

try:
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除 "]["
    cleaned_content = content.replace('],[', ',')

    # 将处理后的内容重新保存为 JSON 文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"文件已成功处理并保存为 {output_file_path}")

except FileNotFoundError:
    print(f"文件 {file_path} 不存在")
except Exception as e:
    print(f"处理文件时发生错误: {e}")
