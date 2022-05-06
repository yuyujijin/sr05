# SR05 - Projet de programmation : *Comptes bancaires répartis et dupliqués*

1. [Présentation](#Présentation)
2. [Installation et lancement du projet](#Installation-et-lancement-du-projet)
    - [Installation](#Installation)
    - [Lancement](#Lancement)
3. [Description général des sites](#Description-général-des-sites)
    - [Généralités](#Généralites)
    - [Topologie](#Topologie)
    - [APP](#APP)
    - [BAS](#BAS)
    - [NET](#NET)
    - [Format des messages](#Format-des-messages)
5. [Algorithmes utilisés](#Algorithmes-utilisés)
    - [Sentinels (Lecture de l’entrée standard)](##Sentinels-Lecture-de-l’entrée-standard)
    - [Algorithme de file d'attente](#Algorithme-de-file-d’attente)
    - [Algorithme de snapshot](#Algorithme-de-snapshot)
7. [Scénarios](#Scénarios1)
    - [Déroulement classique d’une demande de section critique : exemple sur 2 sites](#Déroulement-classique-d’une-demande-de-section-critique--exemple-sur-2-sites)
    - [Déroulement classique d’une demande de snapshot : exemple sur 2 sites](#Déroulement-classique-d’une-demande-de-snapshot--exemple-sur-2-sites)
9. [Architecture](#Architecture)
    - [horlogelogique.py](#horlogelogiquepy)
    - [horlogevectorielle.py](#horlogevectoriellepy)
    - [message.py](#messagepy)
    - [output.py](#outputpy)
    - [app.py](#apppy)
    - [bas.py](#baspy)
    - [net.py](#netpy)

## Présentation

Ce projet a été réalisé par Adrien Magneron (`amagnero`), Lucas Mabille (`lumabill`), Haotian Zhu (`zhuhaoti`) et Eugène Valty (`valtyeug`) dans le cadre de l'UV SR05 (Algorithmes et systèmes repartis).
Il permet de mettre en oeuvre la duplication et repartition de données bancaires sur différents sites, en s'assurant que les données soit cohérentes entre chaque sites, en utilisant un algorithme de **file repartie**. Il permet aussi de prendre un instantané global du système en utilisant cette fois ci un algorithme de **snapshot**.

## Installation et lancement du projet

### Installation

Le projet utilise comme langage `python` et la librairie `tkinter` *(pour l'interface graphique)*. Il est donc nécessaire d'installer ces derniers *(possible via les commandes suivantes)*.

**Installer python 3.8 :**
```
apt-get install python3.8
```
**Installer tkinter :**
```
apt-get install python-tk
```

### Lancement

Le programme peut être lancé via le script `launch.sh`, en précisant le nombre de site voulu en argument.

## Description général des sites

### Généralites

Chaque site est composé de deux élements : `BAS` et `NET`. `BAS` représente l'application de base, ayant accès aux données (la **"section critique"**). Les messages destinées à `BAS` sont pré-traités par `NET`, qui gère si oui ou non `BAS` a accès à ces donées en utilisant l'algorithme de **file repartie** *(cf. partie correspondante)*. `NET` communique avec son `BAS` et les autres `NET`.
`NET` et `BAS` sont basés (héritent) d'un modèle plus général : `APP`.

### Topologie

Le choix d'une topologie **complète** a été fait. Chaque site communique donc avec tous les autres, et la retransmission des messages n'est donc pas nécessaire.

### APP

`APP` représente une application, lisant constamment dans l'entrée standard, et renvoyer chaque réponse a une fonction de reception, à implémenter selon le type d'application.
Une fonction d'envoi de message permettant de les formatter au format `AirPlug` est aussi disponible.

### BAS

`BAS` traite les données, ici bancaires, en demandant d'abord l'accès a ces dernières à son `NET`. Il communique donc exclusivement avec `NET`. 

### NET

`NET` gère les messages reçus pour et par `BAS` sur le réseau, et les traites selon le type de messages reçus, et utilise l'algorithme de **file repartie** pour s'assurer qu'aucun accès concurrent aux données soient possibles.

### Format des messages

Les messages envoyés sont au format `AirPlug`, comme décrit dans la DokuWiki. Comme l'adage le dit si bien, une image vaut plus que milles mots : 
![](https://github.com/yuyujijin/sr05/blob/main/imgs/msg.png?raw=True)
*Ces champs sont ensuite complétés selon le type de requête (par ex. quel site doit recevoir, le montant et les clients à débiter, …)*


## Algorithmes utilisés

### Sentinels (Lecture de l'entrée standard)

Les messages reçus par `BAS` sont envoyé sur un **Thread**, ne bloquant pas le déroulement de `BAS`. Les messages reçus sont ensuite ajoutés dans une file de messages, et sont traités par ordre d'arrivé par le Thread principal, en s'assurant d'un accès unique via un **MUTEX**. Cette solution s'approche de la solution **6** du cours.

### Algorithme de file d'attente

L'algorithme implémenté est calqué sur l'algorithme vu dans le cours ([ici](https://moodle.utc.fr/pluginfile.php/172574/mod_resource/content/1/5-POLY-file-attente-2018.pdf)). Les attributs, tableau et type de messages nécessaires ont été ajoutés aux applications `NET`.
La fonction de réception héritée de `APP` et implementée par `NET` implemente les gardes décritent dans l'algorithme de file d'attente et utilise des **estampilles** *(horloges logiques)*.
Le code commenté ***devrait*** suffir à comprendre le fonctionnement de ce dernier.

### Algorithme de snapshot

L'algorithme implémenté se base sur deux algorithmes du cours : 
1. Le premier algorithme de snapshot, supposant l'hypothèse **FIFO**
2. L'algorithme de snapshot permettant le rapatriement des captures au site initiateur

Les snapshot sont initiée par `BAS`, puis géré par `NET` qui compte le nombre de site restant. Chaque site ayant effectué sa capture devient rouge, s'assurant qu'une seule capture ne soit faites et que les messages ne circulent pas indéfiniement.
Après avoir récupéré toutes les captures, le site initiateur renvoie tout à `BAS`, qui écrit alors ces dernières dans un fichier de log.
L'algorithme utilise des **horloges vectorielles** pour s'assurer que les coupures soient cohérentes.

## Scénarios

Pour mieux comprendre le fonctionnement du programme, nous décrirons ici le déroulement classique d'un envoi de message de manière imagée, pour le plaisir de tous.

### Déroulement classique d'une demande de section critique : *exemple sur 2 sites*

![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties.png?raw=True)
***1.** Envoie d'une demande de section critique par `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(1).png?raw=True)
***2.** Reception de la requête par `NET` et retransmission aux autres `NET`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(2).png?raw=True)
***3.** Envoie d'un accusé de reception de la part des autres `NET`.*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(3).png?raw=True)
***4.** Reception des accusés, vérification de possibilité d'entrée en section critique et envoie de message d'entrée en section critique à son `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(4).png?raw=True)
***5.** Envoie d'un message de fin de section critique par `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(5).png?raw=True)
***6.** Reception du message de fin de section critique par `NET` et transmission d'un message de type libération aux autres `NET`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(6).png?raw=True)
***7.** Envoie d'un message de mis à jour des autres `NET` à leur `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(7).png?raw=True)
***8.** Fin de l'algorithme*

Encore une fois, le code commenté ***devrait*** se suffir à lui même pour observer plus en détail le traitement des messages et l'utilisation des fonctions *(aux noms explicites)*.

### Déroulement classique d'une demande de snapshot : *exemple sur 2 sites*

Execution imagée de l'algorithme, pour les mêmes raisons que précedemment.

![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties.png?raw=true)
***1.** Envoie d'une demande de snapshot par `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(1).png?raw=true)
***2.** Reception de la requête par `NET`, passage en rouge et déclaration en tant qu'initiateur et retransmission aux autres `NET`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(2).png?raw=true)
***3.** Reception de la requête par les autres `NET` et retransmission a leur `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(3).png?raw=true)
***4.** Renvoie de la capture par `BAS` a son `NET`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(4).png?raw=true)
***5.** Renvoie de la capture au `NET` initiateur*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(5).png?raw=true)
***6.** L'initiateur n'attend plus aucun site, il renvoie les captures a son `BAS`*
![](https://github.com/yuyujijin/sr05/blob/main/imgs/snap/SR05%20Algorithmes%20et%20syst%C3%A8mes%20r%C3%A9parties(6).png?raw=true)
***7.** Le `BAS` initiateur ecrit la capture dans un fichier log*

## Architecture

Le projet contient plusieurs fichier `python`, chacun ayant une fonction particulère : 

### `horlogelogique.py`

Comme son nom l'indique, `horlogelogique.py` gère la création, l'utilisation, l'incrémentation et la transformation en format textuel des **horloges logiques**.

### `horlogevectorielle.py`

Comme pour les horloges logiques, mais pour les **horloges vectorielles**.

### `message.py`

Gère la création de message, plus précisement le **payload**, via un dictionnaire de couple `clé`/`valeur`, leur création soit via un `string` au format `AirPlug` ou via un dictionnaire déjà instancié et leur passage au format texte `AirPlug`.

### `output.py`

Permet d'afficher des logs dans un format plutôt propre et compréhensible, incluant l'heure du log, dans la sortie erreur standard `stderr`.

### `request.py`

Gère les enums gérant le type de message des requêtes, pour `BAS` et `NET`.

### `app.py`

Comme décrit précedemment, possède un dictionnaire de couple `clé`/`valeur` (les paramètres), un constructeur permettant la crétation à partir d'un dictionnaire pré-rempli (ou non) et une liste de paramètres nécessaires (ou non), une methode d'envoi, une de reception **abstraite** et quelques methodes auxiliaires.

### `bas.py`

Hérite de `App`, réimplémente le constructeur pour compléter les paramètres, ainsi que la méhode de réception pour renvoyer aux différentes fonctions selon le type de requête. Une classe `BasWindow` est aussi dans le module et gère l'interface graphique de `BAS`.

### `net.py`

Hérite de `App`, réimplémente le constructeur pour compléter les paramètres, ainsi que la méhode de réception pour renvoyer aux différentes fonctions selon le type de requête. Comme décrit précedemment, implémente l'algorithme de la file d'attente en instantiant les paramètres nécessaire à sa création.


