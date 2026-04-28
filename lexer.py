import re
import tkinter as tk
from tkinter import scrolledtext
from parser import parser

class TinyPieGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer for TinyPie")

        self.current_line = 0
        self.lines = []

        title = tk.Label(root, text="Lexical Analyzer for TinyPie", font=("Arial", 14))
        title.grid(row=0, column=0, columnspan=5, pady=10)

        tk.Label(root, text="Source Code Input:").grid(row=1, column=0)

        tk.Label(root, text="Lexical Analyzed Result:").grid(row=1, column=2)

        tk.Label(root, text="Parse Tree:").grid(row=1, column=4)

        self.input_box = scrolledtext.ScrolledText(root, width=40, height=10)
        self.input_box.grid(row=2, column=0, padx=10, pady=10)

        self.output_box = scrolledtext.ScrolledText(root, width=40, height=10)
        self.output_box.grid(row=2, column=2, padx=10, pady=10)

        self.parse_box = scrolledtext.ScrolledText(root, width=40, height=10)
        self.parse_box.grid(row=2, column=4, padx=10, pady=10)

        tk.Label(root, text="Current Processing Line:").grid(row=3, column=0, sticky="e")

        self.line_var = tk.StringVar(value="0")
        self.line_display = tk.Entry(root, textvariable=self.line_var, width=5, justify='center')
        self.line_display.grid(row=3, column=1, sticky="w")

        self.next_button = tk.Button(root, text="Next Line", command=self.next_line)
        self.next_button.grid(row=4, column=1, pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.grid(row=4, column=2, pady=10)

        self.quit_button = tk.Button(root, text="Restart", command=self.restart)
        self.quit_button.grid(row=4, column=3, pady=10)

    def next_line(self):
        if self.current_line == 0:
            text = self.input_box.get("1.0", tk.END)
            self.lines = text.splitlines()

        # skip blank lines
        while self.current_line < len(self.lines) and not self.lines[self.current_line].strip():
            self.current_line += 1

        if self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            line_num = self.current_line + 1

            # run lexer on this line
            tokens = CutOneLineTokens(line)
            self.output_box.insert(tk.END, f"---- Line {line_num} ----\n")
            for tok in tokens:
                self.output_box.insert(tk.END, tok + "\n")
            self.output_box.insert(tk.END, "\n")

            # run parser and show parse tree
            tree_output = parser(tokens, line_num)
            self.parse_box.insert(tk.END, f"####Parse tree for line {line_num}####\n")
            self.parse_box.insert(tk.END, tree_output + "\n\n")

            self.current_line += 1
            self.line_var.set(str(self.current_line))

    def restart(self):
        self.input_box.delete("1.0", tk.END)

        self.output_box.delete("1.0", tk.END)

        self.parse_box.delete("1.0", tk.END)

        self.lines = []

        self.current_line = 0

        self.line_var.set("0")

def CutOneLineTokens(program_code):
    """
    Tokenize one line of TinyPie code
    Returns list of <type, token> strings
    """
    # Output list starting from empty list
    tokens = []

    # Starts with the full line
    line_to_cut = program_code.strip()

    # Token patterns in order
    patterns = [
        ("string_literal", r'^"[^"]*"'),  # test first
        ("float_literal", r"^\d+\.\d+"),  # test before int literals
        ("keyword", r"^(if|else|int|float)\b"),  # \b ensures whole word match
        ("int_literal", r"^\d+"),  # test after floats
        ("identifier", r"^[a-zA-Z]+[a-zA-Z0-9]*"),
        ("operator", r"^[=+>*]"),
        ("separator", r'^[\(\):;"]'),
    ]

    while line_to_cut:
        # Skips whitespace before next token
        if line_to_cut[0] == " ":
            line_to_cut = line_to_cut[1:]
            continue

        matched = False

        for token_type, pattern in patterns:
            match = re.match(pattern, line_to_cut)
            if match:
                token_value = match.group(0)

                tokens.append(f"<{token_type},{token_value}>")

                line_to_cut = line_to_cut[len(token_value) :]

                matched = True
                break

        if not matched:
            print(f" Skipping unexpected char: '{line_to_cut[0]}'")
            line_to_cut = line_to_cut[1:]

    # Prints output list
    print(f"Output <type, token> list: {tokens}")
    return tokens
