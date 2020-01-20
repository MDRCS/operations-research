from __future__ import print_function
from random import randint,random
import time
import sys
from math import ceil
from libs.ortools_lib import Simple_SolVal, ObjVal, newSolver
from libs import tableutils

def data_model(types_packages):
  " type of packages - number of packages - unit weight "
  packages = []

  for i in range(types_packages):
    type_package = [randint(6,10),randint(200,500)] #number of packages, Unit weight
    packages.append(type_package) # type of a package : 0, info { number of packages, Unit weight }

  truck_weight_limit = randint(1200, 1500)
  return packages,truck_weight_limit

def solve_model(packages,truck_weight_limit,symmetry_break=False,knapsack=True):

  s = newSolver('Bin Packing',True) #True means that we will use an interger programming solver
  packages_types,total_number_packages = len(packages), sum([package[0] for package in packages])
  all_weights_packages = [e for sub in [[package[1]]*package[0] for package in packages] for e in sub] #Each case is a package unit weight //difficult expr
  nbr_trucks,min_trucks = bound_trucks(all_weights_packages,truck_weight_limit)

  assign_package_totruck = [[[s.IntVar(0,1,'')  for _ in range(nbr_trucks)] \
      for _ in range(package[0])] for package in packages]

  available_trucks = [s.IntVar(0,1,'')  for _ in range(nbr_trucks)] #1 if truck is available else 0


  " Constraints "

  for k in range(nbr_trucks):
    " 1- Sum of Weights of packages assigned to a truck should be small than the weight capacity of the truck "
    weights_packages_oftruck = sum(packages[i][1]*assign_package_totruck[i][j][k] \
              for i in range(packages_types) for j in range(packages[i][0]))
    s.Add(weights_packages_oftruck <= truck_weight_limit*available_trucks[k])

  " 2- we should ensure that each package find it's way to a truck that mean a package i, " \
  "sum of [p[j]] should be one that mean that package is assigned to a truck j"

  for i in range(packages_types):
    for j in range(packages[i][0]):
      s.Add(sum([assign_package_totruck[i][j][k] for k in range(nbr_trucks)]) == 1)

  " Breaking symmetry help us improve runtime execution "
  if symmetry_break:
    for k in range(nbr_trucks-1):
      s.Add(available_trucks[k] >= available_trucks[k+1])
    for i in range(packages_types):
      for j in range(packages[i][0]):
        for k in range(nbr_trucks):
          for jj in range(max(0,j-1),j):
            s.Add(sum(assign_package_totruck[i][jj][kk] \
              for kk in range(k+1)) >= assign_package_totruck[i][j][k])
          for jj in range(j+1,min(j+2,packages[i][0])):
            s.Add(sum(assign_package_totruck[i][jj][kk] \
              for kk in range(k,nbr_trucks))>=assign_package_totruck[i][j][k])

  " Normal Solution "
  if knapsack:
    s.Add(sum(truck_weight_limit*available_trucks[i] for i in range(nbr_trucks)) >= sum(all_weights_packages))

  " Objective function -> minimizing number of trucks and also not reduce the number of trucks that the min trucks number "
  s.Add(sum(available_trucks[k] for k in range(nbr_trucks)) >= min_trucks)
  s.Minimize(sum(available_trucks[k] for k in range(nbr_trucks)))
  rc = s.Solve()

  packages_trucks_vector=[[packages[i][1], [k  for j in range(packages[i][0]) for k in range(nbr_trucks)
                  if Simple_SolVal(assign_package_totruck[i][j][k])>0]] for i in range(packages_types) ] #assigning packages by unit_weight/Type to trucks

  trucks_overview=[[k, [(i,j,packages[i][1]) \
    for i in range(packages_types) for j in range(packages[i][0])\
            if Simple_SolVal(assign_package_totruck[i][j][k])>0]] for k in range(nbr_trucks)]

  return rc,ObjVal(s),packages_trucks_vector,trucks_overview

def bound_trucks(all_weights_packages,truck_weight_limit):

  nbr_trucks,total_weights = 1,0 #min we have one truck
  for i in range(len(all_weights_packages)):
    if total_weights+all_weights_packages[i] < truck_weight_limit: #if all weight don't bypass truck limit weight that mean that we need just 'one truck'
      total_weights += all_weights_packages[i]
    else:
      total_weights = all_weights_packages[i]
      nbr_trucks = nbr_trucks+1  #else we will start counting how many trucks we will need

  return nbr_trucks,ceil(sum(all_weights_packages)/truck_weight_limit) #Return the ceiling of x as a float, the smallest integer value greater than or equal to x.



def main():
    types_packages = 3

    if len(sys.argv) <= 1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))

    packages,truck_weight_limit = data_model(types_packages)

    if sys.argv[1] == 'data':

        T=tableutils.wrapmat(packages,[str(i) for i in range(types_packages)],['','nb of packages','Unit weight'])
        T.insert(0,['','Truck weight limit',truck_weight_limit])
        T.append(['Total',sum(e[0] for e in packages), sum(e[0]*e[1] for e in packages)])
        tableutils.printmat(T,True)
        w = [e for sub in [[d[1]] * d[0] for d in packages] for e in sub]
        print(w,sum(w),len(w),truck_weight_limit)
    elif sys.argv[1] in ['run', 'run0', 'nrun', 'nrun0']:

        start = time.time()

        if sys.argv[1] in ['nrun', 'nrun0']:
            rc,Val,packages_trucks_vector,trucks_overview=solve_model(packages,truck_weight_limit,False)
        else:
            rc,Val,packages_trucks_vector,trucks_overview=solve_model(packages,truck_weight_limit,True)

        end = time.time()
        #print 'Elapsed time ', end-start, ' optimal value ', Val

        if rc != 0:
            print('Infeasible')
        else:
            if sys.argv[1] in ['run', 'nrun']:
                w = sum(e[2] for row in trucks_overview for e in row[1] )
                t = sum(1 for row in trucks_overview for e in row[1] if len(row)>0)
                print('Trucks {0}, Packages {2} ({1})'.format(Val,w,t))
                print('(id weight), (id weight)*')
                for row in trucks_overview:
                    if (len(row[1])):
                        print('{0:2} ({2}),"{1}"'.format(row[0],row[1],sum(e[2] for e in row[1])))
            else:
                print('Weight, Truck id')
                for row in packages_trucks_vector:
                    print('{0},"{1}"'.format(row[0],row[1]))

if __name__ == '__main__':

    sys.argv.append('run')
    main()


