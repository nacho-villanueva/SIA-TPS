# Trabajo Práctico 2 - Algoritmo Genético

En este TP se explora la implementacion de un algoritmo genético, con el uso de diversos metodos
de cruza, mutación y seleccion.

## Dependencias 

* Python **>= 3.9 (Importante!)**
* PIP

## Instalación
Una vez que se tenga Python (>=3.9) y PIP instalado, pueden ejecutar el siguiente comando en la carpeta `./TP1` para instalar las dependencias

```shell
pip install -r requirements.txt
```

## Cómo Correr
Utilizando python se debera ejecutar el main.py donde el primer parámetro es el del archivo de configuración.
```bash
python main.py "./config.json"
```

## Archivo de Configuración:
### Configuraciones Basicas
Para definir las configuraciones basicas deberan agregar los siguientes parámetros:

**Nota: Borrar los comentarios (//), ya que no son parte de json.**

**Nota: (opción_a | opción_b | opción_c) representa un parámetro que puede tomar únicamente esas opciones**
```json5
"role": ("warrior"|"archer"|"tank"|"assasin"), 
"population_size": 100, 
"K": 50,
  
"implementation": ("fill-all"|"fill-parent"),
"real_time_graphics": (true|false),
"precision": 2,
"mutation_probability": 0.5, // ∈[0, 1]

"weapons_dataset_path": "./dataset/armas.tsv",
"boots_dataset_path":   "./dataset/botas.tsv",
"helmets_dataset_path": "./dataset/cascos.tsv",
"gloves_dataset_path":  "./dataset/guantes.tsv",
"armours_dataset_path": "./dataset/pecheras.tsv"

```

* Los datasets pueden ser distintos a los proporcionados por la cátedra, pero de todas formas deben contener las mismas definiciones de columnas. Es decir, deben contar con las columnas "id", "Fu", "Ag", "Ex", "Re" y "Vi"

### Métodos de Seleccion/Remplazo
Para definir los métodos de configuración se deben utilizar como nombre los siguientes parámetros:
```json5
"A": 0.5,		// Coeficiente de Seleccion (A * selection_1 + (1-A) * selection_2)
"selection_1": {},	// Método de Seleccion 1
"selection_2": {},	// Método de Seleccion 2

"B": 0.5,		// Coeficiente de Seleccion (B * replacement_1 + (1-B) * replacement_2)
"replacement_1": {},	// Método de Remplazo 1
"replacement_2": {},	// Método de Remplazo 2
```
Donde los valores para los metodos de seleccion y de remplazo pueden ser los siguientes:
<table>
<tr>
	<td>
		<pre>Elite</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "elite",
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Ruleta</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "roulette",
},
		</pre>
	</td>
</tr>

<tr>
	<td>
		<pre>Universal</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "universal",
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Boltzmann</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "boltzmann",
},
		</pre>
	</td>
</tr>

<tr>
	<td>
		<pre>Torneo Determinísticos</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "deterministic_tournament",
	"M": 25
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Torneo Estocástico</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "stochastic_tournament",
	"threshold": 0.75    // ∈[0.5, 1]
},
		</pre>
	</td>
</tr>

<tr>
	<td>
		<pre>Ranking</pre>
	</td>
	<td>
		<pre>
"selection_1": {
	"method": "ranking",
},
		</pre>
	</td>
</tr>
</table>

### Métodos de Cruza
Para elegir el método de cruza se debera insertar una de las siguientes posibilidades:
<table>
<tr>
	<td>
		<pre>Cruza de un Punto</pre>
	</td>
	<td>
		<pre>
"crossover": "one_point",
		</pre>
	</td>
<td></td>
	<td>
		<pre>Cruza de dos Puntos</pre>
	</td>
	<td>
		<pre>
"crossover": "two_point",
		</pre>
	</td>
</tr>
<tr>
	<td>
		<pre>Cruza Anular</pre>
	</td>
	<td>
		<pre>
"crossover": "anular",
		</pre>
	</td>
<td></td>
	<td>
		<pre>Cruza Uniforme</pre>
	</td>
	<td>
		<pre>
"crossover": "uniform",
		</pre>
	</td>
</tr>
</table>

### Métodos de Mutación
Para elegir el método de cruza se debera insertar uno de las siguientes posibilidades:

<table>
<tr>
	<td>
		<pre>Unico Gen</pre>
	</td>
	<td>
		<pre>
"mutation": {
	"method": "gene"
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Multi-Gen Limitado</pre>
	</td>
	<td>
		<pre>
"mutation": {
	"method": "limited_multiple_gene",
	"M": 25
},
		</pre>
	</td>
</tr>
<tr>
	<td>
		<pre>Multi-Gen Uniforme</pre>
	</td>
	<td>
		<pre>
"mutation": {
	"method": "uniform_multiple_gene"
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Completo</pre>
	</td>
	<td>
		<pre>
"mutation": {
	"method": "complete"
},
		</pre>
	</td>
</tr>
</table>

### Condición de Freno
Para elegir la condición de freno se debera insertar una de las siguientes posibilidades:

<table>
<tr>
	<td>
		<pre>Por Tiempo</pre>
	</td>
	<td>
		<pre>
"stop_condition": {
	"method": "time",
	"time": 500		// Tiempo en Segundos
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Por Generacion</pre>
	</td>
	<td>
		<pre>
"stop_condition": {
	"method": "generation",
	"generation": 1000
},
		</pre>
	</td>
</tr>
<tr>
	<td>
		<pre>Por Fitness Maximo</pre>
	</td>
	<td>
		<pre>
"stop_condition": {
	"method": "fitness",
	"fitness": 30
},
		</pre>
	</td>
<td></td>
	<td>
		<pre>Por Estructura</pre>
	</td>
	<td>
		<pre>
"stop_condition": {
	"method": "structure",
        "relevant_percentage": 90,  // representa 90%
        "generations_amount": 10
},

El ejemplo de arriba significa "_cortar cuando las últimas 
10 generaciones tienen el 90% o más de su población idéntica_"
		</pre>
	</td>
</tr>
<tr>
	<td>
		<pre>Por Contenido</pre>
	</td>
	<td>
		<pre>
"stop_condition": {
	"method": "content",
	"generations_amount": 10
},
		</pre>
	</td>
</tr>
</table>