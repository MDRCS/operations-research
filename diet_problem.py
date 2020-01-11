from ortools.linear_solver import pywraplp
from libs.ortools_lib import  ObjVal, newSolver,Simple_SolVal


" N is a multi-dimensional array that have :" \
"Each row represents a food, except that the last two rows represent the minimum and maximum requirement of each nutrient" \
" nutrients are represented by the columns, with the last three representing the minimum, maximum, and the cost of each food serving. "

" The problem that we want to solve is how much of each food [1,2,3,4,5] we will give to each military, with the minimum invested cost so that they can stay healthy "

def solve_diet(N):
  s = newSolver('Diet')  #give a name to the solver 'diet', integer = False that mean that the problem that we are going to solve is a Linear problem

  " Getting Indexes for Each Variable "

  nbF,nbN = len(N)-2, len(N[0])-3 #nbF = foods = len(N)-2 /* Columns  */       nbN = Nutritions = len(N[0]) - 3  /* Rows  */

  FMin,FMax,FCost,NMin,NMax = nbN,nbN+1,nbN+2,nbF,nbF+1 #FMin = nbN -> how much of food1 we could have generated value between boundaries [lb,ub] /* Rows  */  ...

  " Initialization "

  f = [s.NumVar(N[i][FMin], N[i][FMax],'') for i in range(nbF)] #Each case gonna be a number between this interval [lowerbound, upperbound] -> Boundaries for food

  for j in range(nbN): #number of nutritions

      " Constraints "

      # Min for each Nutrition column <= sum(Number_generated_boundaries_For_food[i] * N[i][j] )
      # served number of the i eme food (value -> [lowerbound, upperbound]) * Nutrition value (N1,N2 ..)
      s.Add(N[NMin][j]<=s.Sum([f[i]*N[i][j] for i in range(nbF)]))
      # sum(Number_generated_boundaries_For_food[i] * N[i][j] ) <= Max for each Nutrition column
      # served number of the i eme food (value -> [lowerbound, upperbound]) * Nutrition value (N1,N2 ..)
      s.Add(s.Sum([f[i]*N[i][j] for i in range(nbF)])<=N[NMax][j])

  # served number of the i eme food ->  food[i] * N[i][FCost] <- Cost of each i eme food
  s.Minimize(s.Sum([f[i]*N[i][FCost] for i in range(nbF)]))
  rc = s.Solve()

  # f is a list of values, of how much of each food [1,2,3,4,5] we are going to serve
  print(Simple_SolVal(f),'Number of serving food for each food [1,2,3,4,5]')

  " So here, the functionning of the solver is clear, the model that we put in the solver will try for each iteration minimize the number of serving for each food " \
  "while respecting the constraints"

  #to make sure that the values gettinng from the model giving The objective value we should replace this values on the model .

  foods_values = Simple_SolVal(f)
  objval = [N[i][FCost] * foods_values[i] for i in range(nbF)]
  print(objval == ObjVal(s))
  print('Objectif Value : -> ', ObjVal(s))

  return rc,ObjVal(s),Simple_SolVal(f)

" gen_diet_probelm is a function that genrate the data for our model -> is not the most important thing  "

def gen_diet_problem(nb_foods=5, nb_nutrients=4):

    from random import randint,uniform
    data = []
    ranges = [10**randint(2,4) for i in range(nb_nutrients)]
    x = [randint(15,25) for i in range(nb_foods)] # this must be feasible
    MinNutrient = [0]*nb_nutrients
    MaxNutrient = [0]*nb_nutrients

    " Making data for Foods, Nutritients, minmax_foods, Costs"

    for food in range(nb_foods):
        nutrients = [randint(10,ranges[i]) for i in range(nb_nutrients)]
        minmax = [randint(0,x[food]),randint(x[food],2*x[food])]
        cost = round(100*uniform(0,10))/100
        v = nutrients + minmax + [cost]
        data.append(v)

    for j in range(nb_nutrients):
        b = sum([x[i]*data[i][j] for i in range(nb_foods)])
        MinNutrient[j] = randint(0,b)
        MaxNutrient[j] = randint(b, 2*b)
    data.append(MinNutrient+['','','',''])
    data.append(MaxNutrient+['','','',''])

    return data



if __name__ == '__main__':

    N = gen_diet_problem()
    print(N,'-> data')
    print(solve_diet(N))

