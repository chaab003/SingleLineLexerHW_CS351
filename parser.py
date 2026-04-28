# Recursive descent parser for TinyPie
#
# BNF:
#   assign_exp     -> keyword identifier = math
#   math           -> multi + math | multi
#   multi          -> term * multi | term
#   term           -> identifier | int_literal | float_literal
#   if_exp         -> if ( comparison_exp ) :
#   comparison_exp -> identifier > identifier
#   print_exp      -> print ( string_literal )

output = []


def emit(line):
    print(line)
    output.append(line)


def parse_token(tok):
    inner = tok[1:-1]
    ttype, tval = inner.split(",", 1)
    return ttype.strip(), tval.strip()


def term(tokens, idx, depth):
    """term -> identifier | int_literal | float_literal"""
    indent = "  " * depth
    if idx >= len(tokens):
        return idx

    ttype, tval = parse_token(tokens[idx])
    if ttype in ("identifier", "int_literal", "float_literal"):
        emit(f"{indent}term -> {ttype}: {tval}")
        return idx + 1

    return idx


def multi(tokens, idx, depth):
    """multi -> term * multi | term"""
    indent = "  " * depth
    emit(f"{indent}multi ->")

    idx = term(tokens, idx, depth + 1)

    # check for *
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        if ttype == "operator" and tval == "*":
            emit(f"{indent}  *")
            idx = multi(tokens, idx + 1, depth + 1)

    return idx


def exp(tokens, idx, depth):
    """math -> multi + math | multi"""
    indent = "  " * depth
    emit(f"{indent}math ->")

    idx = multi(tokens, idx, depth + 1)

    # check for +
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        if ttype == "operator" and tval == "+":
            emit(f"{indent}  +")
            idx = exp(tokens, idx + 1, depth + 1)

    return idx


def assign_exp(tokens, depth):
    """assign_exp -> keyword identifier = math"""
    indent = "  " * depth
    emit(f"{indent}assign_exp -> keyword identifier = math")

    idx = 0

    # keyword
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        if ttype == "keyword":
            emit(f"{indent}  keyword: {tval}")
            idx += 1

    # identifier
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        if ttype == "identifier":
            emit(f"{indent}  identifier: {tval}")
            idx += 1

    # =
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        if ttype == "operator" and tval == "=":
            emit(f"{indent}  =")
            idx += 1

    # math part
    idx = exp(tokens, idx, depth + 1)
    return idx


def comparison_exp(tokens, idx, depth):
    indent = "  " * depth
    emit(f"{indent}comparison_exp -> identifier > identifier")

    # left side
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        emit(f"{indent}  identifier: {tval}")
        idx += 1

    # >
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        emit(f"{indent}  {tval}")
        idx += 1

    # right side
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        emit(f"{indent}  identifier: {tval}")
        idx += 1

    return idx


def if_exp(tokens, depth):
    indent = "  " * depth
    emit(f"{indent}if_exp -> if ( comparison_exp ) :")

    idx = 0

    # if
    if idx < len(tokens):
        emit(f"{indent}  if")
        idx += 1

    # (
    if idx < len(tokens):
        emit(f"{indent}  (")
        idx += 1

    idx = comparison_exp(tokens, idx, depth + 1)

    # )
    if idx < len(tokens):
        emit(f"{indent}  )")
        idx += 1

    # :
    if idx < len(tokens):
        emit(f"{indent}  :")
        idx += 1

    return idx


def print_exp(tokens, depth):
    """print_exp -> print ( string_literal )"""
    indent = "  " * depth
    emit(f"{indent}print_exp -> print ( string_literal )")

    idx = 0

    # print
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        emit(f"{indent}  print")
        idx += 1

    # (
    if idx < len(tokens):
        emit(f"{indent}  (")
        idx += 1

    # string literal
    if idx < len(tokens):
        ttype, tval = parse_token(tokens[idx])
        if ttype == "string_literal":
            emit(f"{indent}  string_literal: {tval}")
            idx += 1

    # )
    if idx < len(tokens) and parse_token(tokens[idx])[1] == ")":
        emit(f"{indent}  )")
        idx += 1

    return idx


def parser(tokens, line_num):
    output.clear()

    if not tokens:
        return ""

    first_type, first_val = parse_token(tokens[0])

    if first_type == "keyword" and first_val in ("float", "int"):
        assign_exp(tokens, 0)
    elif first_type == "keyword" and first_val == "if":
        if_exp(tokens, 0)
    elif first_type == "identifier" and first_val == "print":
        print_exp(tokens, 0)
    else:
        exp(tokens, 0, 0)

    return "\n".join(output)
