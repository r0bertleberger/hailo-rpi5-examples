## Les script :

### `test.sh`

Analyse une vidéo à l'aide du modèle `YOLO-v8` et stocke le résultat dans un fichier texte.

###### Entrées
- *const* `video-file`, la vidéo à analyser,
- `text-file`, le fichier où seront écrits les résultats


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

### `demo-bis.sh`

Capture une vidéo, l'analyse via `YOLO-v8` puis analyse le résultat avec le random forest, et donne, dans le tty et dans un fichie texte, le résultat quant à la justesse de la posture.

##### Sortie 
- `cout`, le résultat de l'analyse.
- `resultat-bis.txt` fichier regroupant le résultat de l'anlyse
