cd ..
./build.sh
for VELOCITY in 2 1.75 1.5 1.25 1 0.75 0.5 0.25
do
	for SIMULATION in {1..10}
	do
		python3 generator.py 100 0.01 $VELOCITY
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 pressureAnalysis.py $VELOCITY $SIMULATION
		cd ..
	done
done