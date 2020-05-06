print("Python Parser Project")
global Next, lex, token, char, Lexeme, NextToken
# file open
# out = open('parser_output.txt', 'w')

# for i in range(1, 25):
#                 str(i)+ '.txt'
file = open('1.txt', 'r')
text = file.read()





lex = ''
token = ''
NextToken = (lex, token)

Lexeme = []
for i in text:
   Lexeme+=i

#not sure took from yusuf
def nextChar():
   for i in Lexeme:
      yield i

Next = nextChar()
char = next(Next)



# Lex() - lexical analyzer
def Lex():
   lex = ''
   token = ''
   NextToken = (lex, token)
   while char.isdigit()


# getChar()
def getChar():

# Lookup() - function to lookup operators and return the token
def lookpu(char):
    if char == "(":
        return ('(', 'Left_Paren')
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
# error()
# statement()

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

# <lowercase-char> -> a | b | c | ... | x | y | z

# <uppercase-char> -> A | B | C | ... | X | Y | Z | _

# <numeral> -> <digit> | <digit> <numeral>

# <digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

# <string> -> <character> | <character> <string>

# <character> -> <alphanumeric> | <special>

# <special> -> + | - | * | / | \ | ^ | ~ | : | . | ? | | # | $ | &
