import math
import time

def eq1():
    df = 0
    di = input('enter di(m):>')
    v = input('enter v(m/s):>')
    t = input('enter t(s):>')
    di = int(di)
    v = int(v)
    t = int(t)
    vt = v * t
    vt = int(vt)
    df = di + vt
    print(df, ' meters')

def eq2():
    vf = 0
    a = input('enter a(m/s^2):>')
    t = input('enter t(s):>')
    vi = input('enter vi(m/s):>')
    if a == '9.80':
        a = 9.80
    t = int(t)
    vi = int(vi)
    at = a * t
    at = int(at)
    vf = at + vi
    print(vf, 'm/s')

def eq3():
    df = 0
    di = input('enter di(m):>')
    vi = input('enter vi(m/s):>')
    t = input('enter t(s):>')
    a = input('enter a(m/s^2):>')
    di = int(di)
    vi = int(vi)
    t = int(t)
    a = int(a)
    at = a * t
    vit = vi * t
    onehalf = 0.5
    onehalfat = onehalf * at
    onehalfatsq = onehalfat ** 2
    df = di + vit + onehalfatsq
    print(df, 'meters')

def eq4():
    vf = 0
    vi = input('enter vi(m/s):>')
    a = input('enter a(m/s^2):>')
    deltad = input('enter deltad(m):>')
    vi = int(vi)
    a = int(a)
    deltad = int(deltad)
    visq = vi ** 2
    twoa = a * 2
    twoadeltad = twoa * deltad
    vf = math.sqrt(visq + twoadeltad)
    print(vf, 'm/s')
