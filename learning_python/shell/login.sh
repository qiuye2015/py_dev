#!/usr/bin/expect

set timeout 30
set host "10.5.25.150"
set username "fjp"
set password "fjp"

spawn ssh $username@$host
expect {
    "*yes/no*" {send "yes\r"; exp_continue}
    "*password*" {send "$password\r"; exp_continue}
    }
expect "*#"
interact

exit

if {$argc < 3} {
    puts "Usage:cmd <host> <username> <password>"
    exit 1
}

set timeout -1
set host [lindex $argv 0] 
set username [lindex $argv 1]
set password [lindex $argv 2]
#set username "root"
#set password ""
