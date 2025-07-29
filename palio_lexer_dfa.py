# Define o conjunto de palavras-chave da linguagem Palio
KEYWORDS = {
    "pg-if", "pg-else", "pg-while", "pg-for",
    "pg-def", "pg-return", "pg-print",
    "pg-and", "pg-or", "pg-not",
    "pg-true", "pg-false"
}

# Define os delimitadores e operadores simples (de um caractere)
SINGLE_SYMBOLS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "%": "MOD",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ",": "COMMA",
    ":": "COLON"
}

# Funções auxiliares para verificar tipo de caractere
def is_letter(char):
    return char.isalpha() or char == "_"

def is_digit(char):
    return char.isdigit()

# Função principal que executa o analisador léxico
def tokenize(code):
    tokens = []
    index = 0
    line = 1

    while index < len(code):
        state = "q0"
        lexeme = ""
        start_line = line

        while index < len(code):
            char = code[index]

            if char == '\n':
                line += 1

            # Estado inicial: decide o tipo do token
            if state == "q0":
                if char.isspace():
                    index += 1
                    break
                elif is_letter(char):
                    lexeme += char
                    state = "q_id"
                    index += 1
                elif is_digit(char):
                    lexeme += char
                    state = "q_int"
                    index += 1
                elif char == '"':
                    lexeme += char
                    state = "q_string"
                    index += 1
                elif char == '=':
                    lexeme += char
                    state = "q_eq"
                    index += 1
                elif char in "<>!":
                    lexeme += char
                    state = "q_cmp"
                    index += 1
                elif char in SINGLE_SYMBOLS:
                    tokens.append((SINGLE_SYMBOLS[char], char))
                    index += 1
                    break
                elif char == "#":
                    state = "q_comment"
                    index += 1
                else:
                    print(f"[Erro léxico] Caractere inválido '{char}' na linha {line}")
                    index += 1
                    break

            # Estado para reconhecimento de identificadores/palavras-chave
            elif state == "q_id":
                if is_letter(char) or is_digit(char):
                    lexeme += char
                    index += 1
                else:
                    if lexeme in KEYWORDS:
                        tokens.append(("KEYWORD", lexeme))
                    else:
                        tokens.append(("ID", lexeme))
                    break

            # Estado para números inteiros
            elif state == "q_int":
                if is_digit(char):
                    lexeme += char
                    index += 1
                elif char == ".":
                    lexeme += char
                    state = "q_float"
                    index += 1
                else:
                    tokens.append(("INTEGER", lexeme))
                    break

            # Estado para números de ponto flutuante
            elif state == "q_float":
                if is_digit(char):
                    lexeme += char
                    index += 1
                else:
                    tokens.append(("FLOAT", lexeme))
                    break

            # Estado para reconhecimento de strings entre aspas
            elif state == "q_string":
                lexeme += char
                index += 1
                if char == '"':
                    tokens.append(("STRING", lexeme))
                    break
                elif char == '\n':
                    print(f"[Erro léxico] Quebra de linha em string na linha {start_line}")
                    break

            # Estado para verificação de "=" ou "=="
            elif state == "q_eq":
                if char == "=":
                    tokens.append(("EQ", "=="))
                    index += 1
                else:
                    tokens.append(("ASSIGN", "="))
                break

            # Estado para operadores relacionais compostos (!=, >=, <=)
            elif state == "q_cmp":
                if char == "=":
                    if lexeme == "!":
                        tokens.append(("NEQ", "!="))
                    elif lexeme == ">":
                        tokens.append(("GEQ", ">="))
                    elif lexeme == "<":
                        tokens.append(("LEQ", "<="))
                    index += 1
                else:
                    if lexeme == ">":
                        tokens.append(("GT", ">"))
                    elif lexeme == "<":
                        tokens.append(("LT", "<"))
                    elif lexeme == "!":
                        print(f"[Erro léxico] Operador inválido '!' na linha {line}")
                break

            # Estado de comentário: ignora até o fim da linha
            elif state == "q_comment":
                if char == '\n':
                    break
                index += 1

    return tokens

# Execução direta via terminal
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python palio_lexer_dfa.py arquivo.palio")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    tokens = tokenize(code)
    for token in tokens:
        print(token)
