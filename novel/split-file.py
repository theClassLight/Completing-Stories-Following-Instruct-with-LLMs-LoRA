import os
import argparse

def split_text_file(input_file, output_dir, lines_per_file):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 计算总行数
    total_lines = len(lines)
    num_files = (total_lines + lines_per_file - 1) // lines_per_file

    # 分割数据并保存
    for i in range(num_files):
        start = i * lines_per_file
        end = min((i + 1) * lines_per_file, total_lines)
        file_lines = lines[start:end]

        output_file = os.path.join(output_dir, f'part_{i+1}.txt')
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(file_lines)

    print(f"Split {input_file} into {num_files} files in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a text file into multiple smaller files.")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_dir", help="Directory to save the split files")
    parser.add_argument("lines_per_file", type=int, help="Number of lines per split file")

    args = parser.parse_args()

    split_text_file(args.input_file, args.output_dir, args.lines_per_file)
