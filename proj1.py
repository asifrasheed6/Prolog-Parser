import re

#global
global lex_index, token, Lexeme, NextToken, File, error, charClass
File = None
number_of_lines = -1
token = -1
Lexeme = []
error = []
nextChar = ''

#character classes
UPPER_CHAR, LOWER_CHAR, DIGIT, SPECIAL, UNKNOWN= 0,1,2,3,99

#token codes
ADD_OP, SUB_OP, MULT_OP, DIV_OP = 21,22,23,24
BACK_SLASH, CIRCUMFLEX, TILDE, COLON, PERIOD =25,26,27,28,29
QUESTION, SPACE, HASHTAG, DOLLAR, AMPERSAND = 30,31,32,33,34,35
LEFT_PAREN, RIGHT_PAREN = 36, 37
EOF = -1



#main driver
def main():
    global File
    i = 0
    while True:
        i+=1
        try:
            File = open(str(i)+'1.txt', 'r')
            get_char()

            while(NextToken != EOF):
                Lex()

            #print error
            #reset the variables
        except FileNotFoundError:
            print('File does not exist')

# Lookup() - function to lookup operators and return the token
def lookup(char):

    global next_token, number_of_lines
    if char == "(":
        add_char()
        next_token = LEFT_PAREN
    elif char == ")":
        add_char()
        next_token = RIGHT_PAREN
    elif char == "+":
        add_char()
        next_token = ADD_OP
    elif char == "-":
        add_char()
        next_token = SUB_OP
    elif char == "*":
        add_char()
        next_token = MULT_OP
    elif char == "/":
        add_char()
        next_token = DIV_OP
    elif char == "\\":
        add_char()
        next_token = BACK_SLASH
    elif char == "^":
        add_char()
        next_token = CIRCUMFLEX
    elif char == "~":
        add_char()
        next_token = TILDE
    elif char == ":":
        add_char()
        next_token = COLON
    elif char == ".":
        add_char()
        next_token = PERIOD
    elif char == "?":
        add_char()
        next_token = QUESTION
    elif char == " ":
        add_char()
        next_token = SPACE
    elif char == "#":
        add_char()
        next_token = HASHTAG
    elif char == "$":
        add_char()
        next_token = DOLLAR
    elif char == "&":
        add_char()
        next_token = AMPERSAND
    elif char == "\n":
        number_of_lines+=1
    else:
        add_char()
        next_token = EOF

    return next_token

#add next char to lexeme
def add_char():
    Lexeme.append(nextChar)

#to get the next character of input and determine its character and class
def get_char():
    global nextChar, charClass
    nextChar = ''.join(File.read(1))
    if nextChar != EOF:
        if char.isupper():
            charClass = UPPER_CHAR
        elif nextChar.islower():
            charClass = LOWER_CHAR
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF

def getNonBlank():
    while nextChar.isspace():
        get_char()

# Lex() - lexical analyzer
#numeral, atom, variable
def Lex():
    global NextToken
    getNonBlank()
    if charClass == DIGIT:
        add_char()
        get_char()
        while charClass == DIGIT:
            add_char()
            get_char()
        NextToken = DIGIT
    elif charClass == UNKNOWN:
        lookup(nextChar)
        get_char()
    elif charClass == EOF:
        NextToken = EOF
        Lexeme.append('EOF')

    print("Next token is %d, Next lexeme is %s\n", NextToken, Lexeme)
    return NextToken





    if char.islower():
        lex+=char
        token = ''



#---------Syntax analysis-----------

# <program> -> <clause-list> <query> | <query>

# <clause-list> -> <clause> | <clause> <clause-list>

# <clause> -> <predicate> . | <predicate> :- <predicate-list> .

# <query> -> ?- <predicate-list> .

# <predicate-list> -> <predicate> | <predicate> , <predicate-list>

# <predicate> -> <atom> | <atom> ( <term-list> )

# <term-list> -> <term> | <term> , <term-list>

# <term> -> <atom> | <variable> | <structure> | <numeral>

# <structure> -> <atom> ( <term-list> )

# <atom> -> <small-atom> | ' <string> '

# <small-atom> -> <lowercase-char> | <lowercase-char> <character-list>

# <variable> -> <uppercase-char> | <uppercase-char> <character-list>

# <character-list> -> <alphanumeric> | <alphanumeric> <character-list>

# <alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>

# <numeral> -> <digit> | <digit> <numeral>

# <string> -> <character> | <character> <string>

# <character> -> <alphanumeric> | <special>

