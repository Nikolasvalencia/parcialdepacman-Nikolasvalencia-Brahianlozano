import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# Configuración de la ventana
ANCHO, ALTO = 600, 400

# Laberinto con más muros
paredes = [
    pygame.Rect(0, 0, 600, 10), pygame.Rect(0, 390, 600, 10),
    pygame.Rect(0, 0, 10, 400), pygame.Rect(590, 0, 10, 400),
    pygame.Rect(50, 50, 500, 10), pygame.Rect(50, 340, 500, 10),
    pygame.Rect(50, 50, 10, 300), pygame.Rect(540, 50, 10, 300),
    pygame.Rect(150, 100, 300, 10), pygame.Rect(150, 300, 300, 10),
    pygame.Rect(100, 200, 400, 10), pygame.Rect(250, 100, 10, 200)
]

# Ventana de Tkinter
root = tk.Tk()
root.title("Pac-Man")

# Variable de puntuación
puntos_comidos = tk.IntVar(value=0)

def iniciar_juego():
    global puntos_comidos
    puntos_comidos.set(0)
    juego_pacman()

def juego_pacman():
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pac-Man con Fantasmas")
    
    # Fuente para puntuación
    fuente = pygame.font.Font(None, 36)
    
    pacman_pos = [100, 100]
    pacman_vel = 4
    pacman_radio = 15

    fantasmas = [pygame.Rect(450, 100, 20, 20), pygame.Rect(450, 250, 20, 20)]
    fantasmas_vel = 2
    fantasmas_direcciones = [random.choice([(fantasmas_vel, 0), (-fantasmas_vel, 0), (0, fantasmas_vel), (0, -fantasmas_vel)]) for _ in fantasmas]
    
    puntos = [pygame.Rect(x, y, 10, 10) for x in range(60, 540, 40) for y in range(60, 340, 40) if not any(pygame.Rect(x, y, 10, 10).colliderect(p) for p in paredes)]
    
    reloj = pygame.time.Clock()
    ejecutando = True
    
    def mover_fantasma(idx):
        fantasma = fantasmas[idx]
        dx, dy = fantasmas_direcciones[idx]
        nueva_pos = fantasma.move(dx, dy)
        if any(nueva_pos.colliderect(pared) for pared in paredes):
            nuevas_direcciones = [(fantasmas_vel, 0), (-fantasmas_vel, 0), (0, fantasmas_vel), (0, -fantasmas_vel)]
            random.shuffle(nuevas_direcciones)
            for nueva_dx, nueva_dy in nuevas_direcciones:
                nueva_pos = fantasma.move(nueva_dx, nueva_dy)
                if not any(nueva_pos.colliderect(pared) for pared in paredes):
                    fantasmas_direcciones[idx] = (nueva_dx, nueva_dy)
                    break
        fantasma.x += fantasmas_direcciones[idx][0]
        fantasma.y += fantasmas_direcciones[idx][1]
    
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
        
        teclas = pygame.key.get_pressed()
        nueva_pos = pacman_pos.copy()
        if teclas[pygame.K_a]:
            nueva_pos[0] -= pacman_vel
        if teclas[pygame.K_d]:
            nueva_pos[0] += pacman_vel
        if teclas[pygame.K_w]:
            nueva_pos[1] -= pacman_vel
        if teclas[pygame.K_s]:
            nueva_pos[1] += pacman_vel

        pacman_rect = pygame.Rect(nueva_pos[0] - pacman_radio, nueva_pos[1] - pacman_radio, pacman_radio * 2, pacman_radio * 2)
        if not any(pacman_rect.colliderect(pared) for pared in paredes):
            pacman_pos = nueva_pos

        for i in range(len(fantasmas)):
            mover_fantasma(i)
            if pacman_rect.colliderect(fantasmas[i]):
                messagebox.showinfo("Game Over", "¡Pac-Man ha sido atrapado!")
                return

        for punto in puntos[:]:
            if pacman_rect.colliderect(punto):
                puntos.remove(punto)
                puntos_comidos.set(puntos_comidos.get() + 1)

        if not puntos:
            messagebox.showinfo("¡Ganaste!", "Has comido todos los puntos.")
            return

        VENTANA.fill(NEGRO)
        pygame.draw.circle(VENTANA, AMARILLO, pacman_pos, pacman_radio)
        for pared in paredes:
            pygame.draw.rect(VENTANA, AZUL, pared)
        for punto in puntos:
            pygame.draw.rect(VENTANA, BLANCO, punto)
        for fantasma in fantasmas:
            pygame.draw.rect(VENTANA, ROJO, fantasma)
        
        texto_puntuacion = fuente.render(f"Puntuación: {puntos_comidos.get()}", True, BLANCO)
        VENTANA.blit(texto_puntuacion, (10, 10))
        
        pygame.display.flip()
        reloj.tick(60)

# Botones en la ventana de Tkinter
tk.Label(root, text="Pac-Man", font=("Arial", 14)).pack()
tk.Button(root, text="Iniciar Juego", command=iniciar_juego).pack()
tk.Label(root, textvariable=puntos_comidos, font=("Arial", 12)).pack()

root.mainloop()