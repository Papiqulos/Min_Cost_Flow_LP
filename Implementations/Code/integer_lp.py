import gurobipy as gp
from gurobipy import GRB
import time


def min_cost_flow_ilp(nodes, edges, cost, capacity, supply):
    start_time = time.time()

    # Suppress output
    env = gp.Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    model = gp.Model(env=env)

    ## Ορισμός μεταβλητών απόφασης
    f = model.addVars(nodes, nodes, vtype=GRB.INTEGER, name='f')

    ## Περιορισμοί για διατήρηση ροής
    for i in nodes:
        model.addConstr(gp.quicksum(f[i,j] for (x,j) in edges if x == i) -
                        gp.quicksum(f[j,i] for (j,x) in edges if x == i)
                    == supply[i])

    ## Περιορισμοί για τη ροή σε κάθε ακμή
    # Χωρητικότητα ακμών
    for (i,j) in edges:
        model.addConstr(f[i,j] <= capacity[i,j])

    # Θετικότητα ροής
    for (i,j) in edges:
        model.addConstr(f[i,j] >= 0)
        
    ## Αντικειμενική συνάρτηση
    model.setObjective(gp.quicksum(cost[i,j] * f[i,j] for (i,j) in edges), GRB.MINIMIZE)

    # Επίλυση
    model.optimize()

    end_time = time.time()

    diff = time.gmtime(end_time - start_time)
    print('\n[Total time used: {} minutes, {} seconds]'.format(diff.tm_min, diff.tm_sec))

    # Εκτύπωση αποτελεσμάτων
    try:
        print(f'\nObjective value found: {model.objVal}')
    except AttributeError as e:
        print(f'\nCould not find an objective value. \nTraceback:\n\t{e}')


    # Βέλτιστη ροή ανά ακμή
    for (i,j) in edges:
        print('f[{},{}] = {}'.format(
            i, j, f[i,j].x
        ))



if __name__ == '__main__':
    # Input Data
    
    # Example_1
    '''
    MIN Z = x1 + 4x2 + 2x3 + 8x4
    subject to
    x1 + x2 = 5
    -x1 + -x3 = -6
    x3 + x4 = 3
    -x2 + x4 = -2
    x1 <= 5
    x2 <= 2
    x3 <= 3
    x4 <= 2
    and x1,x2,x3,x4 >= 0 
    '''
    nodes1 = range(4)

    edges1 = [(0,1), (0,3), (2,1), (2,3)]

    # cost[i,j] is the cost of sending one unit of flow along edge (i,j)
    cost1 = {
    (0,1) : 0,
    (0,3) : 4,
    (2,1) : 2,
    (2,3) : 8
    } 

    # capacity[i,j] is the capacity of edge (i,j)
    capacity1 = {
    (0,1) : 5,
    (0,3) : 2,
    (2,1) : 3,
    (2,3) : 2
    }

    # supply[i] is the supply (if positive) or demand (if negative) of node i
    supply1 = [5, -6, 3, -2]


    # Example_2 
    nodes2 = range(5)

    edges2 = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4), (4,2)]

    cost2 = {
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

    capacity2 = {
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

    supply2 = [20, 0, 0, -5, -15]

    print("-----------------------------Example_1-----------------------------")
    min_cost_flow_ilp(nodes1, edges1, cost1, capacity1, supply1)

    print("\n-----------------------------Example_2-----------------------------")
    min_cost_flow_ilp(nodes2, edges2, cost2, capacity2, supply2)