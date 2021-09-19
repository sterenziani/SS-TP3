cd ..
./build.sh
for VELOCITY in 0.25 2 0.75 1.5 
do
	for SIMULATION in {1..2}
	do
		python3 generator.py 100 0.02 $VELOCITY
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 pressureAnalysis.py $VELOCITY $SIMULATION
		cd ..
	done
done