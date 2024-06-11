# Permite la posicion aleatoria del gato, raton, ruta de escape.
import random

# Interfaz.
import tkinter as tk
from tkinter import messagebox

TAMANO_TABLERO = 5
NUMERO_MOVIMIENTOS_MAX = 20

# Esta clase representa el tablero del juego, es una matriz, con un conjunto de vectores que te permite crear filas y columnas X, Y. 
class Tablero:

# Metodo constructor. 
# Comenzamos creando un tablero con espacios vacíos (' ').
    def __init__(self):
        self.tablero = [[' ' for _ in range(TAMANO_TABLERO)] for _ in range(TAMANO_TABLERO)]

# Elegimos posiciones aleatorias para el gato, el ratón y la ruta de escape.
        self.posicion_gato = self.posicion_inicial_aleatoria()
        self.posicion_raton = self.posicion_inicial_aleatoria()
        self.ruta_escape = self.posicion_inicial_aleatoria()

# Nos aseguramos de que el ratón no esté en la misma posición que el gato o la ruta de escape, y que haya suficiente distancia entre el gato y el ratón.   
        while self.posicion_raton == self.posicion_gato or self.posicion_raton == self.ruta_escape or self.distancia_minima(self.posicion_gato, self.posicion_raton) < 2:
            self.posicion_raton = self.posicion_inicial_aleatoria()
        
        while self.ruta_escape == self.posicion_gato or self.ruta_escape == self.posicion_raton:
            self.ruta_escape = self.posicion_inicial_aleatoria()

# Marcamos las posiciones del gato ('G'), el ratón ('R'), y la ruta de escape ('E') en el tablero.
        self.tablero[self.posicion_gato[0]][self.posicion_gato[1]] = 'G'  # Gato
        self.tablero[self.posicion_raton[0]][self.posicion_raton[1]] = 'R'  # Ratón
        self.tablero[self.ruta_escape[0]][self.ruta_escape[1]] = 'E'  # Ruta de escape

# Estos métodos nos ayudan a mover al ratón y al gato, y verificar si los movimientos son válidos.
    def posicion_inicial_aleatoria(self):   # Elige una posición aleatoria en el tablero.
        return (random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1))

# Calcula la distancia Manhattan entre dos posiciones.
    def distancia_minima(self, pos1, pos2):  # Calcula la distancia entre dos posiciones en el tablero.
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
# #  Mueve al ratón o al gato si el movimiento es válido (dentro del tablero y no ocupando un lugar del otro). 
    def mover_raton(self, movimiento):
        nueva_posicion = (self.posicion_raton[0] + movimiento[0], self.posicion_raton[1] + movimiento[1])
        if self.es_movimiento_valido(nueva_posicion):
            self.tablero[self.posicion_raton[0]][self.posicion_raton[1]] = ' '
            self.posicion_raton = nueva_posicion
            self.tablero[self.posicion_raton[0]][self.posicion_raton[1]] = 'R'
    
    def mover_gato(self, movimiento):
        nueva_posicion = (self.posicion_gato[0] + movimiento[0], self.posicion_gato[1] + movimiento[1])
        if self.es_movimiento_valido(nueva_posicion):
            self.tablero[self.posicion_gato[0]][self.posicion_gato[1]] = ' '
            self.posicion_gato = nueva_posicion
            self.tablero[self.posicion_gato[0]][self.posicion_gato[1]] = 'G'
# #

    def es_movimiento_valido(self, posicion): # Comprueba si la nueva posición es válida.
        return 0 <= posicion[0] < TAMANO_TABLERO and 0 <= posicion[1] < TAMANO_TABLERO and self.tablero[posicion[0]][posicion[1]] not in ['G', 'R']

    def obtener_estado(self):  #Devuelve el estado actual del tablero.
        return self.tablero
    
# Esta clase decide los mejores movimientos para el ratón y el gato usando un algoritmo inteligente.
class Minimax:
    def __init__(self, tablero):
# Variable de instancia 
        self.tablero = tablero

# MINIMAX

# Parametros 
    def minimax(self, profundidad, es_maximizando, alfa=float('-inf'), beta=float('inf')):

# Mis conficiones para terminar el juego 

        if profundidad == 0 or self.tablero.posicion_raton == self.tablero.ruta_escape or self.tablero.posicion_raton == self.tablero.posicion_gato:
           
           
            return self.evaluar_estado(), None # Nos dice cual es la posición actual.
        
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos arriba, abajo, izquierda, derecha


# Turno del ratón

        if es_maximizando:  # Variable para almacenar el mejor movimiento encontrado.
            max_eval = float('-inf') # ALFA representa el valor máximo garantizado
            mejor_movimiento = None # empezamos sin ningún movimiento mejor aún.
        

#  # Probamos cada movimiento posible  

            for movimiento in movimientos: 

              # Guardamos el estado actual del tablero.   
                estado_original = [fila[:] for fila in self.tablero.tablero]

              # Posición actual del ratón. 
                posicion_raton_original = self.tablero.posicion_raton
# # 


# #  Movemos al Ratón y Evaluamos jugada 

                self.tablero.mover_raton(movimiento) # movemos al raton 
                evaluacion = self.minimax(profundidad - 1, False, alfa, beta)[0]  # aca se aplica la recursividad, pero con profundidad -1
                # (miramos un movimiento menos en el futuro) y ""es_maximizando"" como False (ahora es el turno del gato).
                
                
                self.tablero.tablero = estado_original # Restauramos el tablero y la posición del ratón a como estaban antes de probar el movimiento.
                self.tablero.posicion_raton = posicion_raton_original 
# #  

