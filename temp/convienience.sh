qstat -f | awk '/Job Id/ {job=$3 ; 
        if (s > 0) {printf(format,lastjob,user,name,state,host)} ;
        lastjob=job ; s+=1} 
   /exec_host/ {host=$3} 
   /Job_Name/ {name=$3} 
   /job_state/ {state = $3} 
   /Job_Owner/ {user=$3; sub("@.*","",user)}
   END {printf(format,lastjob,user,name,state,host)}
   BEGIN {format="%10s\t%10s\t%25s\t%5s\t%8s\n";
          printf(format,"JobId","Owner","Job Name","State","Hosts")}'