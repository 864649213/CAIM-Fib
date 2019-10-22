Petita expliacion de los scripts utilizados para hacer la practica:

-> ZipsLaw.py: Fichero que a partir de el fitchero generado por el script CountWords, genera la grafica de frequencia-rango y la grafica de log(frequencia)-log(rango). Tambien pinta en formato array, por la consola, los valores optimos de la funcion de Zipf [a, b, c].

-> SplitText.py: Fichero que parte la novela pg30896.txt en 16 partes de tamaño incremental.

-> CreateHeapIndexes.py: Fichero que pone cada uno de los fitcheros creados por el script SplitText.py dentro de elasticsearch, con un indice diferente cada uno.

-> CountWordsHeap.py: Por cada uno de los fitchero insertados con el script CreateHeapIndexes.py, genera la grafica (palabras diferentes)-(numero de palabras). Tambien pinta en formato array, por la consola, los valores optimos de la fincion de Heap [K, Beta].
