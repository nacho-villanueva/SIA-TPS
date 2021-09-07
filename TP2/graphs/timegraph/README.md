# Timegraph
Para correr este grafico primero armar un archivo data.json en este directorio de la siguiente manera:
```json5
{
    "bar_name":["bar1","bar2"],
    "bar1":[ //llenar estos arreglos con los datos a promediar
        1,
        2,
        1
    ],
    "bar2":[
        2,3,2
    ]
}
```
donde bar_name debe tener los nombres de las barras y debe haber un dato con ese nombre dentro del json el cual sera un arreglo con los numeros a promediar