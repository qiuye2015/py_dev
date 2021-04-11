#!/bin/bash
# 获取hdfs目录下最近日期的文件

global_output_path=""
function get_recent_file(){
	input_path=$1
	count=1
	num=`hdfs dfs -ls $input_path | grep "Found" | awk '{print $2}'`
	while (( $count <= $num ))
	do
		ret=`hdfs dfs -ls  -t -r $input_path | tail -n $count | head -1 | awk '{print $8}'`
		hdfs dfs -test -e $ret/_SUCCESS
		if [ $? -eq 0 ]; then
			global_output_path=$ret
			break
		fi
		let "count++"
	done
}

pid2catid_hdfs="hdfs://mercury25148:8020/test/fjp"
get_recent_file  $pid2catid_hdfs
echo $global_output_path
