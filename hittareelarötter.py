import math
def evaluate_function(function_string, x):
    return eval(function_string)

tolerance = 0.0001
i_tot = 0
def newtons_metod(function_string, deriv_string, x):
    global i_tot
    dx = 1; y = 1; Error = False; i = 0
    
    if evaluate_function(deriv_string,x) == 0: #Förhindra att newton startar på extrempunkt
        x = 3
    while abs(dx) > tolerance:
        y = evaluate_function(function_string,x)
        dx = y / evaluate_function(deriv_string,x) 
        x += -dx #Går mot nollstället
        i += 1
        if i > 90:
            Error = True
            break
    else:
        x += -dx
        i_tot += i
    if not Error:
        return x
    else:
        return None #ger ingenting

from polynomderiverare2 import get_all_derivatives
import datetime

"""
Skriv polynomet i variabeln poly för att hitta dess reella nollställen
exempel: 
poly =  "3x**6 -2x+ 5x+2"
eller
poly = "3*x^6 -2*x+ 5*x+2"

Sen är det bara att köra kommandot 
roots = get_real_roots(poly)[0]
print(roots)

"""

def get_real_roots(poly):
    #Tar bort mellanslag
    global i_tot
    i_tot = 0
    poly = "".join(poly.split())
    
    #Modifierar poly för att kunna deriveras, deriverare accepterar i formen 3x**6-2x+5x+6
    poly = list(poly) 

    for i in range(1, len(poly)):
        prev_char = poly[i-1]
        char = poly[i]
        if char == "x" and prev_char == "*":
            poly[i-1] = ""
            poly[i] = "x"
        if char == "^":
            poly[i] = "**"
    poly = "".join(poly) 

    
    a = datetime.datetime.now()
    text_deriv_list = get_all_derivatives(poly)
    b = datetime.datetime.now()
    timeForDerivatives = int((b - a).total_seconds() * 1000)
    
    #Modifierar poly för att fungera för eval()
    # Byter ut t.ex. 5x + x^2 till 5*x + x**2
    polyForEval = list(poly) 
    for i in range(1, len(polyForEval)):
        prev_char = polyForEval[i-1]
        char = polyForEval[i]
        if char == "x" and prev_char.isdigit():
            polyForEval[i] = "*x"
        elif char == "^":
            polyForEval[i] = "**"
    polyForEval = "".join(polyForEval) 
 
    all_functions = [polyForEval] + text_deriv_list
    all_functions = all_functions[::-1]
    
    """Själva processen börjar här
    1. Hitta nollställen till näst lägsta derivatan(rät linje)
    2. De hittade nollställena är primitiva funktionens extrempunkter
    3. Hitta den primitiva funktionens nollställe genom att leta mellan och utanför 
       extrempunkterna m.h.a newtons method och vissa vilkor
    4. Gör om processen tills moder funktionen är nådd
    """
    guesses = [0]

    for i in range(1, len(all_functions) - 1):
        deriv_string = all_functions[i-1]
        function_string = all_functions[i]
        roots = []
        for guess in guesses:
            root = newtons_metod(function_string, deriv_string, guess) #Hittar rötter för function_string
            if root or root == 0:
                roots.append(root)
            elif root == None:
                print("Newton sök stoppad, för många iterationer!")
        numRoots = len(roots)
        
        #Konstruera gissningar för nästa funktion
        if i + 1 < len(all_functions):
            guesses = []
            if numRoots == 1: #För en enkel andragradsfunktion
                root = roots[0]
                dy0 = evaluate_function(all_functions[i], root + 1)
                dy1 = evaluate_function(all_functions[i], root + 1)   
                extrema = evaluate_function(all_functions[i+1], root)
                a = extrema * dy0 #Positiv om x-axeln korsas
                b = extrema * dy1
                if (a <= 0 or b >= 0):
                    guesses = [root-3, root+3] ##Hitta formel för detta? ist för 3
                
            elif numRoots >= 2:
                for j in range(0, numRoots - 1):
                    root = roots[j]
                    next_root = roots[j+1]
                    dx = (next_root - root) / 2

                    y0 = evaluate_function(all_functions[i+1], root)
                    y1 = evaluate_function(all_functions[i+1], next_root)
                    if (y0 * y1 <= 0) or abs(y1 - y0) >= tolerance: #Om teckenbyte, x-axel korsas
                        guesses.append(root + dx) #Lägger till sökställe mellan extrempunkter
                        
                #Placerar sökställen utanför de yttre extrempunkterna
                first_root = roots[0]
                dy0 = evaluate_function(all_functions[i], first_root - 1)
                y0 = evaluate_function(all_functions[i+1], first_root)
                    
                last_root = roots[-1]
                dy1 = evaluate_function(all_functions[i], last_root + 1)
                y1 = evaluate_function(all_functions[i+1], last_root)
                a = y0 * dy0 #Positiv om x-axeln korsas
                b = y1 * dy1
                if (a >= 0):
                    guesses = [roots[0] - dx] + guesses #Vänster om den yttre extrempunkten
                if (b <= 0):
                    guesses = guesses + [roots[-1] + dx] #Höger om den yttre extrempunkten
            else: #Om inga extrempunkter finns
                guesses = [0] 

    """"Och slutligen för själva moderfunktionen"""
    roots = []

    for guess in guesses:
        root = newtons_metod(all_functions[-1], all_functions[-2], guess) 
        if root or root == 0:
            roots.append(root)
        elif root == None:
            print("Newton sök stoppad på moder funktionen, för många iterationer!")
            
    return roots, i_tot, timeForDerivatives #Obs endast multipliciet <= 2 kan räknas med

"""
Denna del är till för att lösa flera polynom från ett textdokument och 
spara värden för tid och error i ett textdokument.
(denna del nedanför behövs alltså inte om man bara ska köra lösaren på ett polynom)
"""
file = open('polynomials.txt','r')
wfile = open('resultsPolynomials.txt','w')

m = 0
for line in file:
    if m % 2 == 0:
        poly = line
        a = datetime.datetime.now()
        found_roots, i_tot, derivativeTime = get_real_roots(poly)
        b = datetime.datetime.now()
        delta = b - a
        microseconds = int(delta.total_seconds()*1000)
    else:
        text = ",".join(["Tid(ms):", str(microseconds), "Grad:", str(m//2+2), "i_tot:", str(i_tot), "\n"])
        wfile.write(text)
    m += 1
else:
    print("Korrekta rötter - funna rötter =", sum([int(r) for r in line.split(",")])+sum(found_roots))
    
    
print("Antal rötter:", len(found_roots))
#print("Rötterna är:", found_roots)
sumFunctionRoots = 0
for root in found_roots:
    x = root
    sumFunctionRoots += abs(eval(poly))
print("Ackumulerad summa av rötterna: ", sumFunctionRoots)
 
file.close()
wfile.close()
