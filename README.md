[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Jujuka89/wood_calculator/releases)


🌲 wood_calculator

Objectif :

🔥 Détecter si le poêle est allumé:

- Une sonde sera placée sur le poêle ou à proximité pour detecter la chaleur. Pour exemple la mienne est derrière à 30cm et j'estime la chauffe à partir de 30°C.


⏱️ 30 minutes = 1 bûche

🔥 Journalier : bûches brûlées / stère

📊 Annuel : stère depuis le 1er janvier

🌍 Total : stère depuis toujours (Energy Dashboard friendly)

💰 Calcul du coût journalier

🔄 Persistant après reboot grâce à RestoreEntity


But à venir: 

- Prédiction pour l'année suivante.
  
- Connaitre les jours de chauffe ainsi que les éconnomies.
  
- Comparaison avec les DJU
  
- Estimer s'il est préférable de chauffé au bois ou à l'électrique suivant la température extérieur et le cout ?


  Future card de réglages :
  
  - Seuil de la sonde
    
  - Prix d'achat du stère
    
  - taille des buches
    

<img width="1056" height="478" alt="image" src="https://github.com/user-attachments/assets/8d415b71-2b74-44a3-a844-125445a833f4" />

<img width="1030" height="484" alt="image" src="https://github.com/user-attachments/assets/f257597e-41b7-46b5-a089-c59a0e221cff" />

<img width="1018" height="437" alt="image" src="https://github.com/user-attachments/assets/04776d84-4a31-4cd3-8d47-e1607a5fdc88" />



A mettre dans "sensors" : 

```yaml
  - platform: wood_calculator
    poele_sensor: sensor.sonde_poele_a_bois_temperature
    temp_seuil: 30 #suivant le positionnement de la sonde
    duree_buche: 30
    buches_stere: 250
    prix_stere: 60
```


Création de plusieurs sensors :

<img width="880" height="134" alt="image" src="https://github.com/user-attachments/assets/c6a39d01-9ad8-4025-9f5a-9886c178bf42" />

<img width="1089" height="59" alt="image" src="https://github.com/user-attachments/assets/f8dbec16-53a6-4256-a962-45501d0c054a" />



<img width="1384" height="339" alt="image" src="https://github.com/user-attachments/assets/cca43a90-f917-448d-b4a8-c8f47564431d" />




