"""Sepererar till termer"""

plus_minus = ("+", "-")
def seperate_into_terms(text): #Detta görs en gång
    list_with_terms = []  
    start = 0
    end = 0
    for i in range(len(text)): #Texten deles upp i en lista där + och - är "snitten"
        if text[i] in plus_minus:
            end = i
            term = text[start:end] #detta inkluderar minustecken och plus
            start = i
            if term:
                list_with_terms.append(term)
    else:
        list_with_terms.append(text[end:]) #För sista
    return list_with_terms

def seperate_into_factors(term): #Detta görs en gång.
    x_i = term.find("x")
    #Om ingen koefficient, eller + då har den koefficienten 1
    if x_i == 0:
        factor_form = [1, term[x_i:]]
    else: #Om koefficient finns
        factor_form = [term[:x_i], term[x_i:]] #k , x**c     
    if len(str(factor_form[0])) == 1: #Om koefficienten är 1 tecken långt
        if factor_form[0] == "-":
            factor_form[0] = -1
        elif factor_form[0] == "+":
            factor_form[0] = 1
            
    #Koefficienten är i text, nu kan man floata
    factor_form[0] = float(factor_form[0]) 
    return factor_form

"""Detta upprepas"""
def get_exponent(term):
    exp_i = term[1].find("**")
    if exp_i == -1: #Om ingen exponent funnen, exponent = 1
        return 1
    else: #Om hittad
        return float(term[1][exp_i+2:])
    
def remove_constants(terms):
    new_terms = []
    for term in terms:
        #Kolla om termen innehåller någon bokstav, variabel eller inte exponenten 0
        if term[1].islower() and float(get_exponent(term)) != 0: #Om term har bokstav och exponent != 0
            new_terms.append(term)  #Lägger till term som har x och inte exp 0
    return new_terms

def get_derivative(terms): #av termer i faktorform
    derivative = []
    terms = remove_constants(terms)
    for term in terms:
        exp = get_exponent(term)
        a = [term[0] * exp, ("x**" + str(exp - 1))] #term[0] = koefficient
        derivative.append(a)
    return derivative

def get_all_derivatives(text):
    terms = seperate_into_terms(text) #Översätt för datorn
    terms = [seperate_into_factors(term) for term in terms] #Görs 1 gång
 
    the_list = []
    deriv = terms
    while deriv:
        derivative = get_derivative(deriv)
        the_list.append(derivative)
        deriv = derivative
    else:
        the_list.pop(-1) #Tar bort en tom array

    text_deriv_list = []
    for deriv in the_list: #För varje derivata
        text_deriv = "" #är en funktions hela derivata
        for term in deriv:
            if str(term[0])[0] != "-":  #Om inte minus
                text_deriv += "  +" + str(term[0]) + "*" + str(term[1]) #term[0] = koefficien, term[1] == x**b
            else: #Om minus
                text_deriv += "  " + str(term[0]) + "*" + str(term[1])
        text_deriv_list.append(text_deriv)
    return text_deriv_list

