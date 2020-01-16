from libs.ortools_lib import Simple_SolVal,newSolver,ObjVal
from random import randint, random
import sys
from libs import tableutils

def gen_data_resources(oils = 9, acids = 7):
    #Kinds of oils should be bigger than acids (oils > acids)

    resources = []

    for i in range(oils):
        oil = []
        total_percentage = 100

        for j in range(acids-1):

            if total_percentage > 1:
                acid = randint(1,min(70,total_percentage)) * randint(0,1)
            else:
                acid = 0

            total_percentage -= acid
            oil.append(acid)

        oil.append(total_percentage)
        resources.append(oil)

    return resources

" Boundaries Of Acids - Target "

def gen_data_acids_boundaries(resources):

    percentages_acids_ByOil = []
    lb,ub=[],[]
    oils,acids=len(resources),len(resources[0])
    total_percentage=100
    R=[0 for j in range(acids)]

    for i in range(oils-1):

        if total_percentage:
            f=randint(1,min(20,total_percentage))
        else:
            f=0

        percentages_acids_ByOil.append(f)
        total_percentage -= f

        for j in range(acids):
            acid = f*resources[i][j]
            R[j] += acid

    f=total_percentage
    percentages_acids_ByOil.append(f)

    for j in range(acids):
        acid = f*resources[oils-1][j]
        R[j] += acid

    for j in range(acids):
        lb.append((0.95*R[j]/100.0))
        ub.append((1.05*R[j]/100.0))

    return [lb,ub]

def gen_data_costs(oils = 9, months = 12):

    cost_oils = []

    for i in range(oils):
        oil = []
        for j in range(months):
            cost = randint(100,200)
            oil.append(cost)

        cost_oils.append(oil)

    return cost_oils


def gen_data_inventory(oils = 9):
    # What 'Held' in the inventory initial for each oil in tons
    Hold=[]
    for i in range(oils):
        cost = [randint(0,200)]
        Hold.append(cost)
    return Hold

def model_soap_manufacturing_problem(resources,target,costs,inventory,demand,storage_cost,boundaries_hold_inventory):

  s = newSolver('Multi-period soap Blending/Stock problem')

  " Declaring & Initializing decision variables "

  oils= range(len(resources))
  months, acids = range(len(costs[0])), range(len(resources[0]))
  buy = [[s.NumVar(0,demand,'') for _ in months] for _ in oils]
  blend = [[s.NumVar(0,demand,'') for _ in months] for _ in oils]
  hold = [[s.NumVar(0,demand,'') for _ in months] for _ in oils]
  total_qty_produced = [s.NumVar(0,demand,'') for _ in months]
  cost_production= [s.NumVar(0,demand*1000,'') for _ in months]
  cost_storage = [s.NumVar(0,demand*1000,'') for _ in months]
  acid = [[s.NumVar(0,demand*demand,'') for _ in months] for _ in acids]

  " Constraints "

  for i in oils:
    s.Add(hold[i][0] == inventory[i][0])

  for j in months:
    s.Add(total_qty_produced[j] == sum(blend[i][j] for i in oils))
    s.Add(total_qty_produced[j] >= demand)

    if j < months[-1]:
      for i in oils:
        s.Add(hold[i][j]+buy[i][j]-blend[i][j] == hold[i][j+1])

    s.Add(sum(hold[i][j] for i in oils) >= boundaries_hold_inventory[0])
    s.Add(sum(hold[i][j] for i in oils) <= boundaries_hold_inventory[1])

    for k in acids:
      s.Add(acid[k][j] == sum(blend[i][j]*resources[i][k] for i in oils))
      s.Add(acid[k][j] >= target[0][k] * total_qty_produced[j])
      s.Add(acid[k][j] <= target[1][k] * total_qty_produced[j])

    s.Add(cost_production[j] == sum(buy[i][j] * costs[i][j] for i in oils))
    s.Add(cost_storage[j] == sum(hold[i][j] * storage_cost for i in oils))

  total_production_cost = s.Sum(cost_production[j] for j in months)
  total_storage_cost = s.Sum(cost_storage[j] for j in months)

  s.Minimize(total_production_cost+total_storage_cost)
  rc = s.Solve()

  buy,blend,hold,acid = Simple_SolVal(buy),Simple_SolVal(blend),Simple_SolVal(hold),Simple_SolVal(acid)
  total_production_cost ,total_storage_cost,total_qty_produced  = Simple_SolVal(cost_production), Simple_SolVal(cost_storage), Simple_SolVal(total_qty_produced)

  return rc,ObjVal(s),buy,blend,hold,total_qty_produced,acid,total_production_cost,total_storage_cost

