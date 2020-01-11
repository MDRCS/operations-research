from ortools.linear_solver import pywraplp
from libs.ortools_lib import ObjVal, Simple_SolVal, newSolver
from random import randint

def data_model(tasks = 12):

    Tasks = []

    for i in range(tasks):
        Task = [i]
        Task.append(randint(2,8))
        Precedents = []
        for j in range(i):
            if randint(0,1) * randint(0,1):
                Precedents.append(j)
        Task.append(Precedents)
        Tasks.append(Task)

    return Tasks


def project_management_solver(Tasks):

    s = newSolver(' Project Management ')
    length = len(Tasks)
    total_duration = sum([Tasks[i][1] for i in range(length)])
    t = [s.NumVar(0,total_duration,'t[%i]' % i) for i in range(length)]
    Total = s.NumVar(0,total_duration,'Total')

    for i in range(length):
        s.Add(t[i] + Tasks[i][1] <= Total)
        for j in Tasks[i][2]: #Loop on precedents
            s.Add(t[j] + Tasks[j][1] <= t[i])

    s.Minimize(Total)
    rc = s.Solve()

    return Simple_SolVal(Total),Simple_SolVal(t)


if __name__ == '__main__':

    tasks_planning = data_model()

    total_project_duration, durations = project_management_solver(tasks_planning)

    print('Total duration : ',total_project_duration)
    print('Durations for each Task : ',durations)