import gurobipy as gp
from gurobipy import GRB
import time




# Input Data
# Example_0
nodes = range(5)

edges = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4), (4,2)]

cost = {
    (0,1) : 4,
    (0,2) : 4,
    (1,2) : 2,
    (1,3) : 2,
    (1,4) : 6,
    (2,3) : 1,
    (2,4) : 3,
    (3,4) : 2,
    (4,2) : 3
}

capacity = {
    (0,1) : 15,
    (0,2) : 8,
    (1,2) : 20,
    (1,3) : 4,
    (1,4) : 10,
    (2,3) : 15,
    (2,4) : 4,
    (3,4) : 20,
    (4,2) : 5
}

supply = [20, 0, 0, -5, -15]

# Example_1
# nodes = range(4)

# edges = [(0,1), (0,3), (2,1), (2,3)]

# # cost[i,j] is the cost of sending one unit of flow along edge (i,j)
# cost = {
#     (0,1) : 0,
#     (0,3) : 4,
#     (2,1) : 2,
#     (2,3) : 8
# } 

# # capacity[i,j] is the capacity of edge (i,j)
# capacity = {
#     (0,1) : 5,
#     (0,3) : 2,
#     (2,1) : 3,
#     (2,3) : 2
# }

# # supply[i] is the supply (if positive) or demand (if negative) of node i
# supply = [5, -6, 3, -2]



def main():
    start_time = time.time()

    model = gp.Model()

    # set output level to max
    model.Params.TuneOutput = 3

    # add variable f
    f = model.addVars(nodes, nodes, vtype=GRB.CONTINUOUS, name='f')

    # add constraint representing supply/demand
    for i in nodes:
        model.addConstr(gp.quicksum(f[i,j] for (x,j) in edges if x == i) -
                        gp.quicksum(f[j,i] for (j,x) in edges if x == i)
                    == supply[i])

    # add constraint on edge flows w.r.t. capacities
    for (i,j) in edges:
        model.addConstr(f[i,j] <= capacity[i,j])

    # add constraint on edge flows w.r.t. 0
    for (i,j) in edges:
        model.addConstr(f[i,j] >= 0)
        
    # set objective
    model.setObjective(gp.quicksum(cost[i,j] * f[i,j] for (i,j) in edges), GRB.MINIMIZE)

    model.optimize()

    end_time = time.time()

    diff = time.gmtime(end_time - start_time)
    print('\n[Total time used: {} minutes, {} seconds]'.format(diff.tm_min, diff.tm_sec))

    try:
        print(f'\nObjective value found: {model.objVal}')
    except AttributeError as e:
        print(f'\nCould not find an objective value. \nTraceback:\n\t{e}')


    # optimal solution
    for (i,j) in edges:
        print('f[{},{}] = {}'.format(
            i, j, f[i,j].x
        ))


if __name__ == '__main__':
    main()