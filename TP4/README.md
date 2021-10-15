# Trabajo Práctico 4 - Métodos de Aprendizaje no Supervisado
En este trabajo práctico se implementaron los siguientes algoritmos:
* Método de Kohonen
* Método de Hopfield
* Método de Oja

## Dependencias
* Python **>= 3.9 (Importante!)**
* PIP
--------------
## Cómo correr Kohonen
```bash
python ./kohonen/kohonen_main.py "./config/kohonen_config.json"
```

### Configuración para Kohonen
```json
{
    "k": 4,
    "R": 2,
    "R_updates": true,
    "learning_rate": 0.5,
    "data_path": "./data/europe.csv"
}
```
* `k`: es el tamaño de la matriz k x k
* `R`: es el radio en el que se deben tomar en cuenta a los vecinos de la neurona activada
* `R_updates`: si está activado, el radio se decrementará desde el valor inicial `R` hasta 1 a lo largo del algoritmo
* `learning_rate`: factor de aprendizaje
* `data_path`: path del dataset

--------------
## Cómo correr Hopfield
```bash
python 
```
--------------
## Cómo correr Oja
```bash
python 
```

### Configuración para Oja