

def example1():
    # Example_1
    '''
    MIN Z = 0x1 + 4x2 + 2x3 + 8x4
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

def example3(graph:bool = False, 
             crown:bool = True,
             num_plants:int = 2, 
             num_warehouses:int = 4, 
             num_customers:int = 6, 
             costs_pw:list = [
                            [0.5, None],  # W1 (Costs for P1, P2)
                            [0.5, 0.3],   # W2
                            [1.0, 0.5],   # W3
                            [0.2, 0.2],   # W4
                            ], 
             costs_pc:list = [
                            [1.0, 2.0],   # C1 (Costs for P1, P2)
                            [None, None], # C2
                            [1.5, None],  # C3
                            [2.0, None],  # C4
                            [None, None], # C5
                            [1.0, None]   # C6
                            ], 
             costs_wc:list = [
                            [None, 1.0, None, None],    # C1 (Costs for W1, W2, W3, W4)
                            [1.5, 0.5, 1.5, None],      # C2
                            [0.5, 0.5, 2.0, 0.2],       # C3
                            [1.5, 1.0, None, 1.5],      # C4
                            [None, 0.5, 0.5, 0.5],      # C5
                            [1.0, None, 1.5, 1.5]       # C6
                            ] , 
             capacities_plants:list = [150_000, 200_000], 
             throughputs_warehouses:list = [70_000, 50_000, 100_000, 40_000], 
             demands_customers:list = [50_000, 10_000, 40_000, 35_000, 60_000, 20_000]) -> tuple:
    """Example 3 (Crown distributors company is the default) or any other example with the same structure.
    Args:
        graph (bool, optional): If True, the function returns the graph. Defaults to False.
        crown (bool, optional): If True, the example is Crown distributors company. Defaults to True.
        num_plants (int, optional): Number of plants. 
        num_warehouses (int, optional): Number of warehouses. 
        num_customers (int, optional): Number of customers. 
        costs_pw (list, optional): Costs from plants to warehouses.
        costs_pc (list, optional): Costs from plants to customers.
        costs_wc (list, optional): Costs from warehouses to customers.
        capacities_plants (list, optional): Capacities of plants.
        throughputs_warehouses (list, optional): Throughputs of warehouses.
        demands_customers (list, optional): Demands of customers
    
    Returns:
        tuple: A tuple containing the graph's nodes, edges, costs, capacities, throughputs, demands, plants_n, warehouses_n, customers_n, plants_to_warehouses, plants_to_customers, warehouses_to_customers
    """
    # Example 3 (Crown distributors company)
    ##
    plants = range(num_plants)
    plants_n = [f"p{i+1}" for i in plants]

    ##
    warehouses = range(num_warehouses)
    warehouses_n = [f"w{j+1}" for j in warehouses]

    ##
    customers = range(num_customers)
    customers_n = [f"c{k+1}" for k in customers]
    
    # Nodes
    nodes = plants_n + warehouses_n + customers_n

    # Edges (Decision variables)
    plants_to_warehouses = [(f"p{i+1}", f"w{j+1}") for i in plants for j in warehouses]         # x_ij
    plants_to_customers = [(f"p{i+1}", f"c{k+1}") for i in plants for k in customers]           # y_ik
    warehouses_to_customers = [(f"w{j+1}", f"c{k+1}") for j in warehouses for k in customers]   # z_jk
    edges = plants_to_warehouses + plants_to_customers + warehouses_to_customers              

    # Mapping costs to edges
    cost3_1 = {(f"p{i+1}", f"w{j+1}"): costs_pw[j][i] for i in plants for j in warehouses}     # c_ij
    cost3_2 = {(f"p{i+1}", f"c{k+1}"): costs_pc[k][i] for i in plants for k in customers}      # d_ik
    cost3_3 = {(f"w{j+1}", f"c{k+1}"): costs_wc[k][j] for j in warehouses for k in customers}  # e_jk

    # Merging costs
    costs = {**cost3_1, **cost3_2, **cost3_3}

    # Remove the edges with None costs
    plants_to_warehouses = [edge for edge in plants_to_warehouses if costs[edge] is not None]
    plants_to_customers = [edge for edge in plants_to_customers if costs[edge] is not None]
    warehouses_to_customers = [edge for edge in warehouses_to_customers if costs[edge] is not None]
    edges = [edge for edge in edges if costs[edge] is not None]

    ## Capacities of plants
    # Mapping capacities to plants
    capacities = {f"p{i+1}": capacities_plants[i] for i in plants}

    ## Throughput of warehouses
    # Mapping throughputs to warehouses
    throughputs = {f"w{j+1}": throughputs_warehouses[j] for j in warehouses}

    ## Demand of customers
    # Mapping demands to customers
    demands = {f"c{k+1}": demands_customers[k] for k in customers}

    if graph:
        capacity3_1 = {(f"p{i+1}", f"w{j+1}"): min(capacities_plants[i], throughputs_warehouses[j]) for i in plants for j in warehouses}
        capacity3_2 = {(f"p{i+1}", f"c{k+1}"): min(capacities_plants[i], demands_customers[k]) for i in plants for k in customers}
        capacity3_3 = {(f"w{j+1}", f"c{k+1}"): min(throughputs_warehouses[j], demands_customers[k]) for j in warehouses for k in customers}

        capacities = {**capacity3_1, **capacity3_2, **capacity3_3}

        supplies = capacities_plants + [0] * len(warehouses) + [-demand for demand in demands_customers]
    
        supplies = {node: supplies[i] for i, node in enumerate(nodes)}
        excess = sum(supplies.values())

        # Balance the supply and demand by adding a dummy node if there is an excess supply
        if excess != 0:
            
            # Add a dummy node
            nodes.append('dummy')

            # Give the dummy node the excess supply as demand
            supplies['dummy'] = -excess

            if num_plants == 1:
                # Connect the dummy node to the plant
                edges.append(('p1', 'dummy'))

                # Set the cost of the edge from the plant to the dummy node to 0
                costs['p1', 'dummy'] = 0

                capacities['p1', 'dummy'] = excess
            else:
                # Connect the dummy node to the first two plants
                edges.append(('p1', 'dummy'))
                edges.append(('p2', 'dummy'))

                # Set the costs of the edges from the plants to the dummy node to 0
                costs['p1', 'dummy'], costs['p2', 'dummy'] = 0, 0
            
                # Distribute the excess supply to the dummy node from the plants
                # This distribution is arbitrary and can be changed and yields different results for different distributions
                # This distribution is based on the capacities of the plants (Higher capacity plant, higher distribution from the plant to the dummy node)
                if crown:
                    # This distribution yields the same result as non-graph implementation for the Crown distributors company
                    capacities['p1', 'dummy'], capacities['p2', 'dummy'] = 80_000, 55_000
                else:
                    # Arbitrary distribution for any other example
                    capacities['p1', 'dummy'], capacities['p2', 'dummy'] = excess // 2, excess - (excess // 2)
        
        return nodes, edges, costs, capacities, supplies
    else:
        return nodes, edges, costs, capacities, throughputs, demands, plants_n, warehouses_n, customers_n, plants_to_warehouses, plants_to_customers, warehouses_to_customers





