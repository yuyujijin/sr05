# ARCHITECTURE

## Architecture générale

Le système est composé de plusieurs sites reparties, qui communiquent entre eux. Chaque site est composée de deux composantes : `NET` et `BAS`. 
- `BAS` correspond à l'application de base et effectuant les opérations et calculs.
- `NET` correspond à la couche réseau, et traite les messages reçu par d'autres `NET` pour les rediriger vers `BAS`, et traite les messages reçus de `BAS` pour les envoyer aux autres `NET`

## Langage utilisé

Le langage choisi est `python`.

## Envoi et réception des messages

Les envoies de messages se font via `stdout`, et la reception via `stdin`. Tout autre message peut être envoyé dans `stderr`.

## Format des messages

Les messages sont de la forme `/{SENDER}/{RECEIVER}/{MSG}`, avec `{SENDER}` et `{RECEIVER}` soit égals à `BAS` ou `NET`, et `{MSG}` de la forme `^{key}~{value}`.

## Contenu de MSG

Les messages peuvent contenir autant de couples clé~valeur que l'on veut. On décidera pour nos messages d'avoir les champs :
- `nseq~int` pour le numéro d'horloge
- *`type~str` pour préciser le type de message : soit `...` pour les transactions, soit `snapshot` pour une demande de snapshot* **(à préciser)**
- pour les messages de `NET` à `NET`, un champ `^appnet~BAS` est rajouté par `NET` pour préciser l'origine du message

## Structuration du code 

Pour la structuration du projet, on a récuperé les templates du tutoriel **Airplug**, qu'on adaptera selon nos besoins (comme expliqué dans le projet). On a donc les répertoires `BASpy`, contenant l'application simulant l'hôpital (avec une interface), et `NETpy`, contenant l'application s'occupant du réseau et de la retransmission des messages.

## Fonctionnement des sites lors de la récepetion des messages

Il faut bien faire attention à ne pas faire de l'attente active et bien gérer les locks pour ne pas avoir d'accès concurrent sur une donnée au sein d'un même site. (cf correction **Activité 4**).
Pour les algos au sein des sites :
- pour `NET`, le template donné et le tutorial **Airplug** explique bien le traitement apporté aux messages
- pour `BAS`, bien regarder les algos. avec les gardes de reception, envoie de message et traitement des données + màj de l'horloge du cours
- pour les `snapshots`, se referer a l'algo. du cours pour ces dernières **(peut être intégrer un champ couleur sur chaque site?)**
- aussi regarder l'algo. de file inclu dans le projet

**Normalement**, le projet et le cours se suffisent à eux même pour les traitements, seul le formattage et la création des messages est spéciales.