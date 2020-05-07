import re


global lex_index, token, nextChar, Lexeme, NextToken, File, error, charClass
File = None
lex_index = -1
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
    for i in range(1, 25):
        File = open(str(i)+'1.txt', 'r')
        get_char()

        while(NextToken != EOF):
            Lex()

        #print error
        #reset the variables

# Lookup() - function to lookup operators and return the token
def lookup(char):

    global next_token
    if char == "(":
        add_char()
        next_token = LEFT_PAREN
    elif char == ")":
        return (')', 'Right_Paren')
    elif char == "+":
        return ('+', 'special')
    elif char == "-":
        return ('-', 'special')
    elif char == "*":
        return ('*', 'special')
    elif char == "/":
        return ('/', 'special')
    elif char == "\\":
        return ('\\', 'special')
    elif char == "^":
        return ('^', 'special')
    elif char == "~":
        return ('~', 'special')
    elif char == ":":
        return (':', 'special')
    elif char == ".":
        return ('.', 'special')
    elif char == "?":
        return ('?', 'special')
    elif char == " ":
        return (' ', 'special')
    elif char == "#":
        return ('#', 'special')
    elif char == "$":
        return ('$', 'special')
    elif char == "&":
        return ('&', 'special')

#add next char to lexeme
def add_char():
    Lexeme.append(nextChar)

#to get the next character of input and determine its character and class
def get_char():
    global nextChar, charClass
    nextChar = File.read(1)
    if nextChar != EOF:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF



# Lex() - lexical analyzer
#numeral, atom, variable
def Lex():
    NextToken = (lex, token)
   while char.isdigit():
       lex+=char
       token = 'numeral'
       NextToken = (lex, token)
       char = next(Next)
       break

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

