# POC Music-Sim

Ce dépôt est une preuve de concept pour une application web qui utilise Flask pour se connecter à Milvus. L'objectif est de tester l'hypothèse qu'il est amusant de parcourir une bibliothèque musicale et de recevoir des recommandations basées sur les caractéristiques acoustiques des morceaux, plutôt que sur les métadonnées.

## Fonctionnalités

- **Parcourir la bibliothèque musicale** : Parcourez les artistes, albums et morceaux disponibles.
- **Recommandations basées sur les caractéristiques acoustiques** : Recevez des recommandations de morceaux similaires en fonction de leurs caractéristiques acoustiques.
- **Authentification** : Connectez-vous pour accéder à des recommandations personnalisées.

## Technologies Utilisées

- **Flask** : Framework web utilisé pour le backend.
- **Milvus** : Système de recherche vectorielle utilisé pour trouver des morceaux similaires.
- **Docker** : Utilisé pour containeriser l'application.
- **Back4app** : Service utilisé pour héberger l'application.

## Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/Hatchi-Kin/music-sim.git
    cd music-sim
    ```

2. Créez un fichier `.env` et ajoutez vos variables d'environnement :
    ```env
    API_URL=votre_api_url
    SECRET_KEY=votre_cle_secrete
    ```

3. Construisez et lancez les conteneurs Docker :
    ```sh
    docker-compose up --build
    ```

4. Accédez à l'application à l'adresse `http://localhost:5000`.

## Déploiement

L'application est déployée dans un conteneur grâce à un service de conteneurisation (Container as a Service) fourni par Back4app. Vous pouvez accéder à l'application déployée à l'adresse suivante : [https://musicsim-2agicsd1.b4a.run/](https://musicsim-2agicsd1.b4a.run/).

## Prochaines Étapes

Si cette preuve de concept est concluante, le projet sera réécrit en TypeScript et React pour une meilleure maintenabilité et une expérience utilisateur améliorée.
