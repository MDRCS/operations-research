from ortools.linear_solver import pywraplp
from libs.ortools_lib import Simple_SolVal,ObjVal,newSolver
from random import randint,uniform


def data_model(foods = 5, nutrients = 4):
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
    length = len(data)
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


if __name__ == '__main__':

    data = data_model()
    print('\n DATA : \n')

    for row in data:
        print(row)

    print('\n \n')
    obj_value,serving_foods = diet_solver(data)

    print('objective value -> ',obj_value)
    print('\n vector of serving food : \n')

    for f in range(len(serving_foods)):
        print(f'F{f}',round(serving_foods[f],2))
