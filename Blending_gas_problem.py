from ortools.linear_solver import pywraplp
from libs.ortools_lib import Simple_SolVal,ObjVal,newSolver
from random import randint

def raws_data(raw = 8):

    raws = []

    for i in range(raw):
        raws.append([randint(80,100),randint(600,1000),0])

    avg_octane = sum(raws[i][0] for i in range(raw))/float(raw)

    for i in range(raw):
        p = randint(50,55) + 4 * raws[i][0] /avg_octane
        raws[i][2] = round(p,2)

    return raws


def refined_data(ref = 3):
    refined = []

    for i in range(ref):
        refined.append([randint(87,95),randint(200,500),randint(5000,13000),0])
    avg_refined = sum(refined[i][0] for i in range(ref)) / float(ref)

    for i in range(ref):
        p = 61.0 + refined[i][0]/avg_refined
        refined[i][3] = round(p,2)

    return refined

def solve_gas(raws,refined):

    s = newSolver('gas blending')
    r = len(raws)
    re = len(refined)

    avl = 1 #Availabality
    ref_lb = 1
    ref_ub = 2
    cost = 2
    price = 3
    rating_octane = 0
    " Initialization "
    G = [[s.NumVar(0.0,10000,'') for i in range(re)] for j in range(r)]

    " Constraint "
    raws_capacity = [s.NumVar(0,raws[i][avl],'') for i in range(r)]
    refined_capacity = [s.NumVar(refined[i][ref_lb],refined[i][ref_ub],'') for i in range(re)]

    for i in range(r):
        s.Add(raws_capacity[i] == s.Sum(G[i][j] for j in range(re)))

    for j in range(re):
        s.Add(refined_capacity[j] == s.Sum(G[i][j] for i in range(r)))

    for j in range(re):
        s.Add(s.Sum([G[i][j] * raws[i][0] for i in range(r)]) == refined_capacity[j] * refined[j][rating_octane] )

    cost = s.Sum(raws_capacity[i] * raws[i][cost] for i in range(r)) #Cost = s.Sum(R[i]*C[i][Rcost] for i in range(nR))
    price = s.Sum(refined_capacity[j] * refined[i][price] for i in range(re))

    s.Maximize(price - cost)
    rc = s.Solve()

    return ObjVal(s),Simple_SolVal(G)


if __name__ == '__main__':
    raws = raws_data()
    refined = refined_data()
    print('raws : -> ',raws)
    print('refined : -> ',refined)

    obj_val,solution = solve_gas(raws,refined)

    print('Objective value : -> ', round(obj_val,2),'')
    print('Solution : -> ',solution)