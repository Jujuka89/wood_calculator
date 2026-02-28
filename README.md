[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Jujuka89/wood_calculator/releases)


🌲 wood_calculator

Objectifs :



**************************🔥 Détecter si le poêle est allumé *************************************** ✅ 

- Une sonde sera placée sur le poêle ou à proximité pour detecter la chaleur. Pour exemple la mienne est derrière à 30cm et j'estime la chauffe à partir de 30°C.

<img width="242" height="77" alt="image" src="https://github.com/user-attachments/assets/9d72eadd-028a-47c7-a991-c6574d7dd47b" />

```yaml
type: tile
entity: sensor.poele_en_route
show_entity_picture: false
hide_state: false
vertical: false
features_position: bottom
```

**************************🔥 Journalier : bûches brûlées / stère *************************************** ✅ 

<img width="461" height="154" alt="image" src="https://github.com/user-attachments/assets/5554f320-f0a0-481f-a062-3555e17bee54" />

```yaml
type: tile
entity: sensor.buches_brulees_jour
vertical: false
features_position: bottom
grid_options:
  columns: 12
  rows: 1

```

```yaml
type: tile
entity: sensor.consommation_bois_stere
vertical: false
features_position: bottom
grid_options:
  columns: 12
  rows: 1

```

⏱️ 30 minutes = 1 bûche (Estimation réglable)

**************************💰 Calcul du coût journalier *************************************** ✅ 

<img width="236" height="68" alt="image" src="https://github.com/user-attachments/assets/3a015891-168a-4d23-b56c-1d210c315902" />


**************************📅 Saison de chauffe : consommation en stère persistante *************************************** ✅ 

Un nouveau capteur `sensor.consommation_bois_stere_saison` est ajouté :
- il cumule la consommation en stère sur la **saison de chauffe** (par défaut septembre → août),
- il **conserve la valeur après redémarrage de Home Assistant**,
- il se remet à zéro automatiquement au démarrage de la saison suivante,
- le mois de début est réglable via `debut_chauffe_mois`.


************************** Prédiction pour l'année suivant les DJU *************************************** ❌




- Alerte remettre du bois

- Commande d'une ventilation suivant poele allumé et piece basse.
  
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




