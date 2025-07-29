# Compiladores-T1
# Analisador Léxico da Linguagem Palio<img width="1" height="1" alt="image" src="https://github.com/user-attachments/assets/6175cdaa-ef70-456d-a86c-31e74032220e" />



O objetivo principal deste trabalho foi desenvolver um analisador léxico funcional, responsável por identificar os componentes básicos (tokens) da linguagem de programação fictícia Palio. Esse trabalho faz parte da disciplina de Compiladores e visa colocar em prática os conhecimentos teóricos sobre Autômatos Finitos Determinísticos (DFA) e análise léxica, que é a primeira etapa do processo de compilação.
A linguagem Palio foi projetada com base na sintaxe do Python, mas com um diferencial: todas as palavras-chave são prefixadas com pg- (ex: pg-if, pg-print, pg-def). O restante da estrutura (identificadores, operadores, delimitadores, literais) segue padrões semelhantes aos das linguagens de alto nível.

## ✨ Características Principais

- **Implementação**: Construído em Python, sem bibliotecas externas de regex, para simular o comportamento real de um compilador.
- **Análise por DFA**: Utiliza um Autômato Finito Determinístico para identificar e validar tokens.
- **Sintaxe Inspirada**: A linguagem Palio tem uma base familiar, inspirada em Python, com um toque diferente no uso de palavras-chave.
- **Detecção de Erros**: Identifica e reporta caracteres inválidos no código-fonte, indicando a linha do erro.

## 🧠 A Origem do Nome: Palio

O nome **Palio** é uma união dos nomes dos times Palmeiras e Grêmio. Combinando **Pal**meiras (time da Tuliana) e Grêm**io** (time da Julia), nasceu o nome da nossa linguagem. Este nome é muito utilizado na internet para quando esses times ajudam um ao outro derrotando seus respectivos rivais em jogos e etc. Os prefixos que decidimos utilizar também se refere aos times, PG (Palmeiras e Grêmio)⚽

## 🗂️ Estrutura da Linguagem

Decidimos utilizar uma sintaxe inspirada em Python. Sua principal característica é que todas as **palavras-chave** são prefixadas com `pg-`.

### Tokens Reconhecidos

| Categoria | Descrição | Exemplos |
| :--- | :--- | :--- |
| **Palavras-chave** | Comandos e estruturas de controle | `pg-if`, `pg-def`, `pg-while`, `pg-for`, `pg-true`, `pg-false` |
| **Identificadores** | Nomes de variáveis e funções | `minha_variavel`, `soma2`, `_temp` |
| **Números** | Literais numéricos inteiros e de ponto flutuante | `10`, `3.14`, `100` |
| **Strings** | Sequências de caracteres entre aspas duplas | `"Olá, Mundo!"`, `"Palio"` |
| **Operadores**| Aritméticos, de atribuição e lógicos | `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `>` |
| **Delimitadores** | Símbolos de agrupamento e separação | `(`, `)`, `{`, `}`, `[`, `]`, `:`, `,` |
| **Comentários** | Linhas iniciadas com `#` (ignoradas pelo analisador) | `# Este é um comentário` |

## ⚙️ Como Executar

**Pré-requisitos:**
- Python 3

**Passos:**

1. Clone o repositório ou salve o código-fonte como `palio_lexer_dfa.py`.
2. Crie um arquivo de teste com a extensão `.palio` (ex: `codigo.palio`).
3. Execute o analisador via terminal, passando o nome do arquivo como argumento:

   ```shell
   python palio_lexer_dfa.py seu_arquivo.palio
Exemplo de Saída
Para um código-fonte válido, a saída será uma lista de tuplas (TIPO_DO_TOKEN, VALOR):

('KEYWORD', 'pg-def')
('ID', 'saudacao')
('LPAREN', '(')
('ID', 'nome')
('RPAREN', ')')
('COLON', ':')
...
🧪 Testes e Validação
O projeto inclui arquivos de exemplo para demonstrar o funcionamento:

Acerto.palio: Contém um código sintaticamente correto que será tokenizado com sucesso.


# Exemplo de função e condicional
pg-def saudacao(nome):
    pg-print("Olá, " + nome)

pg-if pg-true:
    saudacao("Julia")
erro.palio: Contém um caractere inválido (@) para testar a detecção de erros léxicos.

@variavel = 42
Saída esperada para erro.palio:

[Erro léxico] Caractere inválido '@' na linha 1
📚 Sobre a Implementação
O núcleo do analisador é um Autômato Finito Determinístico (DFA) simulado manualmente. O código percorre o arquivo de entrada caractere por caractere, realizando transições entre estados para classificar cada sequência em um token específico.

Os principais estados da máquina incluem:

q0: Estado inicial

q_id: Formação de identificadores e palavras-chave

q_int / q_float: Formação de números inteiros e reais

q_string: Formação de literais string

q_eq / q_cmp: Tratamento de operadores de comparação e atribuição

q_comment: Ignora linhas de comentário


👩‍💻 Autoras
Julia Gomes (Gremista)

Tuliana Andrade (Palmeirense)
