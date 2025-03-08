from ..adaptateurs import AdaptateurVF,AdaptateurVS



class Controleur:
    def __init__(self,adapVS,adapVF):
        self.adapVF = adapVF
        self.adapVS = adapVS
    

    