from ursina import *

app = Ursina()

# Variable pour contrôler l'état de la simulation
simulation_running = True

# Création du sol
ground = Entity(model='plane', scale=(20, 1, 20), color=color.white, collider='box')

# Création du prisme triangulaire avec collider ajusté
prism = Entity(
    model=Mesh(vertices=[
        # Base inférieure (triangle isocèle)
        Vec3(0, 0.1, -0.5),
        Vec3(-0.5, 0.1, 2),  # Point 1 (gauche de la base)
        Vec3(0.5, 0.1, 2),   # Point 2 (droite de la base)
    ], triangles=[
        # Faces du prisme triangulaire
        (2, 1, 0),  # Base inférieure
    ]),
    color=color.green,  # Remplissage vert
    collider='box'  # Utilisation du collider pour correspondre à la forme
)

# Roues de la voiture (en bas du prisme triangulaire)
front_left_wheel = Entity(model='sphere', scale=0.2, position=(-0.5, 0.1, 2), color=color.black , parent=prism, collider='sphere')
front_right_wheel = Entity(model='sphere', scale=0.2, position=(0.5, 0.1, 2), color=color.black , parent=prism, collider='sphere')
back_wheel = Entity(model='sphere', scale=0.2, position=(0, 0.1, -0.5), color=color.black, parent=prism, collider='sphere')

# Obstacle avec collider
obstacle = Entity(model='cube', scale=(4, 2, 2), position=(0, 0, 5), color=color.black, collider='box')

# Fonction de vérification des collisions
def check_collisions():
    global simulation_running
    if prism.intersects(obstacle):  # Vérifier si le prisme touche l'obstacle
        print("Collision détectée !")
        simulation_running = False  # Arrêter la simulation en cas de collision

# Fonction de mise à jour pour déplacer la caméra et les objets
def update():
    global simulation_running
    
    if not simulation_running:
        # Bloquer tout mouvement tant que l'utilisateur ne redémarre pas
        if held_keys['r']:  # On redémarre seulement quand R est pressé
            print("Redémarrage du véhicule")
            simulation_running = True
            prism.position = (0, 0.1, -0.5)  # Réinitialisation de la position du prisme
            prism.rotation_y = 0  # Réinitialisation de la rotation du prisme
            camera.position = (0, 5, -12)  # Réinitialisation de la caméra
            camera.look_at(prism)
        return


    # Déplacement de la caméra avec les touches
    p = prism.forward
    if held_keys['w']:
        camera.position += camera.forward * time.dt * 5  # Déplacement en avant
    if held_keys['s']:
        camera.position -= camera.forward * time.dt * 5  # Déplacement en arrière
    if held_keys['a']:
        camera.position -= camera.right * time.dt * 5  # Déplacement à gauche
    if held_keys['d']:
        camera.position += camera.right * time.dt * 5  # Déplacement à droite
    if held_keys['up arrow']:
        
        prism.z += 5 * time.dt * p[2] # Déplacement vers l'avant
        prism.x += 5 * time.dt * p[0]
    if held_keys['down arrow']:
        prism.z -= 5 * time.dt * p[2] # Déplacement vers l'arrière
        prism.x -= 5 * time.dt * p[0]
    if held_keys['left arrow']:
        prism.rotation_y -= 50 * time.dt  # Rotation à gauche
        
    if held_keys['right arrow']:
        prism.rotation_y += 50 * time.dt  # Rotation à droite


    # Rotation de la caméra avec les touches de direction
    if held_keys['q']:
        camera.rotation_y -= 50 * time.dt  # Rotation à gauche
    if held_keys['e']:
        camera.rotation_y += 50 * time.dt  # Rotation à droite

    # Vérification des collisions à chaque mise à jour
    check_collisions()

# Position initiale de la caméra
camera.position = (0, 5, -12)
camera.look_at(prism)  # Faire en sorte que la caméra regarde le prisme

# Lancer l'application
app.run()
