🌲 wood_calculator

Objectif :

🔥 Détecter si le poêle est allumé via une sonde de température fixée sur le poêle ou à proximité.

⏱️ 30 minutes = 1 bûche

🌲 Conversion en stère

💰 Calcul du coût journalier

🔄 Reset automatique chaque jour


But: 

- Calcule automatique de sa consommation de bois en stére sur l'année.
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
    temp_seuil: 30
    duree_buche: 30
    buches_stere: 250
    prix_stere: 60
```

<img width="880" height="134" alt="image" src="https://github.com/user-attachments/assets/c6a39d01-9ad8-4025-9f5a-9886c178bf42" />

