def readNumber(line, index):
    # string to number
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            # pointerをひとつ進めて返す
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def readMulti(line, index):
    token = {'type': 'MULTI'}
    return token, index + 1


def readDiv(line, index):
    token = {'type': 'DIV'}
    return token, index + 1


def readRBracket(line, index):
    token = {'type': 'R_BRACKET'}
    return token, index + 1


def readLBracket(line, index):
    token = {'type': 'L_BRACKET'}
    return token, index + 1


def multiplication(tokens, tmp, index):
    term = tmp['number']*tokens[index+1]['number']
    tmp = {'type': 'NUMBER', 'number': term}
    return tmp, index + 2


def division(tokens, tmp, index):
    term = tmp['number']/tokens[index+1]['number']
    tmp = {'type': 'NUMBER', 'number': term}
    return tmp, index + 2


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit(): (token, index) = readNumber(line, index)
        elif line[index] == '+': (token, index) = readPlus(line, index)
        elif line[index] == '-': (token, index) = readMinus(line, index)
        elif line[index] == '*': (token, index) = readMulti(line, index)
        elif line[index] == '/': (token, index) = readDiv(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# multiplication, division
def firstEvaluate(tokens):
    tmp = {'type': 'PLUS'}
    md_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTI':
            (tmp, index) = multiplication(tokens, tmp, index)
        elif tokens[index]['type'] == 'DIV':
            (tmp, index) = division(tokens, tmp, index)
        else:
            md_tokens.append(tmp) # ひとつ前に保存したtoken
            tmp = tokens[index] # 現在のtokenに更新
            index += 1
    # 最後にtmpに保存したtokenを追加
    md_tokens.append(tmp)
    return md_tokens

# addition, subtraction
def secondEvaluate(tokens):
    answer = 0
#     tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    md_tokens = firstEvaluate(tokens)
    actualAnswer = secondEvaluate(md_tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2")
    test("1+2+2")
    test("1-2")
    test("1-2-3")
    test("1+2-3")
    test("1+2+3-9")
    test("1.0+2.0")
    test("1.0-2.0")
    test("1.3+1.5")
    test("1.4-1.3")
    test("1.3+1.4+1.7")
    test("1.5-2.8-3.9")
    test("1.3-5.4+4.5")
    test("2.3+4.9-5.6")
    test("2.34+39.4")
    test("8.59-3.53")
    test("9.58-3.45+3.544")
    
    test("1*2")
    test("1*2*2")
    test("1/2")
    test("1/2-3")
    test("1*2/3")
    test("1*2*3/9")
    test("1.0*2.0")
    test("1.0/2.0")
    test("1.3*1.5")
    test("1.4/1.3")
    test("1.3*1.4*1.7")
    test("1.5/2.8/3.9")
    test("1.3/5.4*4.5")
    test("2.3*4.9/5.6")
    test("2.34*39.4")
    test("8.59/3.53")
    test("9.58/3.45*3.544")
    
    test("1+4*3")
    test("1-4*3")
    test("1-4/2")
    test("1+4/2")
    test("1.0+4.0*3.0")
    test("1.0-4.0*3.0")
    test("1.0-4.0/2.0")
    test("1.0+4.0/2.0")
    test("1.2+4.2*3.2")
    test("1.2-4.2*3.2")
    test("1.3-4.3/2.3")
    test("1.4+4.4/2.4")
    
    test("3+4-5*3")
    test("3-4+5*3")
    test("4+5-5/2")
    test("4-5+5/2")
    test("4-5+5*2+4/2")
    test("4+5-5*2-4/2")
    test("5*2-4/2+4+5")
    test("5*2/6-10+1")
    test("6/2*3+10+1")
    
    test("3.0+4.3-5.3*30.3")
    test("3.3-4.333+35.3*333.3")
    test("4.6+5.33-5.44/332.4")
    test("44.4-5.2+5.22/222.4")
    test("4.33-5.2222+5444.3*233.55+2.44/44.20")
    test("43.4+5.44-5.44*2.333-3333.4/3.20")
    test("5*27-43.4/2.3+2.344+555.5")
    test("5.009*2.5/6.33-10.44+1.33")
    test("6003.4/2.3*33.3+10.33+1.3")
    
    
    print("==== Test finished! ====\n")

runTest()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    md_tokens = firstEvaluate(tokens)
    answer = secondEvaluate(md_tokens)
    print("answer = %f\n" % answer)
