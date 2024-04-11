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
    def barycenter():
        bary = sorted([[sum(nb_dic[i]) / len(nb_dic[i]) if i in nb_dic.keys() else 0, i] for i in range(n0+1, n0+n1+1)])
        order = [bary[i][1] for i in range(n1)]
        return order
    
    orderedls = barycenter()

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