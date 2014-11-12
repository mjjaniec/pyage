= Lunch in distributed environment

== Preconditions

* on each host
 * pyro4 installed
 * unix system
 * sudo apt-get install daemon
 * pre-installed python 2.7
 * pyage cloned into $HOME/pyage
* host file contains list of host on which pyage should be run
 * first host would be used as master
* current user can ssh onto all these machines without entering password nor user name
 * i.e. he should has accounts with the same name on all machines and
 * ssh certificates (see http://www.linuxproblem.org/art_9.html)
