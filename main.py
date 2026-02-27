from lexer import CutOneLineTokens


def main():
    program_string = """int A1=5
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
    program_lines = program_string.strip().split("\n")

    # Processes each line
    for line in program_lines:
        if line.strip():
            print(f"Test input string: {line}")
            CutOneLineTokens(line)
            print()


# Runs main function
if __name__ == "__main__":
    main()
