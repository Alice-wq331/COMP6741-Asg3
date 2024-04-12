import sys
from sage.graphs.graph import Graph
from sage.all import *

# read the graph file
def read_gr_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    edges = []
    A_size = 0
    B_size = 0
    A_vertices = []
    B_vertices = []
    
    for line in lines:
        if line.startswith('c'):  # ignore commentline
            continue
        elif line.startswith('p'):  # analyze p line
            parts = line.split()
            A_size = int(parts[2])
            B_size = int(parts[3])
            A_vertices = list(range(1, A_size + 1))
            B_vertices = list(range(A_size + 1, A_size + B_size + 1))
        else:  #analyze edges
            parts = line.split()
            edge = (int(parts[0]), int(parts[1]))
            edges.append(edge)
    
    return A_vertices, B_vertices, edges


def calculate_crossings(edges, order_a, order_b):
 
    # mapping the order of vertices in A,B to x coordinate
    pos_a = {vertex: idx for idx, vertex in enumerate(order_a)}
    pos_b = {vertex: idx for idx, vertex in enumerate(order_b)}
    
    crossings = 0
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            # check crossings
            a1, b1 = edges[i]
            a2, b2 = edges[j]
            # corssing count if there is inverse order
            if (pos_a[a1] < pos_a[a2] and pos_b[b1] > pos_b[b2]) or \
               (pos_a[a1] > pos_a[a2] and pos_b[b1] < pos_b[b2]):
                crossings += 1
    return crossings

def median_heuristic(G, A, B):
    #  median
    median_values = {}
    for u in B:
        neighbors = G.neighbors(u)
        neighbor_positions = [A.index(v) for v in neighbors if v in A]
        if neighbor_positions:
            #calculating median
            median_values[u] = sorted(neighbor_positions)[len(neighbor_positions) // 2]
        else:
            # no neighbors
            median_values[u] = 0

    # sort B according to the medians and their parity
    sorted_B = sorted(B, key=lambda u: (median_values[u], G.degree(u) % 2 == 0))

    # Return B
    return sorted_B


def greedy_switch(edges, A, B):
    
    improved = True
    while improved:
        improved = False
        for i in range(len(B) - 1):
            # 
            current_crossings = calculate_crossings(edges, A, B)
            #
            B[i], B[i + 1] = B[i + 1], B[i]
            # 
            new_crossings = calculate_crossings(edges, A, B)
            # 
            if new_crossings >= current_crossings:
                B[i], B[i + 1] = B[i + 1], B[i]
            else:
                improved = True  # 
    return B


def build_neighbor_dict(A, B, edges):
    nb_dic = {}
    for edge in edges:
        a, b = edge
        if a not in nb_dic:
            nb_dic[a] = []
        if b not in nb_dic:
            nb_dic[b] = []
        nb_dic[a].append(b)
        nb_dic[b].append(a)
    return nb_dic


def calculate_specific_crossings(u, v, G, orderA, orderB, index_u, index_v):
    #
    crossings = 0
  
    for a in orderA:
        if a in G.neighbors(u) and a in G.neighbors(v):
            index_a = orderA.index(a)
            #
            if (index_a < index_u and index_a > index_v) or (index_a > index_u and index_a < index_v):
                crossings += 1
    return crossings


def build_neighbor_dict(A, B, edges):
    nb_dic = {}
    for edge in edges:
        a, b = edge
        if a not in nb_dic:
            nb_dic[a] = []
        if b not in nb_dic:
            nb_dic[b] = []
        nb_dic[a].append(b)
        nb_dic[b].append(a)
    return nb_dic

def good_swap(v,u, G):
    nb_v=sorted(G.neighbors(v))
    nb_u=sorted(G.neighbors(u))
    c_uv=0
    cross_nbs=0
    for a in range(len(nb_u)):
        cur_line=nb_u[a]
        c_uv+=cross_nbs
        while cross_nbs!=len(nb_v):
            if nb_v[cross_nbs]<cur_line:
                cross_nbs+=1
                c_uv+=1
            else:
                break          
    c_vu=0
    cross_nbs=0
    for a in range(len(nb_v)):
        cur_line=nb_v[a]
        c_vu+=cross_nbs
        while cross_nbs!=len(nb_u):
            if nb_u[cross_nbs]<cur_line:
                cross_nbs+=1
                c_vu+=1
            else:
                break
    if c_vu>c_uv:
        return True
    else:
        return False


def greedy_post(order, G):
    n=len(order)
    if n<=1:
        return order
    for i in range(n-1):
        j=i+1
        v=order[i]
        u=order[j]
        if good_swap(v,u, G):
            order[j]=v
            order[i]=u
    return greedy_post(order[0:n-1], G)+[order[n-1]]







def write_solution_to_file(solution_filepath, solution_order):
    
    # Convert the linear order of B into string format, with each element on a new line
    solution_data = '\n'.join(map(str, solution_order))
    
    # Write the solution data to the .sol file
    with open(solution_filepath, 'w') as solution_file:
        solution_file.write(solution_data)
    
    print(f"Solution has been written to the file: {solution_filepath}")




def main(graph_file_path, solution_file_path):
    # 
    A, B, edges = read_gr_file(graph_file_path)

    # 
    G = Graph()
    G.add_vertices(A + B)
    G.add_edges(edges)

    # 
    sorted_B = median_heuristic(G, A, B)
    optimized_B = greedy_post(sorted_B, G)  
    write_solution_to_file(solution_file_path, optimized_B)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: solver.sage input_file output_file")
        sys.exit(1)
    
    graph_file_path = sys.argv[1]
    solution_file_path = sys.argv[2]
    
    main(graph_file_path, solution_file_path)