# # Actualizar Mejor Evaluación y Movimiento 

                if evaluacion > max_eval: 
                    max_eval = evaluacion # Si la evaluación de este movimiento es mejor que max_eval, actualizamos max_eval y mejor_movimiento con este nuevo valor y movimiento.
                    mejor_movimiento = movimiento
                alfa = max(alfa, evaluacion)  # Actualizamos alfa con el máximo entre alfa y la evaluación.
                if beta <= alfa:
                    break  # Si beta es menor o igual a alfa, dejamos de probar más movimientos porque ya sabemos que no podemos encontrar un mejor resultado (esto se llama poda alfa-beta y nos ayuda a decidir más rápido).
# # 
           
          
# # Devolver la Mejor Evaluación y Movimiento

            return max_eval, mejor_movimiento 
# #
        
# Turno del gato

        else:  
            min_eval = float('inf') # BETA Representa el valor mínimo garantizado.
            mejor_movimiento = None # Variable para almacenar el mejor movimiento encontrado.

            for movimiento in movimientos: # iteracion de todos los moviemientos posibles 

# Guardamos el estado actual del tablero
                estado_original = [fila[:] for fila in self.tablero.tablero] 
                posicion_gato_original = self.tablero.posicion_gato 

                self.tablero.mover_gato(movimiento) # se ejecuta el movimiento del gato

                evaluacion = self.minimax(profundidad - 1, True, alfa, beta)[0] # Llamada recursiva a minimax con profundidad - 1 y True (ahora es el turno del ratón).
                
# restauramos el  estado original del tablero 
                self.tablero.tablero = estado_original 
                self.tablero.posicion_gato = posicion_gato_original  

# Actualizamos la evaluación mínima y el mejor Movimiento.
                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_movimiento = movimiento # Si la evaluación de este movimiento es menor que min_eval, actualizamos min_eval y mejor_movimiento.

# Se actualiza Beta y se ejecuta Poda Alfa-Beta
                beta = min(beta, evaluacion)
                if beta <= alfa:
                    break

# Se retorna la mejor evaluación y movimiento
            return min_eval, mejor_movimiento
        
# Calcula cuán favorable es una posición

    def evaluar_estado(self):
        distancia_gato = abs(self.tablero.posicion_gato[0] - self.tablero.posicion_raton[0]) + abs(self.tablero.posicion_gato[1] - self.tablero.posicion_raton[1])
        distancia_escape = abs(self.tablero.ruta_escape[0] - self.tablero.posicion_raton[0]) + abs(self.tablero.ruta_escape[1] - self.tablero.posicion_raton[1])
        return distancia_gato - distancia_escape

# Esta clase maneja la interfaz gráfica y el flujo del juego.
class JuegoGatoRaton:
    def __init__(self, root):
        self.root = root
        self.tablero = Tablero()
        self.minimax = Minimax(self.tablero)
        self.movimientos_realizados = 0
        self.root.title("Juego del Gato y el Ratón")
        self.crear_interfaz()

# Crea una ventana con botones para cada celda del tablero.

    def crear_interfaz(self):
        self.botones = []
        for i in range(TAMANO_TABLERO):
            fila = []
            for j in range(TAMANO_TABLERO):
                btn = tk.Button(self.root, width=4, height=2, command=lambda x=i, y=j: self.jugar())
                btn.grid(row=i, column=j)
                fila.append(btn)
            self.botones.append(fila)
        self.actualizar_tablero()

    def actualizar_tablero(self):
        estado = self.tablero.obtener_estado()
        for i in range(TAMANO_TABLERO):
            for j in range(TAMANO_TABLERO):
                self.botones[i][j].config(text=estado[i][j])

# Cada vez que se hace clic en un botón, se realiza un turno del juego. El ratón y el gato se mueven según el algoritmo Minimax.

    def jugar(self):
        if self.movimientos_realizados < NUMERO_MOVIMIENTOS_MAX:
            if self.tablero.posicion_raton == self.tablero.ruta_escape:
                messagebox.showinfo("Juego Terminado", "¡El ratón escapó por la ruta de escape!")
                return
            elif self.tablero.posicion_raton == self.tablero.posicion_gato:
                messagebox.showinfo("Juego Terminado", "¡El gato atrapó al ratón!")
                return
            else:
                _, mejor_movimiento_raton = self.minimax.minimax(profundidad=5, es_maximizando=True)
                self.tablero.mover_raton(mejor_movimiento_raton)

                if self.tablero.posicion_raton == self.tablero.ruta_escape:
                    messagebox.showinfo("Juego Terminado", "¡El ratón escapó por la ruta de escape!")
                    self.actualizar_tablero()
                    return
                elif self.tablero.posicion_raton == self.tablero.posicion_gato:
                    messagebox.showinfo("Juego Terminado", "¡El gato atrapó al ratón!")
                    self.actualizar_tablero()
                    return
                
                _, mejor_movimiento_gato = self.minimax.minimax(profundidad=5, es_maximizando=False)
                self.tablero.mover_gato(mejor_movimiento_gato)
                
                if self.tablero.posicion_raton == self.tablero.posicion_gato or self.tablero.distancia_minima(self.tablero.posicion_gato, self.tablero.posicion_raton) == 1:
                    messagebox.showinfo("Juego Terminado", "¡El gato atrapó al ratón!")
                    self.actualizar_tablero()
                    return

# Actualiza los botones para mostrar el estado actual del tablero.
                self.actualizar_tablero()
                self.movimientos_realizados += 1
                if self.movimientos_realizados >= NUMERO_MOVIMIENTOS_MAX:
                    messagebox.showinfo("Juego Terminado", "¡Se alcanzó el número máximo de movimientos!")

# Ejecución del juego
if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoGatoRaton(root)
    root.mainloop()
