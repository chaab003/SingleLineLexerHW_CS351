import re

#keywords_expressions = [r"if", r"else", r"int", r"float"]
#operators_expressions = [r"\=", r"\+", r"\>", r"*"]
#separators_expressions = [r"\(", r"\)", r"\{", r"\}", r"\;", r"\,"]
#identifiers_expressions = [r"[a-zA-Z_][a-zA-Z0-9_]*"]

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
        ('string_literal', r'^"[^"]*"'),      # test first 
        ('float_literal', r'^\d+\.\d+'),      # test before int literals 
        ('keyword', r'^(if|else|int|float)\b'),  # \b ensures whole word match
        ('int_literal', r'^\d+'),              # test after floats
        ('identifier', r'^[a-zA-Z]+[a-zA-Z0-9]*'),  
        ('operator', r'^[=+>*]'),               
        ('separator', r'^[\(\):;"]'),            
    ]
    
    while line_to_cut:
        # Skips whitespace before next token
        if line_to_cut[0] == ' ':
            line_to_cut = line_to_cut[1:]
            continue
            
        matched = False
        
        for token_type, pattern in patterns:
            match = re.match(pattern, line_to_cut)
            if match:
                token_value = match.group(0)
                
                # Output <type, token> list
                if token_type == 'keyword':
                    tokens.append(f'<key,{token_value}>')
                elif token_type == 'identifier':
                    tokens.append(f'<id,{token_value}>')
                elif token_type == 'operator':
                    tokens.append(f'<op,{token_value}>')
                elif token_type == 'string_literal':
                    tokens.append(f'<string_literal,{token_value}>')
                elif token_type == 'float_literal':
                    tokens.append(f'<float_literal,{token_value}>')
                elif token_type == 'int_literal':
                    tokens.append(f'<int_literal,{token_value}>')
                else:  
                    tokens.append(f'<separator,{token_value}>')
                
                # Cuts first token from LOC
                line_to_cut = line_to_cut[len(token_value):]
                
                matched = True
                break
            
        if not matched:
            print(f" Skipping unexpected char: '{line_to_cut[0]}'")
            line_to_cut = line_to_cut[1:]
    
    # Prints output list
    print(f"Output <type, token> list: {tokens}")
    return tokens

def main():
    """int A1=5
float BBB2 =1034.2
float cresult = A1 +BBB2 * BBB2
if (cresult >10):
print("TinyPie " )
ifAA = 42
10.5
"Hello World"
x = 5 + 3 * 2
int    X   =   100"""
    
 # Gets docstring from main program
    program_lines = main.__doc__.strip().split('\n')
    
    # Processes each line
    for line in program_lines:
        if line.strip():
            print(f"Test input string: {line}")
            CutOneLineTokens(line)
            print()

# Runs main function
if __name__ == "__main__":
    main()