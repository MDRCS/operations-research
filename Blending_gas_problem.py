import sys
from libs.ortools_lib import Simple_SolVal,ObjVal,newSolver
from random import randint,random
from libs import tableutils

def raws_data(raw):

    raws = []

    for i in range(raw):
        raws.append([randint(80,100),randint(600,1000),0])

    avg_octane = sum(raws[i][0] for i in range(raw))/float(raw)

    for i in range(raw):
        p = randint(50,55) + 4 * raws[i][0] /avg_octane
        raws[i][2] = round(p,2)

    return raws

def refined_data(ref):
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


def main():

    raw = 8
    ref = 3

    if len(sys.argv) <= 1:
        print('Usage is main [raw|ref|run] [seed]')

    # elif len(sys.argv) >= 3:
    #     random.seed(int(sys.argv[2]))

    raws = raws_data(raw)
    refined = refined_data(ref)

    if sys.argv[1] == 'raw':
        for i in range(raw):
            raws[i].insert(0, 'R' + str(i))
        raws.insert(0, ['Gas', 'Octane', 'Availability', 'Cost'])
        tableutils.printmat(raws)

    elif sys.argv[1] == 'ref':
        for i in range(ref):
            refined[i].insert(0, 'F' + str(i))
        refined.insert(0, ['Gas', 'Octane', 'Min demand.', 'Max demand.', 'Price'])
        tableutils.printmat(refined)

    elif sys.argv[1] == 'run':
        obj_val,solution = solve_gas(raws,refined)
        Price = 0.0
        Cost = 0.0
        T = []
        for i in range(raw + 2):
            T = T + [[0] * (2 + ref)]
        for i in range(raw):
            for j in range(ref):
                T[i][j] = round(solution[i][j], 2)
            T[i][ref] = round(sum([solution[i][j] for j in range(ref)]), 2)
            T[i][ref + 1] = round(sum([solution[i][j] * raws[i][2] for j in range(ref)]), 2)
            Price += sum([solution[i][j] * refined[j][3] for j in range(ref)])
        for j in range(ref):
            T[raw][j] = round(sum(solution[i][j] for i in range(raw)), 2)
            T[raw + 1][j] = round(sum([solution[i][j] * refined[j][3] for i in range(raw)]), 2)
            Cost += sum([solution[i][j] * raws[i][2] for i in range(raw)])
        T.insert(0, ['F0', 'F1', 'F2', 'Barrels', 'Cost'])
        for i in range(len(T)):
            if i == 0:
                T[i].insert(0, "")
            elif i <= raw:
                T[i].insert(0, "R" + str(i - 1))
            elif i == raw + 1:
                T[i].insert(0, "Barrels")
            else:
                T[i].insert(0, "Price")

        T[2 + raw][2 + ref] = '{0:.2f}'.format(Price - Cost)
        tableutils.printmat(T)

    # print('raws : -> ',raws)
    # print('refined : -> ',refined)
    #
    #
    #
    # print('Objective value : -> ', round(obj_val,2),'')
    # print('Solution : -> ',solution)

if __name__ == '__main__':

    main()
































