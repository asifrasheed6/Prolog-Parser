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
thisChar = ''

# Tokens
UPPER_CHAR, LOWER_CHAR, DIGIT, UNKNOWN= 0,1,2,99
ADD_OP, SUB_OP, MULT_OP, DIV_OP = 21,22,23,24
BACK_SLASH, CIRCUMFLEX, TILDE, COLON, PERIOD, INVCOMMA, COMMA = 25,26,27,28,29,4,20
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
            
        OFile.write('Parsing: '+str(i)+'.txt')
            
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
    global NextToken
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
    global nextChar, charClass, number_of_lines
    nextChar = File.read(1)
    
    while re.match('\s',nextChar) and nextChar != ' ':
        if nextChar == '\n':
            number_of_lines+=1
        nextChar = File.read(1)
        
    if nextChar != EOF:
        if nextChar.isupper():
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
        thisChar = nextChar
        chclass = charClass
        add_char()
        get_char()
        while charClass in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
            add_char()
            get_char()
        NextToken = chclass
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
    
    OFile.write("Next token is "+str(NextToken)+", Next lexeme is "+str(Lexeme))

#---------Syntax analysis-----------
# <special> ->+|-|*|/|\|^|~|:|.|?| |#|$|&
def special():
    global error
    if NextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,BACK_SLASH,CIRCUMFLEX,TILDE,COLON,PERIOD,QUESTION,SPACE,HASHTAG,DOLLAR,AMPERSAND]:
        Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number)+". "+thisChar+" is not a special character")
        error+=1
        get_char()
        Lex()

# <alphanumeric> -><lowercase-char> | <uppercase-char> | <digit>
def alphanumeric():
    global error
    if NextToken in [UPPER_CHAR,LOWER_CHAR,DIGIT]:
        Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number)+". "+thisChar+" is not alphanumeric")
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
    else
        OFile.write("Syntax Error on Line "+str(number)+"."+thisChar+" is not a character")
        error+=1
        get_char()
        Lex()

# <strring> -> <character> | <character> <string>
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
        OFile.write("Syntax Error on Line "+str(number)+". Expected digit, got "+thisChar)
        error+=1
        get_char()
        Lex()

# <atom> -> <small-atom> | ' <string> '
def atom():
    global error
    if NextToken == LOWER_CHAR:
        return smallatom()
    elif NextToken == INVCOMMA:
        Lex()
        string()
        if NextToken != INVCOMMA:
            OFile.write("Syntax Error on Line "+str(number)+". Missing '")
            error+=1
            get_char()
            Lex()
            return False
    else:
        OFile.write("Syntax Error on Line "+str(number)+". Expected Small Atom or String, got "+thisChar)
        error+=1
        get_char()
        Lex()
        return False
        
# <predicate> -> <atom> | <atom> ( <term-list> )
def Predicate():
    global error
    atom()
    if NextToken == LEFT_PAREN:
        Lex()
        termlist()
        if NextToken == RIGHT_PAREN:
            Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number)+". Missing )")
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
            Predicate_List()
            if NextToken == PERIOD:
                Lex()
            else:
                OFile.write("Syntax Error on Line "+str(number)+". Missing .")
                error+=1
                get_char()
                Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number)+". Missing -")
            error+=1
            get_char()
            Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number)+". Missing ?")
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
            Predicate_List()
            if NextToken == PERIOD:
                Lex()
            else:
                OFile.write("Syntax Error on Line "+str(number)+". Missing .")
                error+=1
                get_char()
                Lex()
        else:
            OFile.write("Syntax Error on Line "+str(number)+". Missing -")
            error+=1
            get_char()
            Lex()
    else:
        OFile.write("Syntax Error on Line "+str(number)+". Expected . or :, got "+thisChar)
        error+=1
        get_char()
        Lex()
        
# <clause-list> -> <clause> | <clause> <clause-list>
def Clause_List():
    global error
    Clause()
    if NextToken == QUOTATION:
        Clause_List()

# <program> -> <clause-list> <query> | <query>
def Program():
    global error
    if NextToken == QUESTION:
        Query()
    elif NextToken == LOWER_CHAR:
        ClauseList()
        if NextToken == QUESTION:
            Query()
        else:
            print("Clause_List must come before Query", number_of_lines,token))
            get_char()
            Lex()

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

