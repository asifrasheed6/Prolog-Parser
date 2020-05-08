import re

#global
global lex_index, token, nextChar, Lexeme, NextToken, File, error, charClass
File = None
OFile = None
number_of_lines = 1
token = -1
Lexeme = []
error = 0
nextChar = ''
thisChar = ''
NextToken = -1
count = 0

# Tokens
UPPER_CHAR, LOWER_CHAR, DIGIT, UNKNOWN= 0,1,2,99
ADD_OP, SUB_OP, MULT_OP, DIV_OP = 21,22,23,24
BACK_SLASH, CIRCUMFLEX, TILDE, COLON, PERIOD, INVCOMMA, COMMA = 25,26,27,28,29,4,20
QUESTION, SPACE, HASHTAG, DOLLAR, AMPERSAND = 30,31,32,33,34
LEFT_PAREN, RIGHT_PAREN = 36, 37
EOF = -1



#main driver
def main():
    global File, OFile, error, NextToken
    OFile = open('parser_output.txt','w')
    i = 1
    while True:
        try:
            File = open(str(i)+'.txt', 'r')
        except IOError:
            return 0
            
        OFile.write('Parsing: '+str(i)+'.txt\n')
            
        get_char()
        Lex()
        while NextToken != EOF:
            Program()
            Lex()
            
        if error == 0:
            OFile.write('Syntactically Correct\n\n')
        else:
            OFile.write('\n')
            error = 0
        number_of_lines = 0
            
        i+=1

# Lookup() - function to lookup operators and return the token
def lookup(char):
    global NextToken,count
    if char == "\n":
        number_of_lines+=1
    elif char == ",":
        add_char()
        NextToken = COMMA
    elif char == "'":
        add_char()
        NextToken = INVCOMMA
    elif char == "(":
        add_char()
        NextToken = LEFT_PAREN
    elif char == ")":
        add_char()
        NextToken = RIGHT_PAREN
    elif char == "+":
        add_char()
        NextToken = ADD_OP
    elif char == "-":
        add_char()
        NextToken = SUB_OP
    elif char == "*":
        add_char()
        NextToken = MULT_OP
    elif char == "/":
        add_char()
        NextToken = DIV_OP
    elif char == "\\":
        add_char()
        NextToken = BACK_SLASH
    elif char == "^":
        add_char()
        NextToken = CIRCUMFLEX
    elif char == "~":
        add_char()
        NextToken = TILDE
    elif char == ":":
        add_char()
        NextToken = COLON
    elif char == ".":
        add_char()
        NextToken = PERIOD
    elif char == "?":
        add_char()
        NextToken = QUESTION
    elif char == " ":
        add_char()
        NextToken = SPACE
    elif char == "#":
        add_char()
        NextToken = HASHTAG
    elif char == "$":
        add_char()
        NextToken = DOLLAR
    elif char == "&":
        add_char()
        NextToken = AMPERSAND
    else:
        add_char()
        NextToken = EOF

#add next char to lexeme
def add_char():
    Lexeme.append(nextChar)

#to get the next character of input and determine its character and class
def get_char():
    global nextChar, charClass, number_of_lines,count
    count += 1
    nextChar = File.read(1)
    
    while re.match('\s',nextChar):
        if nextChar == '\n':
            number_of_lines+=1
            count=0
        nextChar = File.read(1)
        
    if nextChar != EOF and nextChar != '\n':
        if nextChar.isupper():
            charClass = UPPER_CHAR
        elif nextChar.islower():
            charClass = LOWER_CHAR
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    elif nextChar == '\n':
        charClass = UNKNOWN
    else:
        charClass = EOF
        
# Lex() - lexical analyzer
#numeral, atom, variable
def Lex():
    global NextToken, Lexeme
    if charClass == LOWER_CHAR:
        thisChar = nextChar
        add_char()
        get_char()
        while charClass in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
            add_char()
            get_char()
        NextToken = LOWER_CHAR
    elif charClass == UPPER_CHAR:
        thisChar = nextChar
        add_char()
        get_char()
        while charClass in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
            add_char()
            get_char()
        NextToken = UPPER_CHAR
    elif charClass == DIGIT:
        thisChar = nextChar
        add_char()
        get_char()
        while charClass == DIGIT:
            add_char()
            get_char()
        NextToken = DIGIT
    elif charClass == UNKNOWN:
        thisChar = nextChar
        lookup(nextChar)
        get_char()
    elif charClass == EOF:
        NextToken = EOF
        Lexeme.append('EOF')
    
#---------Syntax analysis-----------
# <special> ->+|-|*|/|\|^|~|:|.|?| |#|$|&
def special():
    global error
    if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND]:
        Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". "+thisChar+" is not a special character\n")
        error+=1
        get_char()
        Lex()

# <alphanumeric> -><lowercase-char> | <uppercase-char> | <digit>
def alphanumeric():
    global error
    if NextToken in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
        Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". "+thisChar+" is not alphanumeric\n")
        error+=1
        get_char()
        Lex()
        
