#!/bin/bash


function get_ip {
    result=`ssh $1 "ifconfig wlan0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"`
    echo $result
}

##update on all hosts
#for host in `cat hosts`; do
#    ssh $host "cd pyage && git pull && git checkout distributed_launcher"
#done

#first host would be the master
master=`cat hosts | head -n 1`
master_ip=`get_ip $master`
pyro_port=9090

#kill pyro server if exists
ssh $master "fuser -k $pyro_port/tcp 1&>/dev/null"

#run pyro server on master
ssh $master "daemon -- python -Wignore -m Pyro4.naming -n $master_ip -p $pyro_port"

#run pyage on every machine
for host in `cat hosts`; do
    local_ip=`get_ip $host`
    ssh $host " mkdir -p \$HOME/pyage/logs \
        && export NS_HOSTNAME=$master_ip \
        && export PYRO_HOST=$local_ip \
        && export PYTHONPATH=\$HOME/pyage \
        && cd \$HOME/pyage/logs \
        && python \$HOME/pyage/pyage/core/bootstrap.py pyage.conf.flowshop_distributed_conf"
done