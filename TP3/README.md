# Trabajo Práctico 3 - Perceptron

Pending description

## Dependencias 

* Python **>= 3.9 (Importante!)**
* PIP

## Instalación
Una vez que se tenga Python (>=3.9) y PIP instalado, pueden ejecutar el siguiente comando en la carpeta `./TP3` para instalar las dependencias

```shell
pip install -r requirements.txt
```

## Cómo Correr
Utilizando python se deberá ejecutar el main.py donde el primer parámetro es el del archivo de configuración.
```bash
python main.py "./config.json"
```

Hay varios archivos de configuración pre-definidos en la carpeta `/config`, cada uno para resolver un problema indicado en la consigna del trabajo práctico.

### Ejercicio 1.1
Resuelve el problema del XOR con el perceptrón escalón.
```bash
python main.py "./config/ejercicio_1_Y.json"
```

### Ejercicio 1.2
Resuelve el problema del Y con el perceptrón escalón.
```bash
python main.py "./config/ejercicio_1_XOR.json"
```

### Ejercicio 2.1
Resuelve el problema 2 con el perceptrón lineal.
```bash
python main.py "./config/ejercicio_2_lineal.json"
```

### Ejercicio 2.2
Resuelve el problema 2 con el perceptrón no lineal.
```bash
python main.py "./config/ejercicio_2_no_lineal.json"
```

### Ejercicio 3.1
Resuelve el problema del XOR con el perceptrón multicapa.
```bash
python main.py "./config/ejercicio_3_XOR.json"
```

### Ejercicio 3.2
Resuelve el problema de las imágenes de los números con el perceptrón multicapa.
```bash
python main.py "./config/ejercicio_3_imagenes_v1.json"
```

### Ejercicio 3.3
Resuelve el problema de las imágenes de los números con el perceptrón multicapa, pero con ruido añadido.
```bash
python main.py "./config/ejercicio_3_imagenes_v2.json"
```