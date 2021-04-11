#########################################################################
# File Name: go_online.sh
# Author: fjp
# Created Time: Thu 05 Dec 2019 05:04:10 PM CST
#########################################################################
#!/bin/bash
set timeout 30

to_ips="
10.5.25.148
127.0.0.1
"
username="fjp"
password="fjp"

cmd="
echo "hi"
"
# 手动执行
function manual_cmd(){
    host=$1
    ssh $username@$host "$cmd"
}

# 自动输入密码
function auto_cmd(){
    host=$1
    expect -c "
    spawn ssh $username@$host \"$cmd\"
    expect {
        \"*yes/no*\" {send \"yes\r\"; exp_continue}
        \"*password*\" {send \"$password\r\"; exp_continue}
    }
    "
}

for ip in $to_ips
do
        echo "[`date +%Y-%m-%d\ %H:%M:%S`] $ip start..."
        auto_cmd $ip
        echo "[`date +%Y-%m-%d\ %H:%M:%S`] $ip finish!"
        echo ""
done