# <character> -> <alphanumeric> | <special>
def character():
    global error
    if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND]:
        special()
    elif NextToken in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
        alphanumeric()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+"."+thisChar+" is not a character\n")
        error+=1
        get_char()
        Lex()

# <string> -> <character> | <character> <string>
def string():
    global error
    character()
    if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND,UPPER_CHAR,LOWER_CHAR,DIGIT]:
        string()
            
# <numeral> -> <digit> | <digit> <numeral>
def numeral():
    global error
    if NextToken == DIGIT:
        Lex()
        if NextToken == DIGIT:
            numeral()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Expected digit, got "+thisChar+"\n")
        error+=1
        get_char()
        Lex()

# <character-list> -> <alphanumeric> | <alphanumeric> <character-list>
def character_list():
    alphanumeric()
    if NextToken in [UPPER_CHAR, LOWER_CHAR, DIGIT]:
        Lex()
        character_list()

# <variable> -> <uppercase-char> | <uppercase-char> <character-list>
def variable():
    global num_of_errors, list_of_errors, next_token
    if NextToken == UPPER_CHAR:
        Lex()
        if NextToken in [UPPER_CHAR, LOWER_CHAR, DIGIT]:
            character_list()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Expected variable, got "+thisChar+"\n")
        error+=1
        get_char()
        Lex()

# <small-atom> -> <lowercase-char> | <lowercase-char> <character-list>
def smallatom():
    global error
    if NextToken == LOWER_CHAR:
        Lex()
        if NextToken == LOWER_CHAR:
            character_list()
    else:
        OFile.write("Syntax Error on Line " + str(number_of_lines) + ". Expected lowercase, got " + thisChar+"\n")
        error += 1
        get_char()
        Lex()

# <atom> -> <small-atom> | ' <string> '
def atom():
    global error
    if NextToken == LOWER_CHAR:
        smallatom()
    elif NextToken == INVCOMMA:
        Lex()
        string()
        if NextToken != INVCOMMA:
            OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing '\n")
            error+=1
            get_char()
            Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Expected Small Atom or String, got "+thisChar+"\n")
        error+=1
        get_char()
        Lex()

# <term> -> <atom> | <variable> | <structure> | <numeral>
def Term():
    global error
    if NextToken == DIGIT:
        numeral()
    elif NextToken == UPPER_CHAR:
        variable()
    elif NextToken in [LOWER_CHAR, INVCOMMA]:
        Predicate()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Illegal Term\n")
        error+=1
        get_char()
        Lex()

# <term-list> -> <term> | <term> , <term-list>
def TermList():
    Term()
    if NextToken == COMMA:
        Lex()
        TermList()

# <structure> -> <atom> ( <term-list> )
def structure():
    global error
    atom()
    if NextToken == LEFT_PAREN:
        Lex()
        TermList()
        if NextToken == RIGHT_PAREN:
            Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing )\n")
            error+=1
            get_char()
            Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing (\n")
        error+=1
        get_char()
        Lex()
        
# <predicate> -> <atom> | <atom> ( <term-list> )
def Predicate():
    global error
    atom()
    if NextToken == LEFT_PAREN:
        Lex()
        TermList()
        if NextToken == RIGHT_PAREN:
            Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing )\n")
            error+=1
            get_char()
            Lex()

# <predicate-list> -> <predicate> | <predicate> , <predicate-list>
def PredicateList():
    Predicate()
    if NextToken == COMMA:
        Lex()
        PredicateList()

# <query> -> ?- <predicate-list> .
def Query():
    global error
    if NextToken == QUESTION:
        Lex()
        if NextToken == SUB_OP:
            Lex()
            PredicateList()
            if NextToken == PERIOD:
                Lex()
            else:
                OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing .\n")
                error+=1
                get_char()
                Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing -\n")
            error+=1
            get_char()
            Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing ?\n")
        error+=1
        get_char()
        Lex()

# <clause> -> <predicate> . | <predicate> :- <predicate-list> .
def Clause():
    global error
    Predicate()

    if NextToken == PERIOD:
        Lex()
    elif NextToken == COLON:
        Lex()
        if NextToken == SUB_OP:
            Lex()
            PredicateList()
            if NextToken == PERIOD:
                Lex()
            else:
                OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing .\n")
                error+=1
                get_char()
                Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number_of_lines)+". Missing -\n")
            error+=1
            get_char()
            Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number_of_lines)+". Expected . or :, got "+thisChar+"\n")
        error+=1
        get_char()
        Lex()
        
# <clause-list> -> <clause> | <clause> <clause-list>
def Clause_List():
    global error
    Clause()
    if NextToken == INVCOMMA:
        Clause_List()

# <program> -> <clause-list> <query> | <query>
def Program():
    global error
    if NextToken == QUESTION:
        Query()
    elif NextToken == LOWER_CHAR:
        Clause_List()
        if NextToken == QUESTION:
            Query()

main()
