# Cell-Index-Finder
SS TP3

## Para ejecutar:
./build.sh
java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar

## FLOW:
```
python3 generator.py
( Ejecutar en Java )
cd post-processing
python3 animator.py
cd ..
```

## OVITO:
```
Abrir animation/output0
Configurarlo como: x, y, vx, vy, radius, color
A la derecha, donde dice "Add modification...", elegir "Combine datasets"
Abajo aparece la ventanita para importar un dataset. Abrir "wall.txt"
Configurarlo como: x, y, radius
Destildar el elemento "Simulation cell"
Seleccionar output0 y en searchPattern poner "output\*"
```

## INPUT:
```
Cant de Particulas
Width Total
Height
GapSize
x	y	vx	vy	m 	r
x	y	vx	vy	m 	r
.....
```

## OUTPUT:
```
N

x	y	vx	vy	r 	m
x	y	vx	vy	r 	m
......
```

## TODO:
```
* Detallar como considera la colisión entre las partículas y los vértices de las tabiques que separan los recintos
* Graficar la evolución de fp y registrar el tiempo en que se llega al equilibrio
	** Para distintas (al menos 3) configuraciones del sistema
	** Variando el ancho de la apertura y el número de partículas N
	** Para cada configuración, simular varias realizaciones y presentar de manera adecuada los resultados
* Verificar si, en el equilibrio, se cumple la ley de gases ideales PV = T
* Realizar el ajuste de un modelo (P.V ~ T) que corresponda a los datos P vs T utilizando el método genérico
```
