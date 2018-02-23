# -*- coding: utf-8 -*-
from sympy import * 
import random

x, y, z = symbols('x y z')


def generate_polynomial(n, minRoot):
    pol = "1"
    correct_roots  = []
    for i in range(n):
        s = str(random.randint(-50,40))
        if s == 0: s = 10
        if s[0] != "-":
            s = "+" + str(s)
        correct_roots.append(s)
        pol += "*(x" + s + ")"
    return pol, correct_roots
    

f = open('polynomials.txt','w')
maxDegree = 20 #maxDegree och antal polynom
for i in range(1, maxDegree):
    pol, correct_roots = generate_polynomial(i + 1, -maxDegree + i)
    f.write(str(expand(pol)) + "\n")
    f.write(",".join(correct_roots) + "\n")
    
f.close()
        
