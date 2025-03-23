import shlex

def load_config(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = shlex.split(value.strip())[0]
    return config

# Charger la configuration globale
CONFIG = load_config("/home/mmk/tmp/projet_robot_LU2IN013/config.cfg")