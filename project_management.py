import sys
from libs.ortools_lib import ObjVal, Simple_SolVal, newSolver
from random import randint,random
from libs import tableutils


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

    return rc,Simple_SolVal(Total),Simple_SolVal(t)


def main():

    tasks = 12
    if len(sys.argv) <= 1:
        print('Usage is main [data|run] [seed]')
        return
    # elif len(sys.argv) >= 3:
    #     random.seed(int(sys.argv[2]))

    tasks_planning = data_model()

    if sys.argv[1] == 'data':
        planning = []
        for i in range(tasks):
            task = [tasks_planning[i][0], tasks_planning[i][1]]
            s = '{'
            for j in tasks_planning[i][2]:
                s = s + ' ' + str(j)
            s = s + ' }'
            task.append(s)
            planning.append(task)
        planning.insert(0, ['Task', 'Duration', 'Preceding tasks'])
        tableutils.printmat(planning, True)

    elif sys.argv[1] == 'run':
        feasablity,total_project_duration, durations  = project_management_solver(tasks_planning)
        schedule = []
        tasks_ = ['Tasks'] + [tasks_planning[i][0] for i in range(tasks)]
        schedule.append(tasks_)
        starts_ = ['Start'] + [int(durations[i]) for i in range(tasks)]
        schedule.append(starts_)
        ends_ = ['End'] + [int(durations[i] + tasks_planning[i][1]) for i in range(tasks)]
        schedule.append(ends_)
        tableutils.printmat(schedule, True)

if __name__ == '__main__':
    sys.argv.append('run')
    main()

