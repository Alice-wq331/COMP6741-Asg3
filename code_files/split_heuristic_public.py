import sys
import time
import signal
import random

sys.setrecursionlimit(100000)
class TimeoutError(Exception):
    pass

def signal_handler(signum, frame):
    raise TimeoutError("Operation timed out")


#Counting_crossing_alrgorithm
def cross_counting(b,n0,n,nb_dic):
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

def create_sol(n,n0,m,nb_dic,outputpath):
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
    def good_swap(v,u):
        if v not in nb_dic.keys() or u not in nb_dic.keys():
            return False
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
    def greedy_post(order):
        n=len(order)
        if n<=1:
            return order
        for i in range(n-1):
            j=i+1
            v=order[i]
            u=order[j]
            if good_swap(v,u):
                order[j]=v
                order[i]=u
        return greedy_post(order[0:n-1])+[order[n-1]]
    #set iteration time for split algortihm based on the data size
    if n>5000:
        ite_time=1
    elif n>3000:
        ite_time=3
    elif n>1000:
        ite_time=5
    elif n>500:
        ite_time=7
    else: #many medium size graphs with large minimum crossings are also in this range
        ite_time=10
    print(f"Split algorithm for {ite_time} iteration(s)")
    orderedls=split_sort(bls)
    if ite_time>1:
        cross_number=cross_counting(orderedls,n0,n,nb_dic)
    for i in range(ite_time-1):
        b=split_sort(orderedls)
        new_count=cross_counting(b,n0,n,nb_dic)
        if new_count<cross_number:
            cross_number=new_count
            orderedls=b
            continue
    with open(outputpath, 'w') as file:
        for item in orderedls:
            file.write(f"{item}\n")
    return orderedls   
        
for j in range(1,101):
    filepath='Pace2024-Testsets/heuristic_public/Instances/'+str(j)+'.gr'
    outputpath='Pace2024-Testsets/heuristic_public/Solutions_ite_1/'+str(j)+'.sol'
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
    timeout = 300 #set time limit as 5 minutes
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(timeout) 

    try:
        orderedls=create_sol(n,n0,m,nb_dic,outputpath)
        signal.alarm(0)
        print(f"Task {j} completed within the time limit")
        if n<60000:
            print("The achieved crossing number is ...",end='')
            cross_number=cross_counting(orderedls,n0,n,nb_dic)
            print(f"{cross_number}")
    except TimeoutError as e:
        print(f"Task {j} failed due to timeout")