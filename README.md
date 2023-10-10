# ReadMe - brief_cassandra


## Prérequis
Assurez-vous d'avoir les éléments suivants installés sur votre système avant de commencer :
- Docker
- Git (pour cloner le référentiel)
- Un navigateur web pour tester les requêtes API

## Installation

1. Clonez le référentiel du projet sur votre machine.

2. Dézippez les deux fichiers nodes dans le répertoire racine du projet.

## Configuration

3. Dans le répertoire du projet, exécutez la commande suivante pour construire et démarrer les conteneurs Docker :
   ```
   docker-compose up -d
   ```

4. Attendez que les conteneurs se déploient complètement. Vous pouvez vérifier leur état avec la commande suivante :
   ```
   docker-compose ps
   ```

## Tester les requêtes API

5. Ouvrez votre navigateur web et accédez à l'interface de documentation des API à l'adresse suivante : [http://localhost:8000/docs#/](http://localhost:8000/docs#/).

6. Vous trouverez quatre requêtes GET dans la documentation. Pour chacune d'elles, laissez la deuxième case d'ID vide, cela permet de sélectionner aléatoirement une des 2 nodes.

   - Première requête : Entrez l'ID suivant dans la première case : `41414797`
   - Deuxième requête : Entrez le mot `Chinese` dans la première case.
   - Troisième requête : Entrez l'ID suivant dans la première case : `41414797`
   - Quatrième requête : Entrez la lettre `C` dans la première case.

7. Appuyez sur le bouton "Exécuter" ou l'équivalent dans votre interface de documentation API pour tester chaque requête.

8. Les réponses aux requêtes s'afficheront dans la documentation API. Assurez-vous que les résultats correspondent aux attentes.
