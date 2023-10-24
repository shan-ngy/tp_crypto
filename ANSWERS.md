# TP secure chat
## Prise en main

1) C'est une topologie client-serveur.

2) Dans les logs, on peut voir l'expediteur, le receptionneur et le contenu du message.

3) Ici, les échanges sont en clair donc cela viole le principe de confidentialité.

4) Il faudrait mettre en place un chiffrement des message avant que ceux-ci ne passe dans le serveur : on aurait donc un chiffrement entre l'expediteur et le serveur, pui un déchiffrement en le serveur et le receptionneur (chiffrement end to end).

## Chiffrement

1) Pour la cryptographie, les fonctions random(s) de python, dont urandom, ne sont pas assez sécurisées pour cette utilisation : des attaquants pourraient utiliser les potentielles failles derrière ces fonctions. Ainsi, il faudrait utiliser la bibliothèque 'cryptography', créée pour cette usage.

2)

3) Un chiffrement se faire entre un serveur et un client mais une fois que les informations atteignent le serveur, ce dernier peut porter atteinte à ces dernières.

4) Il manque la principe d'intégrité, qui consiste à autoriser qu'une partie restreinte de personnes à pouvoir apporter des modifications aux messages/informations.

## Authenticated Symetric Encryption

1) Fernet est moins risqué par sa simplicité, l'utilisation 'd'une clé statique, de la garantie d'intégrité et de l'encodage en base64.

2) C'est une attaque de répétition.

3) On peut utiliser un IV aléatoire pour chaque message chiffré.

## TTL

1) Oui, ça serait l'ajout d'un Time To Live (TTL) pour les messages.

2) Les messages expirent plus rapidement (15s.), ce qui peut entraîner la perte de messages si le temps de traitement est supérieur à la durée de vie.

3) Le TTL protège partiellement contre les attaques de répétition, mais ça ne donne pas une protection complète.

4) Les limites incluent la vulnérabilité aux attaques en temps réel, la perte de messages si la durée de vie est trop courte, les problèmes de synchronisation d'horloge, les manipulations de l'horloge, et les retards inattendus.

## Regard critique

L'ajout d'un TTL basé sur le temps est une bonne idée pour éviter la réutilisation des anciens messages, mais ça ne règle pas tous les problèmes de sécurité. 
Pour être plus sûr, il faudrait aussi utiliser d'autres techniques qu'on a vu avant, comme des IV aléatoires, une bonne gestion des clés, vérifier l'intégrité des messages et sécuriser la communication entre les parties.

