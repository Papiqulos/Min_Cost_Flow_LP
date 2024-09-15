import gurobipy as gp
from gurobipy import GRB
import time
from examples import example1, example2, example3


def min_cost_flow_ilp(nodes, edges, cost, capacity, supply):
    start_time = time.time()

    # Suppress output
    env = gp.Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    model = gp.Model(env=env)

    ## Ορισμός μεταβλητών απόφασης
    f = model.addVars(nodes, nodes, vtype=GRB.INTEGER, name='f')  
    # print(f'Variables: {f} \n') 

    ## Περιορισμοί για διατήρηση ροής
    for i in nodes:
        model.addConstr(gp.quicksum(f[i,j] for (x,j) in edges if x == i) -
                        gp.quicksum(f[j,i] for (j,x) in edges if x == i)
                    == supply[i])

    ## Περιορισμοί για τη ροή σε κάθε ακμή
    # Χωρητικότητα ακμών
    for (i,j) in edges:
        print(f'Capacity: {capacity[i,j]}')
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
        
        # Βέλτιστη ροή ανά ακμή
        for (i,j) in edges:
            print('f[{},{}] = {}'.format(
                i, j, f[i,j].x
            ))
    except AttributeError as e:
        print(f'\nCould not find an objective value. \nTraceback:\n\t{e}')

def min_cost_flow_ilp_factory(nodes, edges, cost, capacity, capacity1, demand, plants_n, warehouses_n, customers_n, x, y, z):
    start_time = time.time()

    # Suppress output
    env = gp.Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    model = gp.Model(env=env)

    ## Ορισμός μεταβλητών απόφασης
    f = model.addVars(nodes, nodes, vtype=GRB.INTEGER, name='f')  

    for a in plants_n:
        model.addConstr(gp.quicksum(f[i,j] for (i, j) in x if i == a) + gp.quicksum(f[i,k] for (i, k) in y if i == a) <= capacity[a])
        
    for w in warehouses_n:
        model.addConstr(gp.quicksum(f[i,j] for (i, j) in x if j == w) <= capacity1[w])
        
    for w in warehouses_n:
        model.addConstr(gp.quicksum(f[j,k] for (j, k) in z if j == w) == gp.quicksum(f[i,j] for (i, j) in x if j == w))
    
    for d in customers_n:
        model.addConstr(gp.quicksum(f[i,k] for (i, k) in y if k == d) + gp.quicksum(f[j,k] for (j, k) in z if k == d) == demand[d])
    
    ## Αντικειμενική συνάρτηση
    model.setObjective(gp.quicksum(cost[i,j] * f[i,j] for (i,j) in edges if cost[i,j]), GRB.MINIMIZE)

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
    # nodes1, edges1, cost1, capacity1, supply1 = example1()
    # nodes2, edges2, cost2, capacity2, supply2 = example2()
    # nodes3, edges3, cost3, capacity3, supply3 = example3()

    # print("-----------------------------Example_1-----------------------------")
    # min_cost_flow_ilp(*example1())

    # print("\n-----------------------------Example_2-----------------------------")
    # min_cost_flow_ilp(*example2())

    print("\n-----------------------------Example_3-----------------------------")
    min_cost_flow_ilp_factory(*example3())