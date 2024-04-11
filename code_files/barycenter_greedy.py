import argparse
import random

def create_sol(filepath,outputpath):
    nb_dic={}
    parameter=[]
    with open(filepath, 'r') as file:
        i=0
        for line in file:
            x=line.strip().split()
            if i==0:
                parameter.append(int(x[2]))
                parameter.append(int(x[3]))
                parameter.append(int(x[4]))
            else:
                a=int(x[0])
                b=int(x[1])
                if b not in nb_dic.keys():
                    nb_dic[b]=[a]
                else:
                    nb_dic[b].append(a)
            i+=1
    n0=parameter[0];n1=parameter[1];m=parameter[2]
    for i in range(n0+1, n0+n1+1):
        if (i not in nb_dic.keys()):
            nb_dic[i] = []
        nb_dic[i] = sorted(nb_dic[i])


    def barycenter():
        bary = sorted([[sum(nb_dic[i]) / len(nb_dic[i]) if len(nb_dic[i]) != 0 else 0, i] for i in range(n0+1, n0+n1+1)])
        order = [bary[i][1] for i in range(n1)]
        return order
        
    def good_swap(v,u):
        nb_v=nb_dic[v]
        nb_u=nb_dic[u]
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

    def greedy(order):
        swap = 1
        while swap:
            swap = 0
            for i in range(n1-1):
                if good_swap(order[i], order[i+1]):
                    order[i], order[i+1] = order[i+1], order[i]
                    swap+=1
        return order

    orderedls = barycenter()
    orderedls = greedy(orderedls)

    with open(outputpath, 'w') as file:
        for item in orderedls:
            file.write(f"{item}\n")
            
def main(parameters):
    inputpath=parameters[0]
    outputpath=parameters[1]
    create_sol(inputpath,outputpath)


if __name__ == "__main__":
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description="Process parameters without specified names.")
    
    # Add positional arguments
    parser.add_argument("parameters", nargs='+', help="List of parameters")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call main function with extracted arguments
    main(args.parameters)