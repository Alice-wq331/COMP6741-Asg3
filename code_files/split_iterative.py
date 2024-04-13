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
    n=parameter[0];n0=parameter[1];m=parameter[2]
    bls=[i for i in range(n+1,n+n0+1)]
    random.seed(0)
    def split_sort(b):
        if len(b)==0:
            return []
        elif len(b)==1:
            return b
        n=len(b)
        idx=random.randint(0,n-1)
        pivot_u=b[idx]
        lls=[]
        rls=[]
        if  pivot_u not in nb_dic.keys():
            for i in range(n):
                if i==idx:
                    continue
                lls.append(b[i])
            return (split_sort(lls)+[pivot_u])
        nb_u=nb_dic[pivot_u]
        for i in range(n):
            if i==idx:
                continue
            v=b[i]
            if v not in nb_dic.keys():
                lls.append(v)
                continue
            nb_v=nb_dic[v]
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
            if c_vu<c_uv:
                lls.append(v)
            else:
                rls.append(v)
        return (split_sort(lls)+[pivot_u]+split_sort(rls))
    def cross_counting(b,n0,n):
        sum_=0
        c=[[0 for i in range(n+1)] for i in range (n0+1)]
        for i in range(2,n0+1):
            for j in range(2,n+1):
                c[i-1][j-1]=c[i-1][j-2]+c[i-2][j-1]-c[i-2][j-2]
                v=b[i-2]
                w=n-j+2
                if v in nb_dic.keys() and w in nb_dic[v]:
                    c[i-1][j-1]+=1
                v=b[i-1]
                w=n-j+1
                if v in nb_dic.keys() and w in nb_dic[v]:
                    sum_+=c[i-1][j-1]
        return sum_
    orderedls=split_sort(bls)
    cross_number=cross_counting(orderedls,n0,n)
    ite_time=10#5
    for i in range(ite_time):
        b=split_sort(orderedls)
        new_count=cross_counting(b,n0,n)
        if new_count<cross_number:
            cross_number=new_count
            orderedls=b
            continue
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