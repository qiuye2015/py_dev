cat $1 | sort -n |  \
awk 'BEGIN{count=0;sum=0;max=0}{count+=1;sum+=$1;s[count]=$1;if($1>max){max=$1}} \
	 END{print "avg:"sum/count"\t80:"s[int(count*0.8)]"\tmax:"max}'
