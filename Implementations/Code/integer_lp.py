import gurobipy as gp
from gurobipy import GRB
import time
from examples import example1, example2, example3


def min_cost_flow_ilp(nodes:list, 
                      edges:list, 
                      costs:dict, 
                      capacities:dict, 
                      supplies:dict):
    """Solves the minimum cost flow problem when given the nodes, edges, costs, capacities and supplies using Gurobi's ILP solver (for simple networks).
    
    Args:
        nodes (list): List of nodes in the network.
        edges (list): List of edges in the network.
        costs (dict): Dictionary of costs for each edge.
        capacities (dict): Dictionary of capacities for each edge.
        supplies (dict): Dictionary of supplies for each node.
        
    Returns:
        None"""
    start_time = time.time()

    ## Suppress output
    env = gp.Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    model = gp.Model(env=env)

    ## Define decision variables
    f = model.addVars(nodes, nodes, vtype=GRB.INTEGER, name='f')  

    ## Constraints
    # Flow conservation constraints
    for i in nodes:
        model.addConstr(gp.quicksum(f[i,j] for (x,j) in edges if x == i) -
                        gp.quicksum(f[j,i] for (j,x) in edges if x == i)
                    == supplies[i])

    # Capacity constraints
    for (i,j) in edges:
        model.addConstr(f[i,j] <= capacities[i,j])

    # All flows are non-negative
    for (i,j) in edges:
        model.addConstr(f[i,j] >= 0)
        
    ## Objective Function
    model.setObjective(gp.quicksum(costs[i,j] * f[i,j] for (i,j) in edges), GRB.MINIMIZE)

    ## Solve
    model.optimize()

    end_time = time.time()

    diff = time.gmtime(end_time - start_time)
    print('\n[Total time used: {} minutes, {} seconds]'.format(diff.tm_min, diff.tm_sec))

    ## Output results
    try:
        print(f'\nObjective value found: {model.objVal}')
        
        # Optimal edge flows
        for (i,j) in edges:
            print('f[{},{}] = {}'.format(
                i, j, f[i,j].x
            ))
    except AttributeError as e:
        print(f'\nCould not find an objective value. \nTraceback:\n\t{e}')

def min_cost_flow_ilp_factory(nodes:list, 
                              edges:list, 
                              costs:dict,
                              capacities:dict, 
                              throughputs:dict, 
                              demands:dict, 
                              plants_n:list, 
                              warehouses_n:list, 
                              customers_n:list, 
                              plants_to_warehouses:list, 
                              plants_to_customers:list, 
                              warehouses_to_customers:list):
    """Solves the minimum cost flow problem for the Crown Distributors Company example using Gurobi's ILP solver.
    
    Args:
        nodes (list): List of nodes in the network. (plants, warehouses, customers)
        edges (list): List of edges in the network. (plants to warehouses, plants to customers, warehouses to customers)
        costs (dict): Dictionary of costs for each edge.
        capacities (dict): Dictionary of capacities for each plant.
        throughputs (dict): Dictionary of throughputs for each warehouse.
        demands (dict): Dictionary of demands for each customer.
        plants_n (list): List of plants.
        warehouses_n (list): List of warehouses.
        customers_n (list): List of customers.
        plants_to_warehouses (list): List of edges from plants to warehouses.
        plants_to_customers (list): List of edges from plants to customers.
        warehouses_to_customers (list): List of edges from warehouses to customers.
        
    Returns:
        None
    """
    start_time = time.time()

    ## Suppress output
    env = gp.Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    model = gp.Model(env=env)

    ## Define decision variables
    f = model.addVars(nodes, nodes, vtype=GRB.INTEGER, name='f')  

    ## Constraints
    # Factory Capacities
    for a in plants_n:
        model.addConstr(gp.quicksum(f[i,j] for (i, j) in plants_to_warehouses if i == a) + gp.quicksum(f[i,k] for (i, k) in plants_to_customers if i == a) <= capacities[a])
        
    # Quantity into Warehouses
    for w in warehouses_n:
        model.addConstr(gp.quicksum(f[i,j] for (i, j) in plants_to_warehouses if j == w) <= throughputs[w])
        
    # Quantity out of Warehouses
    for w in warehouses_n:
        model.addConstr(gp.quicksum(f[j,k] for (j, k) in warehouses_to_customers if j == w) == gp.quicksum(f[i,j] for (i, j) in plants_to_warehouses if j == w))
    
    # Customer Demands
    for d in customers_n:
        model.addConstr(gp.quicksum(f[i,k] for (i, k) in plants_to_customers if k == d) + gp.quicksum(f[j,k] for (j, k) in warehouses_to_customers if k == d) == demands[d])
    
    ## Objective Function
    model.setObjective(gp.quicksum(costs[i,j] * f[i,j] for (i,j) in edges if costs[i,j]), GRB.MINIMIZE)

    ## Solve
    model.optimize()

    end_time = time.time()

    diff = time.gmtime(end_time - start_time)
    print('\n[Total time used: {} minutes, {} seconds]'.format(diff.tm_min, diff.tm_sec))

    ## Output results
    try:
        print(f'\nObjective value found: {model.objVal}')
        
        # Values of the decision variables
        for (i,j) in edges:
            print('f[{},{}] = {}'.format(
                i, j, f[i,j].x
            ))
    except AttributeError as e:
        print(f'\nCould not find an objective value. \nTraceback:\n\t{e}')
    

if __name__ == '__main__':
    # Input Data
    # nodes1, edges1, cost1, capacity1, supply1 = example1()
    # nodes2, edges2, cost2, capacity2, supply2 = example2()
    # nodes3, edges3, cost3, capacity3, supply3 = example3()

    print("-----------------------------Example_1-----------------------------")
    min_cost_flow_ilp(*example1())

    print("\n-----------------------------Example_2-----------------------------")
    min_cost_flow_ilp(*example2())

    print("\n-----------------------------Example_3-----------------------------")
    min_cost_flow_ilp_factory(*example3())

    print("\n-----------------------------Example_3-----------------------------")
    min_cost_flow_ilp(*example3(graph=True))