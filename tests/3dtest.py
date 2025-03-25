from ursina import *

app = Ursina()

# Variable pour contrôler l'état de la simulation
simulation_running = True

rien = Entity()
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
    collider='box',
    position=(0,0.1,2)# Utilisation du collider pour correspondre à la forme
)

trace = []
trace_trait = Entity(model=Mesh(vertices=[],mode='line'),color=color.black)

pivot_d = Entity(position = (0.5, 0.1, 2), parent = prism )
pivot_g = Entity(position = (-0.5, 0.1, 2) , parnet = prism)
# Roues de la voiture (en bas du prisme triangulaire)
front_left_wheel = Entity(model='sphere', scale=0.2, position=(-0.5, 0.1, 2), color=color.black , parent=prism, collider='sphere')
front_right_wheel = Entity(model='sphere', scale=0.2, position=(0.5, 0.1, 2), color=color.black , parent=prism, collider='sphere')
back_wheel = Entity(model='sphere', scale=0.2, position=(0, 0.1, -0.5), color=color.black, parent=prism, collider='sphere')

# Obstacle avec collider
#obstacle = Entity(model='cube', scale=(4, 2, 2), position=(0, 0, 5), color=color.black, collider='box')

# Fonction de vérification des collisions
#def check_collisions():
#    global simulation_running
#    if prism.intersects(obstacle) or front_left_wheel.intersects(obstacle) or front_right_wheel.intersects(obstacle) or back_wheel.intersects(obstacle):  # Vérifier si le prisme touche l'obstacle
#        print("Collision détectée !")
#        simulation_running = False  # Arrêter la simulation en cas de collision

# Variables de direction
steering_angle = 0  # Angle de braquage des roues avant
max_steering = 30   # Angle max de braquage
wheelbase = 2.5     # Distance entre les roues avant et arrière

# Fonction de mise à jour pour déplacer la caméra et les objets
def update():
    global simulation_running, steering_angle

    

    if not simulation_running:
        # Bloquer tout mouvement tant que l'utilisateur ne redémarre pas
        if held_keys['r']:  # On redémarre seulement quand R est pressé
            print("Redémarrage du véhicule")
            simulation_running = True
            prism.world_parent = rien
            pivot_d.world_parent = prism
            pivot_g.world_parent = prism
            prism.position = (0, 0.1, -0.5)  # Réinitialisation de la position du prisme
            prism.rotation_y = 0  # Réinitialisation de la rotation du prisme
            camera.position = (0, 5, -12)  # Réinitialisation de la caméra
            camera.rotation_y = 0  # Réinitialisation de la rotation de la caméra
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
        prism.world_parent = rien
        pivot_d.world_parent = prism
        pivot_g.world_parent = prism
        move_vehicle(forward=True)
    if held_keys['down arrow']:
        prism.world_parent = rien
        pivot_d.world_parent = prism
        pivot_g.world_parent = prism
        move_vehicle(forward=False)
    if held_keys['left arrow']:
        pivot_g.world_parent = rien
        prism.world_parent = pivot_g
        pivot_d.world_parent = prism
        pivot_g.rotation_y -= time.dt * 10
        #steering_angle = max(-max_steering, steering_angle - 40 * time.dt)  # Tourner à gauche
    elif held_keys['right arrow']:
        pivot_d.world_parent = rien
        prism.world_parent = pivot_d
        pivot_g.world_parent = prism
        pivot_d.rotation_y += time.dt * 10
        #steering_angle = min(max_steering, steering_angle + 40 * time.dt)  # Tourner à droite
    
    # Appliquer l'angle de braquage aux roues avant
    front_left_wheel.rotation_y = steering_angle
    front_right_wheel.rotation_y = steering_angle


    # Rotation de la caméra avec les touches de direction
    if held_keys['q']:
        camera.rotation_y -= 50 * time.dt  # Rotation à gauche
    if held_keys['e']:
        camera.rotation_y += 50 * time.dt  # Rotation à droite

    # Vérification des collisions à chaque mise à jour
    #check_collisions()

    # Ajouter la position à la trace si le mouvement est suffisant
    # Ajouter la position à la trace si le mouvement est suffisant
    if len(trace) == 0 or (trace[-1] - prism.position).length() > 0.5:  # Si le mouvement est assez grand
        trace.append(prism.position + (0, 0.1, 0))  # Ajouter la position au tracé

    # Mettre à jour le Mesh de la trace seulement si la trace contient plus d'un point
    if len(trace) > 1:
        trace_trait.model.vertices = trace  # Affecter la nouvelle liste de vertices
        trace_trait.model.generate()  # Générer la trace


# Fonction pour déplacer le véhicule en fonction de la rotation des roues avant
def move_vehicle(forward=True):
    speed = 5 * time.dt
    direction = 1 if forward else -1
    p = prism.forward
    prism.x += speed * direction * p[0]
    prism.z += speed * direction * p[2]


# Position initiale de la caméra
camera.position = (0, 5, -12)
camera.look_at(prism)  # Faire en sorte que la caméra regarde le prisme

# Lancer l'application
app.run()
