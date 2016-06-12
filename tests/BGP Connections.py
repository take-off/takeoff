#Program for checking the status of the BGP neighbor from the "show ip bgp summary" command.
#Note: Enter the correct number of BGP neighbors. Entering more number than acual produces random result.
pfile=open("BGP.txt")
pfile_r=pfile.read()
pfile_l=pfile_r.split()
index_version=pfile_l.index("State/PfxRcd")
iteration=int(raw_input("Enter the number of neighbours"))
   
def nei_fun(nei,nei_name):
    #print nei, nei_name
    #print type(nei), type(nei_name)
    
    try:
        int(nei)
        print "Connection is working"
    except:
        print "BGP peering with", nei_name, "is Down"
        
for neighbor in range(iteration): 
    nei=pfile_l[index_version+10*neighbor]
    temp=index_version+10*neighbor
    nei_name=pfile_l[temp+1]
    #print nei, temp, nei_name
    #print type(nei), type(temp), type(nei_name)
    nei_fun(nei, nei_name)






