#-*- coding: utf-8 -*-
"""
Created on Wed Feb 03 12:18:38 2018

@author: Suresh Kumar Tathari

Functions related to acronym finder

Acronym definition:
    full form of the word written before its abbrevation is used.
    ex: Department of Energy (DOE)
Typical identification of acronym can be done from normal words if the letters of the word 
are in capital case and also the length of the word varies between 3 and 10
"""
import re

#loading stop words from nltk.
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))


def build_LCS_matrix(X, Y):
    """
    Returns longest common subsequence pointers (diagonal path -d) in the form of matrix
    """
    m = len(X)
    n = len(Y)

    #initialization of matrix c(LCS count) and matrix b(back pointer)
    #matrix will have +1 row and +1 column for LCS and of size (m+1, n+1)
    b = [[0] * (n + 1) for i in range(m + 1)]
    c = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = "d"
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = "u"
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = "l"
    return c, b


def parse_LCS_matrix(b, start_i, start_j, m, n, lcs_length, Stack, Vectorlist):
    """
    Returns the result list of LCS parsing through the matrix.
    """
    for x in range(start_i, m + 1):
        for y in range(start_j, n + 1):
            if (b[x][y] == "d"):
                Stack.append((x, y))
                if lcs_length == 1:
                    vector = build_Vector(Stack, n)
                    Vectorlist.append(vector)
                else:
                    parse_LCS_matrix(b, x + 1, y + 1, m, n, lcs_length - 1, Stack, Vectorlist)
                Stack.pop()
    return Vectorlist


def build_Vector(Stack, n):
    vector = [0]*n
    for i, j in Stack:
        vector[j - 1] = i
    return vector


def vector_Values(V, types):
    i = 1
    start = end = 0
    for i, x in enumerate(V):
        if x is not None:
            start = i
            break
    V_rev = V[::-1]
    for i, x in enumerate(V_rev):
        if x is not None:
            end = i
            break

    dict = {}
    dict['size'] = end - start + 1
    dict['distance'] = (len(V) - 1) - end
    dict['misses']=0
    dict['stopcount']=0
    for i in range(start, end + 1):
        if (V[i] > 0 and types[i] == 's'):
            dict['stopcount'] = dict['stopcount'] + 1
        elif (V[i] == 0 and types[i] != 's'):
            dict['misses'] = dict['misses'] + 1
    return dict


def compare_Vectors(A, B, types):
    vector_A = vector_Values(A, types)
    vector_B = vector_Values(B, types)

    if (vector_A['misses'] > vector_B['misses']):
        return B
    elif (vector_A['misses'] < vector_B['misses']):
        return A
    if (vector_A['stopcount'] > vector_B['stopcount']):
        return B
    elif (vector_A['stopcount'] < vector_B['stopcount']):
        return A
    if (vector_A['distance'] > vector_B['distance']):
        return B
    elif (vector_A['distance'] < vector_B['distance']):
        return A
    if (vector_A['size'] > vector_B['size']):
        return B
    elif (vector_A['size'] < vector_B['size']):
        return A
    return A


def get_Acronym_Definition(words, acronym):
    """ Acronym definition finder function"""
    index = -1  #Acronym index
    i = -1
    for word in words:
        i += 1
        if acronym in word:
            index = i
            break

    if (index == -1):
        return "Acronym not found"

    #words before the acronym pre-window
    prew = []

    #prew start index
    prew_start = index - (2 * len(acronym))
    if (prew_start < 0):
        prew = words[:index]
    else:
        prew = words[prew_start:index]

    prew_string = ' '.join(prew)

    #check for braces
    prew_text = re.findall('[\w]+', prew_string)

    #first letter of words in prewindow list
    leaders = [x[0].lower() for x in prew_text]

    #list for storing the types of words in prewindow list
    #s-stopword, w-word
    types = []
    for x in prew_text:
        if x.lower() in stopWords:
            types.append('s')
        else:
            types.append('w')

    #string of acronym letters and leaders initials
    ai = acronym.lower()
    li = ''.join(leaders)

    m = len(ai)
    n = len(li)

    #LCS Matrix
    c, b = build_LCS_matrix(ai, li)

    #building the results vector by parsing the matrix
    result_vector = parse_LCS_matrix(b, 0, 0, m, n, c[m][n], [], [])

    #if words not found
    if (not result_vector):
        return "No definition found"

    #Comparing vectors for best possible match
    final_Vector = result_vector[0]
    for i in range(1, len(result_vector)):
        final_Vector = compare_Vectors(final_Vector, result_vector[i], types)

    #finding the starting and ending index of acronym words
    start = next((integer for integer, enum in enumerate(final_Vector) if enum), None)
    V_rev = final_Vector[::-1]
    end   = next((integer for integer, enum in enumerate(V_rev) if x), None)
    end   = (len(final_Vector)-1) - end
    
    #forming the list of words for acronym definition and returning it
    result=[]
    for i,x in enumerate(final_Vector):
        if (i>=start and i<=end):
             result.append(prew_text[i])

    return ' '.join(result)