cd ..
./build.sh
for VELOCITY in 0.25 0.5 0.75 1 1.25 1.5 1.75 2
do
	for SIMULATION in {1..20}
	do
		python3 generator.py 100 0.2 $VELOCITY
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 pressureAnalysis.py $VELOCITY
		cd ..
	done
done