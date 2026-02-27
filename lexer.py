import re


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

                # Output <type, token> list
                if token_type == "keyword":
                    tokens.append(f"<key,{token_value}>")
                elif token_type == "identifier":
                    tokens.append(f"<id,{token_value}>")
                elif token_type == "operator":
                    tokens.append(f"<op,{token_value}>")
                elif token_type == "string_literal":
                    tokens.append(f"<string_literal,{token_value}>")
                elif token_type == "float_literal":
                    tokens.append(f"<float_literal,{token_value}>")
                elif token_type == "int_literal":
                    tokens.append(f"<int_literal,{token_value}>")
                else:
                    tokens.append(f"<separator,{token_value}>")

                # Cuts first token from LOC
                line_to_cut = line_to_cut[len(token_value) :]

                matched = True
                break

        if not matched:
            print(f" Skipping unexpected char: '{line_to_cut[0]}'")
            line_to_cut = line_to_cut[1:]

    # Prints output list
    print(f"Output <type, token> list: {tokens}")
    return tokens
