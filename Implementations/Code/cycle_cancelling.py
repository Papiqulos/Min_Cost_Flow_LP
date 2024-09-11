"""From Bradley, Hax and Maganti, 'Applied Mathematical Programming', figure 8.1."""
import numpy as np
from ortools.graph.python import min_cost_flow


def min_cost_flow_cc(start_nodes, end_nodes, capacities, unit_costs, supplies):
    """MinCostFlow simple interface example."""
    # Instantiate a SimpleMinCostFlow solver.
    smcf = min_cost_flow.SimpleMinCostFlow()

    # Add arcs, capacities and costs in bulk using numpy.
    all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
        start_nodes, end_nodes, capacities, unit_costs
    )

    # Add supply for each nodes.
    smcf.set_nodes_supplies(np.arange(0, len(supplies)), supplies)

    # Find the min cost flow.
    status = smcf.solve()

    if status != smcf.OPTIMAL:
        print("There was an issue with the min cost flow input.")
        print(f"Status: {status}")
        exit(1)
    print(f"Minimum cost: {smcf.optimal_cost()}")
    print("")
    print(" Arc    Flow / Capacity Cost")
    solution_flows = smcf.flows(all_arcs)
    costs = solution_flows * unit_costs
    for arc, flow, cost in zip(all_arcs, solution_flows, costs):
        print(
            f"{smcf.tail(arc):1} -> {smcf.head(arc)}  {flow:3}  / {smcf.capacity(arc):3}       {cost}"
        )


if __name__ == "__main__":
    

    # Example_1
    start_nodes1 = np.array([0, 0, 2, 2])
    end_nodes1 = np.array([1, 3, 1, 3])
    capacities1 = np.array([5, 2, 3, 2])
    unit_costs1 = np.array([1, 4, 2, 8])
    supplies1 = [5, -6, 3, -2]

    # Example_2
    start_nodes2 = np.array([0, 0, 1, 1, 1, 2, 2, 3, 4])
    end_nodes2 = np.array([1, 2, 2, 3, 4, 3, 4, 4, 2])
    capacities2 = np.array([15, 8, 20, 4, 10, 15, 4, 20, 5])
    unit_costs2 = np.array([4, 4, 2, 2, 6, 1, 3, 2, 3])
    supplies2 = [20, 0, 0, -5, -15]

    print("-----------------------------Example_1-----------------------------")
    min_cost_flow_cc(start_nodes1, end_nodes1, capacities1, unit_costs1, supplies1)

    print("-----------------------------Example_2-----------------------------")
    min_cost_flow_cc(start_nodes2, end_nodes2, capacities2, unit_costs2, supplies2)