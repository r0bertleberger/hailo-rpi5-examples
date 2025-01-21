# Adaptation de l'implémentation du modèle yolo-v8 sur Hailo 8L et Raspberry Pi 5

## Problématique :

Le *hat* pour Raspberry Hailo 8L requiert une recompilation des modèles vers des `.HEF`, qui est un format propriétaire et requiert beaucoup de travail pour le faire fonctionner. Le fabricant a fourni des exemples d'utilisation du Hailo 8L avec le modèle `yolo-v8`, mais leur système n'est pas adapté au projet, puisque leur système fait appel à un afficheur graphique et ne stocke pas les coordonnées donnéspar le modèle.
Par ailleurs, puisque l'exemple est conçu pour une utilisation comme une caméra de surveillance, le flux vidéo est une boucle continue, ce qui n'est pas du tout adapté au projet.


## Modifications :

Tout d'abord, de manière grossière, j'ai redirigé l'écran vers un `fakesink`, qui est l'équivalent de `/dev/null` sur les systèmes GNU/Linux. Ensuite, j'ai redirigé l'affichage dans la console des coordonnées vers un fichier texte.
Quant à la boucle, j'ai mesuré le temps moyen de calcul par image, puis j'ai fait l'appel au modèle avec un `timeout` adapté à la durée de la vidéo, avec une marge. Pour compenser cette marge, j'ai fait un script python qui retire après les lignes en trop.


## Les script :

### `test.sh`

Analyse une vidéo à l'aide du modèle `YOLO-v8` et stocke le résultat dans un fichier texte.

###### Entrées
- *const* `video-file`, la vidéo à analyser,
- `text-file`, le fichier contenant les résultats

### `enlever-lignes.py`

Retire toutes les lignes à partir d'un certain rang à un fichier texte.

###### Entrées
- `text-file`, le fichier texte auquel il faut retirer des lignes
- *const* `int`, le rang de la première ligne à supprimer.

### `second-ia.py`

Compare / analyse un fichier texte donné en entrée avec la dataset, et renvoie dans la CLI le résultat.

###### Entrée
- *const* `text-file`, le fichier à analyser

###### Sortie 
- `cout`, précise si la posture est bonne ou pas.

### `clean.sh`

Supprimes les fichiers vidéos et des résultats intermédiaires.

### `demo.sh`

Capture une vidéo, l'analyse via `YOLO-v8` puis analyse le résultat avec le random forest, et donne, dans le tty, un résultat quant à la justesse de la posture.

##### Sortie 
- `cout`, le résultat de l'analyse.