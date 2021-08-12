# Trabajo Practico 1 - Sokoban

En este TP se exploran diversos algoritmos, donde el objetivo es 
minimizar la cantidad de movimientos para resolver los escenarios del Sokoban.

## Dependencias 

* Python **>= 3.9** 
* PIP

## Getting Started 

### Instalación
Una vez que se tenga Python (>=3.9) y PIP instalado, pueden ejecutar el siguiente comando en la carpeta `./TP1` para instalar las dependencias

```shell
pip install -r requirements.txt
```

### Como Correrlo

Dentro de la carpeta `'./Tests` podrán encontrar diversos scripts los cuales al ejecutarlos correrán sus correspondientes algoritmos. 

Estos requieren de un parámetro, el cual es un archivo.txt donde se encuentra el código que representa el mapa que se quiere utilizar para encontrar la solución. En `./TestCodes` se pueden encontrar varios de estos archivos que contienen los códigos, 
o en caso de que se quiera generar sus propios mapas, se puede utilizar la página [game-sokoban.com](http://www.game-sokoban.com/) para generar estos codigos (Abajo a la derecha de cada mapa se puede encontrar como acceder al mismo).

#### Ejemplo de Ejecución:
```shell
python ./Tests/TestDFS ./TestCodes/testGame1.txt
```

## Descripción de las Clases 

A continuación daremos una breve descripción de cada clase. 

- **Sokoban:** La clase Sokoban está encargada de manejar toda la lógica del juego. 
Esto incluye permitir al jugador moverse, validar si un movimiento es válido, etc.

- **GameState:** Esta clase está encargada de manejar el estado del juego. 
Permite a los algoritmos guardar y cargar estados fácilmente.
  
- **Algorithms:** Esta clase permite ser extendida y es una interfaz común entre todos los algoritmos. 
  Las clases de algoritmos que extienden a la misma son:
    - **BFS**
    - **DFS**
    - **IDDFS**
    - ****
    - **** 
    - ****
    
- **SokobanBasicApplication:** Esta clase permite ser extendida, y fácilmente mostrar y actualizar el display grafico del juego. Las clases de algoritmos que extienden a la misma son:
    - **SokobanMain:** Esta clase extiende SokobanBasicApplication y permite, usando las flechas, jugar al juego.
    - **SokobanAlgorithmApplication:** Esta clase es instanciada por los tests de cada algoritmo, para que al pasar un array de movimientos correspondientes a la solución, esta pueda mostrar paso por paso. El mismo puede ser controlado con las siguientes teclas:
        - A: Avanzar automáticamente cada movimiento
        - Espacio: Avanzar un paso
        - Q: Salir