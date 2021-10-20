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
python ./hopfield/hopfield_main.py "./config/hopfield_config.json"
```
## Configuración para Kohonen
```json
{
  "load_symbols": ["A", "O", "K", "F"],
  "test_symbol": "F",
  "noise": 0.2,
  "letters_bitmap": "./data/letters.txt"
}
```

* `load_symbols`: son las letras el cual la red de Hopfield aprenderá a reconocer
* `test_symbol`: la letra que se usara para probar la red
* `noise`: la cantidad de ruido que se le aplicara a la letra de prueba
* `letter_bitmap`: archivo que contiene los bitmap de las letras
--------------
## Cómo correr Oja
```bash
python ./oja/oja_main.py "./config/oja_config.json"
```
### Configuración para Oja
```json
{
    "learning_rate": 0.1,

    "iter": 300,

    "data_path": "./data/europe.csv"
}
```

* `learning_rate`: numero que se dividira por el numero de iteracion para obtener el learning rate en cada iteracion
* `iter`: cantidad de iteraciones a realizar sobre el dataset
* `data_path`: path al csv con los datos