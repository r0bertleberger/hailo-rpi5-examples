# Installation du projet

## Pré-requis : 

### Matériel

Raspberry Pi 5, Raspberry Pi Ai Kit +, carte micro-SD d'au moins 16Gb

### Logiciel

RpiOS à jour (Debian 12 Bookworm à l'heure de ce guide)

Git, Python, [dnsmasq](https://thekelleys.org.uk/dnsmasq/), [hostapd](https://w1.fi/cgit/hostap/),

## L'installation

Commencer par mettre à jour le système

##### Réglage du prt PCI-e

Lancer l'outil graphique de configuration du Rpi `sudo raspi-config` puis naviguer dans 
"advanced options" > "PCIe speed" > sélectioner "yes" > "finish".

##### Installation des dépendances du *hat*

Installer les dépendance pour l'accélérateur Hailo `sudo apt install hailo-all` puis redémarrer `systemctl reboot`.
Vérifier l'installation, `hailortcli fw-control identify`, la sortie attendue est du genre 
```
Executing on device: 0000:01:00.0
Identifying board
Control Protocol Version: 2
Firmware Version: 4.17.0 (release,app,extended context switch buffer)
Logger Version: 0
Board Name: Hailo-8
Device Architecture: HAILO8L
Serial Number: N/A
Part Number: N/A
Product Name: N/A
```

il y a ensuite un problème de version (toujours d'actualité le 8 Février) donc il faut spécifier manuellement la version de `hailo-tappas`, `sudo apt install hailo-tappas-core=3.30.0-1`

#### Installation du projet 

Cloner le repo `git clone https://github.com/r0bertleberger/hailo-rpi5-examples`, aller dans le dossier `cd hailo-rpi5-examples` et lancer l'installateur `source install.sh`. Vérifier l'installation `source setup_env.sh`

Créer le dossier pour les vidéos (qui est donc *évidemment* dans le `.gitignore`) `mkdir /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos`

Créer l'environnement Python pour le random-forest et les serveurs Web ` cd && python venv -m test-venv` puis l'activer `source test-vent/bin/activate` et installer les packet requis : `pip install opencv-python pandas scikit-learn Flask requests`.

#### Configuration Web

`sudo su`

`nano /etc/dnsmasq.conf` et taper 
```
interface=wlan0
dhcp-range=10.0.0.2,10.0.0.155,255.255.255.0,24h
dhcp-leasefile=/var/lib/misc/dnsmasq.leases
log-dhcp
log-facility=/var/log/dnsmasq.log
```

`nano /etc/dhcpd.conf` et taper
```
interface=wlan0

static ip_adress=10.0.0.1/24
nohook wpa_supplicant
```

`nano /etc/hostapd.conf` et taper
```
interface=wlan0
driver=nl80211
ssid=test-rpi
hw_mode=g
channel=6
auth_algs=1
wpa=2
wpa_passphrase=testtest
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
```

et pour lancer le tout : 
`ifconfig wlan0 10.0.0.1 netmask 255.255.255.0 up` puis `systemctl start dnsmasq` et `systemctl start hostapd`.

Il est maintenant possible de se connecter au réseau Wifi `test-rpi` avec le mot de passe `ceci-est-un-test` (à changer pour un vrai déploiement). Ensuite il faut se ssh au Rpi pour finir, `ssh pi@10.0.0.1` (ouvrir deux terminaux en parallèle)

#### Démarrer les sites Web 

Repérer l'IP de la caméra, elle est écrite dans le `/var/lib/misc/dnsmasq.leases` et modifier intelligement le fichier `/home/pi/Git/hailo-rpi5-examples/projet/testWebServer/server-mjpeg.py`, à la ligne 14 avec la "bonne" IP.

Ensuite `source /home/pi/test-vent/bin/activate` puis `python /home/pi/Git/hailo-rpi5-examples/projet/testWebServer/server-mjpeg.py` et véfier que le serveur est bien visible, au port 5050.

pour maintenant lancer l'interface Web finale, `source /home/pi/test-vent/bin/activate` puis `python /home/pi/Git/hailo-rpi5-examples/projet/testWebServer/server.py` et elle est au port 5000.