def main():

    oils = 9
    acids = 7
    months = 12

    if len(sys.argv) <= 1:
        print('Usage is main [resources|target|cost|inventory|run] [seed]')
        return

    elif len(sys.argv) > 2:
        random.seed(int(sys.argv[2]))

    resources = gen_data_resources(oils, acids)
    acid_boundaries = gen_data_acids_boundaries(resources)
    costs = gen_data_costs(oils, months)
    inventory = gen_data_inventory(oils)

    if sys.argv[1] == 'resources':

        for j in range(oils):
            resources[j].insert(0, 'O' + str(j))
        resources.insert(0, [''] + ['A' + str(i) for i in range(acids)])
        tableutils.printmat(resources, False, 1)

    elif sys.argv[1] == 'target':

        acid_boundaries.insert(0, [''] + ['A' + str(i) for i in range(acids)])
        acid_boundaries[1].insert(0, 'Min')
        acid_boundaries[2].insert(0, 'Max')
        tableutils.printmat(acid_boundaries, True, 1)

    elif sys.argv[1] == 'cost':

        for j in range(oils):
            costs[j].insert(0, 'O' + str(j))
        costs.insert(0, [''] + ['Month ' + str(i) for i in range(months)])
        tableutils.printmat(costs)

    elif sys.argv[1] == 'inventory':
        for j in range(oils):
            inventory[j].insert(0, 'O' + str(j))
        inventory.insert(0, ['Oil', 'Held'])
        tableutils.printmat(inventory)

    elif sys.argv[1] == 'run':
        demand = 5000
        boundaries_hold_inventory = [500, 2000]
        cost = 5
        #the 'rc' variable should have the value of zero, that mean that the model found the optimal solution elsewhere it's not optimal
        rc, obj_value,buy,blend,hold,total_qty_produced,acid,total_production_cost,total_storage_cost = model_soap_manufacturing_problem(resources, acid_boundaries, costs, inventory, demand, cost, boundaries_hold_inventory)
        print('Feasibility of the model -> ', rc)

        if len(buy):
            acid.append([0 for l in range(len(acid[0]))])
            for j in range(len(acid) - 1):
                for l in range(len(acid[0])):
                    acid[j][l] = acid[j][l] / total_qty_produced[l]
                    acid[-1][l] += acid[j][l]

            for j in range(oils):
                buy[j].insert(0, 'O' + str(j))
                blend[j].insert(0, 'O' + str(j))
                hold[j].insert(0, 'O' + str(j))

            for l in range(acids):
                acid[l].insert(0, 'A' + str(l))

            acid[-1].insert(0, 'Total')
            buy.insert(0, ['Buy qty'] + ['Month ' + str(i) for i in range(months)])
            blend.insert(0, ['Blend qty'] + ['Month ' + str(i) for i in range(months)])
            hold.insert(0, ['Hold qty'] + ['Month ' + str(i) for i in range(months)])
            acid.insert(0, ['Acid %'] + ['Month ' + str(i) for i in range(months)])

            total_qty_produced = [total_qty_produced]
            total_qty_produced[0].insert(0, 'Prod qty')
            total_production_cost = [total_production_cost]
            total_production_cost[0].insert(0, 'P. Cost')
            total_storage_cost = [total_storage_cost]
            total_storage_cost[0].insert(0, 'S. Cost')

            tableutils.printmat(buy, True, 1)
            print('\n')
            tableutils.printmat(blend, True, 1)
            print('\n')
            tableutils.printmat(hold, True, 1)
            print('\n')
            tableutils.printmat(total_qty_produced, True, 1)
            tableutils.printmat(total_production_cost, True, 2)
            tableutils.printmat(total_storage_cost, True, 2)
            print('\n')
            tableutils.printmat(acid, True, 1)

if __name__ == '__main__':
    # print('Usage is main [resources|target|cost|inventory|run] [seed]')
    print(sys.argv.append('run'))
    main()

