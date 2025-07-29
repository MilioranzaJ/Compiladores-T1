# --- DEFINIÇÕES GLOBAIS ---
# Definem os componentes básicos da linguagem "PALIO".

# KEYWORDS armazena todas as palavras reservadas da linguagem.
# Usar um conjunto é muito eficiente para verificar se uma palavra é uma palavra-chave (operação O(1) em média).
KEYWORDS = {
    "pg-if", "pg-else", "pg-while", "pg-for",
    "pg-def", "pg-return", "pg-print",
    "pg-and", "pg-or", "pg-not",
    "pg-true", "pg-false"
}

# SINGLE_SYMBOLS mapeia símbolos de um único caractere
# para o nome do seu token correspondente. Isso facilita o reconhecimento de operadores
# e delimitadores simples.
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

# --- FUNÇÕES AUXILIARES ---
# Funções simples para verificar o tipo de um caractere.

def is_letter(char):
    """Verifica se um caractere é uma letra (a-z, A-Z) ou um subtraço ('_')."""
    return char.isalpha() or char == "_"

def is_digit(char):
    """Verifica se um caractere é um dígito numérico (0-9)."""
    return char.isdigit()

# --- ANALISADOR LÉXICO (TOKENIZER) ---
# Converte o código-fonte em uma lista de tokens.
# Funciona como um Autômato Finito Determinístico simulado.
def tokenize(code):
    """
    Processa uma string de código-fonte e a divide em uma lista de tokens.
    Cada token é uma tupla no formato (TIPO_DO_TOKEN, 'lexema').
    """
    tokens = []  # Lista para armazenar os tokens encontrados.
    index = 0    # Ponteiro para a posição atual no código-fonte.
    line = 1     # Contador de linha para relatar erros.

    # Loop principal que percorre todo o código-fonte.
    while index < len(code):
        # --- INÍCIO DE UM NOVO TOKEN ---
        # A cada iteração deste loop, tenta reconhecer um novo token.
        state = "q0"      # O autômato sempre começa no estado inicial 'q0'.
        lexeme = ""       # String para construir o lexema.
        start_line = line # Guarda a linha onde o token começa, para erros de string.

        # Loop interno que implementa a máquina de estados para reconhecer um único token.
        while index < len(code):
            char = code[index] # Pega o caractere atual.

            # Adiciona o contador de linha sempre que uma nova linha é encontrada.
            if char == '\n':
                line += 1

            # --- ESTADO q0: O ESTADO INICIAL ---
            # Decide para qual estado ir com base no caractere atual.
            if state == "q0":
                if char.isspace():
                    # Ignora espaços em branco, tabulações e quebras de linha.
                    index += 1
                    break # Sai do loop interno para começar a busca por um novo token.
                elif is_letter(char):
                    # Se for uma letra, começa a reconhecer um identificador ou palavra-chave.
                    lexeme += char
                    state = "q_id"
                    index += 1
                elif is_digit(char):
                    # Se for um dígito, começa a reconhecer um número.
                    lexeme += char
                    state = "q_int"
                    index += 1
                elif char == '"':
                    # Se for aspas duplas, começa a reconhecer uma string.
                    lexeme += char
                    state = "q_string"
                    index += 1
                elif char == '=':
                    # Se for '=', pode ser atribuição ('=') ou igualdade ('==').
                    lexeme += char
                    state = "q_eq"
                    index += 1
                elif char in "<>!":
                    # Se for um desses, pode ser um operador de comparação.
                    lexeme += char
                    state = "q_cmp"
                    index += 1
                elif char in SINGLE_SYMBOLS:
                    # Se for um símbolo simples, cria o token imediatamente.
                    tokens.append((SINGLE_SYMBOLS[char], char))
                    index += 1
                    break # Token reconhecido, sai para procurar o próximo.
                elif char == "#":
                    # Se for '#', inicia o tratamento de um comentário.
                    state = "q_comment"
                    index += 1
                else:
                    # Se o caractere não for reconhecido, é um erro léxico.
                    print(f"[Erro léxico] Caractere inválido '{char}' na linha {line}")
                    index += 1
                    break

            # --- ESTADO q_id: RECONHECIMENTO DE IDENTIFICADORES E PALAVRAS-CHAVE ---
            elif state == "q_id":
                if is_letter(char) or is_digit(char):
                    # Continua guardando caracteres enquanto forem letras ou dígitos.
                    lexeme += char
                    index += 1
                else:
                    # Se o caractere não pertence a um ID, o token terminou.
                    # Verifica se o lexema é uma palavra-chave.
                    if lexeme in KEYWORDS:
                        tokens.append(("KEYWORD", lexeme))
                    else:
                        tokens.append(("ID", lexeme))
                    break # Token reconhecido, sai para procurar o próximo.

            # --- ESTADO q_int: RECONHECIMENTO DE NÚMEROS INTEIROS ---
            elif state == "q_int":
                if is_digit(char):
                    # Continua guardando dígitos.
                    lexeme += char
                    index += 1
                elif char == ".":
                    # Se encontrar um ponto, muda para o estado de número flutuante.
                    lexeme += char
                    state = "q_float"
                    index += 1
                else:
                    # Se não, o número inteiro terminou.
                    tokens.append(("INTEGER", lexeme))
                    break

            # --- ESTADO q_float: RECONHECIMENTO DE NÚMEROS DE PONTO FLUTUANTE ---
            elif state == "q_float":
                if is_digit(char):
                    # Continua guardando dígitos após o ponto.
                    lexeme += char
                    index += 1
                else:
                    # O número de ponto flutuante terminou.
                    tokens.append(("FLOAT", lexeme))
                    break

            # --- ESTADO q_string: RECONHECIMENTO DE STRINGS ---
            elif state == "q_string":
                lexeme += char
                index += 1
                if char == '"':
                    # Se encontrar as aspas de fechamento, a string terminou.
                    tokens.append(("STRING", lexeme))
                    break
                elif char == '\n':
                    # Strings não podem conter quebras de linha nesta linguagem.
                    print(f"[Erro léxico] Quebra de linha em string na linha {start_line}")
                    break

            # --- ESTADO q_eq: TRATA '=' E '==' ---
            elif state == "q_eq":
                if char == "=":
                    # Se o próximo caractere também for '=', é o operador de igualdade.
                    tokens.append(("EQ", "=="))
                    index += 1
                else:
                    # Senão, é o operador de atribuição.
                    tokens.append(("ASSIGN", "="))
                break

            # --- ESTADO q_cmp: TRATA '>', '>=', '<', '<=', '!=' ---
            elif state == "q_cmp":
                if char == "=":
                    # Verifica se forma um operador de dois caracteres (>=, <=, !=).
                    if lexeme == "!":
                        tokens.append(("NEQ", "!="))
                    elif lexeme == ">":
                        tokens.append(("GEQ", ">="))
                    elif lexeme == "<":
                        tokens.append(("LEQ", "<="))
                    index += 1
                else:
                    # Senão, é um operador de um caractere.
                    if lexeme == ">":
                        tokens.append(("GT", ">"))
                    elif lexeme == "<":
                        tokens.append(("LT", "<"))
                    elif lexeme == "!":
                        # '!' sozinho não é um operador válido na linguagem PALIO.
                        print(f"[Erro léxico] Operador inválido '!' na linha {line}")
                break

            # --- ESTADO q_comment: IGNORA COMENTÁRIOS ---
            elif state == "q_comment":
                if char == '\n':
                    # O comentário termina na quebra de linha.
                    break
                # Ignora todos os outros caracteres dentro do comentário.
                index += 1

    return tokens

# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
# Este trecho roda quando o script é executado diretamente.

if __name__ == "__main__":
    import sys # Módulo para acessar argumentos da linha de comando.

    # Verifica se o nome do arquivo foi fornecido como argumento.
    if len(sys.argv) != 2:
        print("Uso: python palio_lexer_dfa.py arquivo.palio")
        sys.exit(1) # Encerra o programa se o uso estiver incorreto.

    # Abre e lê o arquivo de código-fonte.
    # e garante que o arquivo será fechado corretamente.
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    # Chama a função tokenize para obter a lista de tokens.
    tokens = tokenize(code)

    # Imprime cada token encontrado.
    for token in tokens:
        print(token)
