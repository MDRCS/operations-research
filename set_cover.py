from random import randint,uniform,random
import sys
from ortools.linear_solver import pywraplp
from libs.ortools_lib import Simple_SolVal,ObjVal
from libs import tableutils


def data_model(suppliers = 13, parts = 25):
    " data model based on a number of suppliers with parts that they could provide to General Engine Corp "
    covered_parts = [0 for i in range(parts)]

    while sum(covered_parts) < parts:
        suppliers_data = []
        covered_parts = [0 for i in range(parts)]
        p = 0.8

        for i in range(suppliers):
            supplier = []
            for j in range(parts):
                if uniform(0,1) > p:
                    supplier.append(j)
                    covered_parts[j] = 1
            suppliers_data.append(supplier)

    costs = [randint(0,10) for i in range(suppliers)]
    return suppliers_data,costs


def solve_model(suppliers_data,costs=None):
  solver_title = 'Set Cover'
  solver = pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
  s = pywraplp.Solver(solver_title,solver)

  " Initialization "
  suppliers = len(suppliers_data)
  parts = len(set([prt for prts in suppliers_data for prt in prts]))
  supplier = [s.IntVar(0,1,'')  for i in range(suppliers)]

  " Constraints "

  " C1 : we need that a part j be provided by at least one supplier "
  for j in range(parts):
    s.Add(1 <= sum(supplier[i] for i in range(suppliers) if j in suppliers_data[i]))

  " Objective function "

  " If each supplier have a cost we will inject the variable into the equation, so the problem will be minimizing (set_cover *cost) else minimize (set_cover) "
  s.Minimize(s.Sum(supplier[i]*(1 if costs is None else costs[i]) \
    for i in range(suppliers)))

  rc = s.Solve()

  " Extract result "

  valide_suppliers = [i for i in range(suppliers) if Simple_SolVal(supplier[i])>0]

  " we can find two suppliers provide the same part, that is what we are going to find in this list of lists" \
  " Each list containt suppliers that provide j part that is the index of the list " \
  " Example : j=0 search in the valide_suppliers vector about who could provide us with the a part with index j"

  suppliers_part = [
      [i for i in range(suppliers) if j in suppliers_data[i] and Simple_SolVal(supplier[i])>0]
      for j in range(parts)]

  return rc,ObjVal(s),valide_suppliers,suppliers_part



def main():
    suppliers = 13
    parts = 25

    if len(sys.argv) < 1:
        print('Usage is main [data|run] [seed]')
        return
    # elif len(sys.argv) > 2:
    #     random.seed(int(sys.argv[2]))

    data,costs = data_model()

    if sys.argv[1] == 'data':
        data_table = []
        for i in range(suppliers):
            data_table.append([tableutils.set2string(data[i])])
        data_table = tableutils.splitwrapmat(data_table, ['S' + str(i) for i in range(suppliers)], ['Supplier', 'Part numbers'])
        tableutils.printmat(data_table, True)

    elif sys.argv[1] == 'run':

        feasibility, obj_value, suppliers, suppliers_part = solve_model(data)
        data_table = []
        for i in range(len(suppliers_part)):
            data_table.append([tableutils.set2string(suppliers_part[i])])

        data_table.insert(0, [tableutils.set2string(suppliers)])
        data_table = tableutils.splitwrapmat(data_table, ['All'] + ['Part #' + str(j) for j in range(parts)], ['Parts', 'Suppliers'])
        tableutils.printmat(data_table, True)

if __name__ == '__main__':
    sys.argv.append('run')
    main()
    # sys.argv = []
    # sys.argv.append('run')
    # main()


