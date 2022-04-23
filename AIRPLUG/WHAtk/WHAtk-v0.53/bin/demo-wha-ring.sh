# Airplug software
# Example of shell-script for a simple ring
# (c) B. Ducourthial 19/04/2022


# --- 1. Variables -------------------------------------------------------------

# --- 1.1 Parameters (to be modified)
# Number of nodes in the ring
NNODES=3

# Airplug application to be used
APP=wha.tk

# Options for the applications
OPTIONS="--auto"

# --- 1.2 Other variables
# Temporary directory for fifos
TMPDIR=/tmp/airplug-$USER-$$

# List of processes id that should be killed when quitting
LIST_PID=""



# --- 2. Cleaning function -----------------------------------------------------
# Cleanup function to kill processes and remove fifos at the end
cleanup () {
		echo "+ Catching signal => cleaning"

		# Killing all processes
		echo "+   Killing all subprocesses"
		kill -TERM $LIST_PID

		# Removing fifos
		echo "+   Removing fifos"
		\rm -f $TMPDIR/in* $TMPDIR/out*

		echo "+ End"
		exit 0
}



# --- 3. Step by step ----------------------------------------------------------
echo "+ Ring of three $APP"


# --- 3.1 Calling the cleanup function when the script terminates
echo "+   Catching signals"
trap cleanup INT QUIT TERM


# --- 3.2 Temporary directory 
echo "+   Creating temporary directory"
mkdir $TMPDIR || (echo "-   Failed creating temporary directory" ; exit)


# --- 3.3 Fifos 
echo "+   Creating input fifo in $TMPDIR"
for I in `seq $NNODES`; do
		rm -f $TMPDIR/in$I 2> /dev/null
		mkfifo $TMPDIR/in$I || (echo "-   Failed creating fifo in$I" ; exit)
done

echo "+   Creating output fifo in $TMPDIR"
for I in `seq $NNODES`; do
		rm -f $TMPDIR/out$I 2> /dev/null
		mkfifo $TMPDIR/out$I || (echo "-   Failed creating fifo out$I" ; exit)
done


# --- 3.4 Start the applications
echo "+   Starting the applications" 
for I in `seq $NNODES`; do
		./$APP --ident=app$I ${OPTIONS} < $TMPDIR/in$I > $TMPDIR/out$I &

		# Another process to kill at the end
		LIST_PID="$LIST_PID $!"
done


# --- 3.5 Ring
echo "+   Connecting the ring"
for I in `seq $NNODES`; do
		# J is equal to I+1 mod $NNODES
		J=$((I+1))
		if [ $J -gt $NNODES ] ; then J=1 ; fi

		# Link node I --> node J
		cat $TMPDIR/out$I > $TMPDIR/in$J &

		# Another process to kill at the end
		LIST_PID="$LIST_PID $!"
done


# --- 3.6 For lazzy processes
# NB: A security to be sure the processes are not waiting for something to read
#     before starting the GUI.
echo "+   Starting"
for I in `seq $NNODES`; do
		echo "" > $TMPDIR/in$I
done


# --- 4. Some printing in the terminal, waiting for Ctrl C ---------------------
echo "+   Waiting (you may quit by Ctrl-C)"
while true ; do
		echo -n "."
		sleep 10
done
