import re
from tkinter import messagebox, filedialog
from verifier import main as verifier_main
from ..registers import alphanumeric_blocks, numeric_blocks


def start():
    file = filedialog.askopenfilename(
        title="Select a TXT file",
        filetypes=[("Text files", "*.txt")]
    )

    if not file:
        messagebox.showinfo("No file selected", "No file was selected. Exiting the program.")
        return

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    process_lines(content)


def process_lines(file_content: str):
    lines = file_content.strip().splitlines()
    total_lines = len(lines)
    valid_count = 0
    errors = []

    record_blocks = {
        "0": numeric_blocks.block_0,
        "1": numeric_blocks.block_1,
        "9": numeric_blocks.block_9,
        "B": alphanumeric_blocks.block_B,
        "C": alphanumeric_blocks.block_C,
        "D": alphanumeric_blocks.block_D,
        "E": alphanumeric_blocks.block_E,
        "G": alphanumeric_blocks.block_G,
        "H": alphanumeric_blocks.block_H,
        "K": alphanumeric_blocks.block_K,
    }

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()

        if not line:
            continue

        if not line.startswith("|") or len(line) < 6:
            errors.append(f"Line {line_num}: Malformed line")
            continue

        block_id = line[1]
        record_id = line[1:5]

        if block_id not in record_blocks:
            errors.append(f"Line {line_num}: Unknown block '{block_id}'")
            continue

        block = record_blocks[block_id]

        if record_id not in block:
            errors.append(f"Line {line_num}: Unknown record type '{record_id}'")
            continue

        pattern = block[record_id]

        if not isinstance(pattern, re.Pattern):
            pattern = re.compile(pattern)
            block[record_id] = pattern

        if pattern.fullmatch(line):
            valid_count += 1
        else:
            errors.append(f"Line {line_num}: Invalid format for record type {record_id}")

    if errors:
        messagebox.showwarning(
            "Validation Results",
            f"Validation completed with {len(errors)} errors.\nCheck file for details."
        )
    else:
        messagebox.showinfo(
            "Validation Results",
            f"All {total_lines} lines validated successfully!"
        )


def main():
    verifier_main()
    start()


if __name__ == "__main__":
    main()