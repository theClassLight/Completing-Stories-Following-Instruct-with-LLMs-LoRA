import re
import argparse

def clean_text(input_file_path, output_file_path):
    try:
        # 读取文件内容
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式查找并替换特定字符串模式
        pattern = r'###第\d+章 \d+ .+?###'
        replacement = ''  # 您可以根据需要定义替换内容
        cleaned_content = re.sub(pattern, replacement, content)

        # 将处理后的内容重新保存为 JSON 文件
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"文件已成功处理并保存为 {output_file_path}")

    except FileNotFoundError:
        print(f"文件 {input_file_path} 不存在")
    except Exception as e:
        print(f"处理文件时发生错误: {e}")

def main():
    parser = argparse.ArgumentParser(description="Clean text in JSON file by removing specific patterns.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input text file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to the output text file")

    args = parser.parse_args()

    clean_text(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
