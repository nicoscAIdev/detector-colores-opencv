import numpy as np
# Importa la biblioteca NumPy y le asigna el alias "np".
# NumPy permite trabajar con arreglos (arrays) de manera eficiente.

import cv2
# Importa OpenCV, que se utilizará para convertir colores entre distintos espacios
# (en este caso de BGR a HSV).


def get_limits(color):
    # Define una función llamada get_limits.
    # Recibe un color en formato BGR y devolverá dos límites en HSV:
    # un límite inferior y otro superior.

    c = np.uint8([[color]])  # BGR values
    # Convierte el color recibido en un arreglo de NumPy de tipo uint8.
    #
    # ¿Por qué [[color]]?
    # Porque cv2.cvtColor() espera una imagen y no un simple vector.
    # Aquí se crea una "imagen" de 1 píxel.
    #
    # Ejemplo:
    # color = [0, 255, 255]
    #
    # c tendrá la forma:
    # [[[0, 255, 255]]]
    #
    # Es decir:
    # 1 fila
    # 1 columna
    # 3 canales (BGR)

    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    # Convierte ese único píxel desde el espacio de color BGR a HSV.
    #
    # Ahora hsvC contiene el mismo color, pero expresado como:
    # Hue (tono)
    # Saturation (saturación)
    # Value (brillo)

    hue = hsvC[0][0][0]  # Get the hue value
    # Obtiene únicamente el valor de Hue (tono).
    #
    # hsvC tiene esta estructura:
    #
    # [
    #     [
    #         [H, S, V]
    #     ]
    # ]
    #
    # Primer [0] -> primera fila.
    # Segundo [0] -> primera columna.
    # Tercer [0] -> canal H (Hue).

    # Handle red hue wrap-around
    # El color rojo es un caso especial en HSV.
    # En OpenCV el Hue va de 0 a 180.
    # El rojo aparece tanto cerca del 0 como cerca del 180.
    # Por eso se necesita un tratamiento especial.

    if hue >= 165:  # Upper limit for divided red hue
        # Si el tono está muy cerca de 180,
        # significa que estamos en la parte superior del rojo.

        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        # Crea el límite inferior del rango.
        # Se permiten tonos 10 unidades menores.

        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
        # El límite superior llega hasta el máximo permitido (180).

    elif hue <= 15:  # Lower limit for divided red hue
        # Si el tono está muy cerca de 0,
        # también corresponde al rojo.

        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        # El límite inferior comienza en 0.
    
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        # El límite superior permite tonos un poco mayores.

    else:
        # Para cualquier otro color (amarillo, verde, azul, etc.)
        # simplemente se crea un rango simétrico alrededor del tono.

        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        # Permite tonos 10 unidades menores.

        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        # Permite tonos 10 unidades mayores.

    return lowerLimit, upperLimit
    # Devuelve ambos límites.
    # Más adelante serán utilizados por:
    #
    # mask = cv2.inRange(...)
    #
    # para decidir qué píxeles pertenecen al color buscado.