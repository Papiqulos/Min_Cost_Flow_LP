def example1():
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
    supply1 = {node: supply1[i] for i, node in enumerate(nodes1)}

    return nodes1, edges1, cost1, capacity1, supply1

def example2():
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

    supply2 = {node: supply2[i] for i, node in enumerate(nodes2)}

    return nodes2, edges2, cost2, capacity2, supply2

def example3():
    # Example 3 (Crown distributors company)
    plants = range(2)
    plants_n = [f"p{i+1}" for i in plants]

    warehouses = range(4)
    warehouses_n = [f"w{j+1}" for j in warehouses]

    customers = range(6)
    customers_n = [f"c{k+1}" for k in customers]
    
    # Nodes
    nodes3 = plants_n + warehouses_n + customers_n

    # Edges (Decision variables)
    plants_to_warehouses = [(f"p{i+1}", f"w{j+1}") for i in plants for j in warehouses]
    x = [(f"p{i+1}", f"w{j+1}") for i in plants for j in warehouses]

    plants_to_customers = [(f"p{i+1}", f"c{k+1}") for i in plants for k in customers]
    y = [(f"p{i+1}", f"c{k+1}") for i in plants for k in customers]

    warehouses_to_customers = [(f"w{j+1}", f"c{k+1}") for j in warehouses for k in customers]
    z = [(f"w{j+1}", f"c{k+1}") for j in warehouses for k in customers]
    
    edges3 = plants_to_warehouses + plants_to_customers + warehouses_to_customers
    

    # Plant to warehouse costs
    costs_pw = [
    [0.5, None],  # W1 (Costs for P1, P2)
    [0.5, 0.3],   # W2
    [1.0, 0.5],   # W3
    [0.2, 0.2],   # W4
    ]

    # Plant to customer costs
    costs_pc = [
        [1.0, 2.0],   # C1 (Costs for P1, P2)
        [None, None], # C2
        [1.5, None],  # C3
        [2.0, None],  # C4
        [None, None], # C5
        [1.0, None]   # C6
    ]

    # Warehouse to customer costs
    costs_wc = [
    [None, 1.0, None, None],    # C1 (Costs for W1, W2, W3, W4)
    [1.5, 0.5, 1.5, None],      # C2
    [0.5, 0.5, 2.0, 0.2],       # C3
    [1.5, 1.0, None, 1.5],      # C4
    [None, 0.5, 0.5, 0.5],      # C5
    [1.0, None, 1.5, 1.5]       # C6
    ]               

    # Mapping costs to edges
    cost3_1 = {(f"p{i+1}", f"w{j+1}"): costs_pw[j][i] for i in plants for j in warehouses}
    cost3_2 = {(f"p{i+1}", f"c{k+1}"): costs_pc[k][i] for i in plants for k in customers}
    cost3_3 = {(f"w{j+1}", f"c{k+1}"): costs_wc[k][j] for j in warehouses for k in customers}

    # Merging costs
    cost3 = {**cost3_1, **cost3_2, **cost3_3}

    # Remove the edges with None costs
    edges3 = [edge for edge in edges3 if cost3[edge] is not None]
    x = [edge for edge in x if cost3[edge] is not None]
    y = [edge for edge in y if cost3[edge] is not None]
    z = [edge for edge in z if cost3[edge] is not None]
    # print(edges3)

    # Capacities of plants
    capacities_plants = [150_000, 200_000]
    capacity = {f"p{i+1}": capacities_plants[i] for i in plants}

    # Throughput of warehouses
    throughput_warehouses = [70_000, 50_000, 100_000, 40_000]
    capacity1 = {f"w{j+1}": throughput_warehouses[j] for j in warehouses}

    # Demand of customers
    demand_customers = [50_000, 10_000, 40_000, 35_000, 60_000, 20_000]
    demand = {f"c{k+1}": demand_customers[k] for k in customers}
    
    
    # capacity3_1 = {(f"p{i+1}", f"w{j+1}"): min(capacities_plants[i], throughput_warehouses[j]) for i in plants for j in warehouses}
    # capacity3_2 = {(f"p{i+1}", f"c{k+1}"): min(capacities_plants[i], demand_customers[k]) for i in plants for k in customers}
    # capacity3_3 = {(f"w{j+1}", f"c{k+1}"): min(throughput_warehouses[j], demand_customers[k]) for j in warehouses for k in customers}

    # capacity3 = {**capacity3_1, **capacity3_2, **capacity3_3}
    
    
    # supply3 = capacities_plants + [0] * len(warehouses) + [-demand for demand in demand_customers]

    # supply3 = {node: supply3[i] for i, node in enumerate(nodes3)}

    return nodes3, edges3, cost3, capacity, capacity1, demand, plants_n, warehouses_n, customers_n, x, y, z





