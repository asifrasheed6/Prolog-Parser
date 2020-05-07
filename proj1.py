import re

#global
global lex_index, token, nextChar, Lexeme, NextToken, File, error, charClass
File = None
OFile = None
number_of_lines = 0
token = -1
Lexeme = []
error = 0
nextChar = ''


UPPER_CHAR, LOWER_CHAR, DIGIT, UNKNOWN= 0,1,2,99
ADD_OP, SUB_OP, MULT_OP, DIV_OP = 21,22,23,24
BACK_SLASH, CIRCUMFLEX, TILDE, COLON, PERIOD =25,26,27,28,29
QUESTION, SPACE, HASHTAG, DOLLAR, AMPERSAND = 30,31,32,33,34,35
LEFT_PAREN, RIGHT_PAREN = 36, 37
EOF = -1



#main driver
def main():
    global File, OFile, error
    OFile = open('parser_output.txt','w')
    i = 1
    while True:
        try:
            File = open(str(i)+'.txt', 'r')
        except IOError:
            return 0
            
        OFile.write('Parsing: '+str(i)'.txt')
            
        get_char()

        while NextToken != EOF:
            Lex()
            
        if error == 0:
            OFile.write('Syntactically Correct\n')
        else:
            OFile.write('\n')
            error = 0
            
        i+=1

# Lookup() - function to lookup operators and return the token
def lookup(char):

    global next_token
    if char == "\n":
        number_of_lines+=1
    elif char == "(":
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
    else:
        add_char()
        next_token = EOF

    return next_token

#add next char to lexeme
def add_char():
    Lexeme.append(nextChar)

#to get the next character of input and determine its character and class
def get_char():
    global nextChar, charClass, number_of_lines
    nextChar = File.read(1)
    
    while re.match('\s',nextChar) and nextChar != ' ':
        if nextChar == '\n':
            number_of_lines+=1
        nextChar = File.read(1)
        
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

# Lex() - lexical analyzer
#numeral, atom, variable
def Lex():
    global NextToken, Lexeme
    if charClass in [UPPER_CHAR,LOWER_CHAR]:
        chclass = charClass
        add_char()
        get_char()
        while charClass in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
            add_char()
            get_char()
        NextToken = chclass
    elif charClass == DIGIT:
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
    
    OFile.write("Next token is "+str(NextToken)+", Next lexeme is "+str(Lexeme))

# <special> ->+|-|*|/|\|^|~|:|.|?| |#|$|&
def special():
    global error
    if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND]:
        Lex()
        return True
    else:
        OFile.write("Syntax Error on Line "+str(number)+". "+str(nextChar)+" is not a special character")
        error+=1
        get_char()
        Lex()
        return False

# <alphanumeric> -><lowercase-char> | <uppercase-char> | <digit>
def alphanumeric():
    global error
    if NextToken in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
        Lex()
        return True
    else:
        OFile.write("Syntax Error on Line "+str(number)+". "+str(nextChar)+" is not alphanumeric")
        error+=1
        get_char()
        Lex()
        return False
        
# <character> -> <alphanumeric> | <special>
def character():
    global error
    if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND]:
        return special()
    elif NextToken in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
        return alphanumeric()
    else
        OFile.write("Syntax Error on Line "+str(number)+"."+str(nextChar)+" is not a character")
        error+=1
        get_char()
        Lex()
        return False

# <strring> -> <character> | <character> <string>
def string():
    global error
    if character():
        if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND,UPPER_CHAR,LOWER_CHAR,DIGIT]:
            string()
            
# <numeral> -> <digit> | <digit> <numeral>
def numeral():
    global error
    if NextToken is DIGIT:
        Lex()
        if NextToken is DIGIT:
            numeral()
        return True
    else:
        OFile.write("Syntax Error on Line "+str(number)+"."+str(nextChar)+" is not a numeral")
        error+=1
        get_char()
        Lex()
        return False
    

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

