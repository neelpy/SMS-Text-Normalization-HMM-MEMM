import string

def align(T, S):
    
    for char in string.punctuation:
        T = T.replace(char, '')
        S = S.replace(char, '')

    T, S = ['$start$'] + T.lower().split() + ['$end$'], ['$start$'] + S.lower().split() + ['$end$']
    tl, sl = len(T), len(S)
    pivot = []

    for i, ti in enumerate(T):
        for j in range(max((0, int(i/tl*sl)-4)), min((int(i/tl*sl)+4, sl))):
            if ti==S[j]:
                pivot.append([i ,j])
                break

    for i, current in enumerate(pivot[:-1]):
        next = pivot[i+1]
        diff0, diff1, diff = next[0]-current[0], next[1]-current[1], sum(next)-sum(current)
        if(diff==4):
            pivot.append([current[0]+1, current[1]+1])
        elif(diff<4):
            pass
        else:
            # Soundex Algorithm
            pass

    sentence = []
    for p in pivot[1:-1]:
        sentence.append((S[p[1]], T[p[0]]))

    return sentence

def extract_word_varients(sentences):
    
    word_varients = {}
    
    for sentence in sentences:
        for word in sentence:
            word_varients[word[0]] = {}
    
    for sentence in sentences:
        for word in sentence:
            if word[1] in word_varients[word[0]]:
                word_varients[word[0]][word[1]] += 1
            else:
                word_varients[word[0]][word[1]] = 1

    for word in list(word_varients.keys()):
        varient = word_varients[word]
        f = sum(list(varient.values()))
        if(f<10):
            del word_varients[word]

    return word_varients



# TESTING
T = "yes ... Me already intro to but haven intro yet . Anyway wat 's ur favorite part time hobbies ."
S = "Yes ... I 've already introduced but you haven 't introduced yet . Anyway what 's your favorite part time hobbies ."

sentence = align(T, S)
sentences = [sentence]
word_vars = extract_word_varients(sentences) 

print(word_vars)