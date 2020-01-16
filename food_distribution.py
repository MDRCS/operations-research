import sys
from libs.ortools_lib import Simple_SolVal,ObjVal,newSolver
from random import randint,uniform,random
from tableutils import wrapmat,printmat,formatmat

def data_model(foods, nutrients):
    diet_data = []
    min_nut = []
    max_nut = []

    x = [randint(15,25) for i in range(foods)]

    for i in range(foods):
        diet_data.append([randint(10,600),randint(10,600),randint(10,1000),randint(10,80),randint(1,15),randint(15,45), round(uniform(4.00,10.00),2)])

    for j in range(nutrients):
        interval = sum([x[i] * diet_data[i][j] for i in range(foods)])

        min_nut.append(randint(0,interval))
        max_nut.append(randint(interval,2*interval))

    diet_data.append(min_nut+['','',''])
    diet_data.append(max_nut + ['', '', ''])

    return diet_data

def diet_solver(data):

    " Solver "
    s = newSolver('diet solver')

    " Variables "
    min_food = 4
    max_food = 5
    cost = 6
    nutrients = 4
    foods = 5
    min_nut = 5
    max_nut = 6
    " Initialization "
    serving_food = [s.NumVar(data[i][min_food],data[i][max_food],'') for i in range(foods)]

    " Constraints "
    for j in range(nutrients):
        s.Add(s.Sum([data[i][j] * serving_food[i] for i in range(foods)]) >= data[min_nut][j])
        s.Add(data[max_nut][j] >= s.Sum([data[i][j] * serving_food[i] for i in range(foods)]))

    " Objective Function "
    cost_per_serving_foods = s.Sum([data[i][cost] * serving_food[i] for i in range(foods)])
    s.Minimize(cost_per_serving_foods)

    rc = s.Solve()

    return ObjVal(s),Simple_SolVal(serving_food)


def main():

    if len(sys.argv) == 1:
        return

    elif len(sys.argv) == 3:
        random.seed(int(sys.argv[2]))

    if sys.argv[1] == 'run':
        foods = 5
        nutrients = 4
        header = [''] + ['N' + str(i) for i in range(nutrients)] + ['Min', 'Max', 'Cost', 'Solution']
        data = data_model(foods, nutrients)
        obj_value, serving_foods = diet_solver(data)
        T = [0] * nutrients
        C = 0
        for food in range(foods):
            C = C + serving_foods[food] * data[food][nutrients + 2]
            for nutrient in range(nutrients):
                T[nutrient] = T[nutrient] + serving_foods[food] * data[food][nutrient]
        for i in range(nutrients):
            T[i] = int(round(T[i], 0))
        T = T + ['', '', round(C, 2), '']
        table = data + [T]
        for i in range(0, foods):
            table[i] = table[i] + [round(serving_foods[i], 2)]

        wrapmat(table, ['F' + str(i) for i in range(foods)] + ['Min', 'Max', 'Sol'], header);
        printmat(formatmat(wrapmat(table, ['F' + str(i) for i in range(foods)] + ['Min', 'Max', 'Sol'], header), True, 4))

if __name__ == '__main__':

    main()
