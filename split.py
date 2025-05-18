def split_file(filepath, parts=10):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        lines = infile.readlines()

    total_lines = len(lines)
    lines_per_file = total_lines // parts

    for i in range(parts):
        start = i * lines_per_file
        end = start + lines_per_file if i < parts - 1 else total_lines
        with open(f'rockyou{i+1}.txt', 'w', encoding='utf-8') as outfile:
            outfile.writelines(lines[start:end])

    print(f"File split into {parts} parts.")

# Call the function
split_file('rockyou.txt', parts=25)
