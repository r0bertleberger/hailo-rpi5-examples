## Problématique :

Le *hat* pour Raspberry Hailo 8L requiert une recompilation des modèles vers des `.HEF`, qui est un format propriétaire et requiert beaucoup de travail pour le faire fonctionner. Le fabricant a fourni des exemples d'utilisation du Hailo 8L avec le modèle `YOLO-v8`, mais leur système n'est pas adapté au projet, puisque leur système fait appel à un afficheur graphique et ne stocke pas les coordonnées donnéspar le modèle.
Par ailleurs, puisque l'exemple est conçu pour une utilisation comme une caméra de surveillance, le flux vidéo est une boucle continue, ce qui n'est pas du tout adapté au projet.


## Modifications :

Tout d'abord, de manière grossière, j'ai redirigé l'écran vers un `fakesink`, qui est l'équivalent de `/dev/null` sur les systèmes GNU/Linux. Ensuite, j'ai redirigé l'affichage dans la console des coordonnées vers un fichier texte.
Quant à la boucle, j'ai mesuré le temps moyen de calcul par image, puis j'ai fait l'appel au modèle avec un `timeout` adapté à la durée de la vidéo, avec une marge. Pour compenser cette marge, j'ai fait un script python qui retire après les lignes en trop.
