#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

print_with_time(){
    now=$(date +"%T")
    echo "${bold}[$now]${normal} $1"
}

# For source
print_with_time "${bold}Don't forget to source ./bin/config.sh!${normal}"

# Remove pipes
print_with_time "Removing pipes in /tmp..."
rm -f /tmp/bas_* /tmp/net_*
print_with_time "Removing done!"

# in & out for every net and bas
print_with_time "Creating pipes in /tmp..."
for i in $(seq 0 $(($1 - 1)))
do
    mkfifo /tmp/net_in$i
    mkfifo /tmp/bas_in$i
done
print_with_time "Creating done!"

# launch every bas and nets, and redirect their output / input
print_with_time "Lauching ${bold}$1${normal} application.s..."
for i in $(seq 0 $(($1 - 1)))
do
    bin/bas.py --nsite=$i > /tmp/net_in$i < /tmp/bas_in$i &
    bin/net.py --nsite=$i --nmax=$1 < /tmp/net_in$i | tee /tmp/net_in[^$i]* /tmp/bas_in$i &
done

print_with_time "${bold}All done!${normal}"

