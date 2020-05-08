# finalAI
IA qui joue à avalam pour le projet informatique de (Adrian Szidlowski et Louis Demarcin)

pour inscrire l'IA il y a le programme subtest.py pour lequel on peut spécifier le port en sys.argv[1] 
pour lancer l'IA on peut taper le numéro de port en sys.argv[1] (attention à lancer sur le même port que subtest)

bibliotèques utilisées:
aucune, nous nous basons uniquement sur des imports

stratégie utilisée:

nous générons un score à chaque position en fonction de la possibilité de construire une tour de 5 pions depuis une position et le nombre de tours appartenant à l'ennemi par rapport aux nombre de tours nous appartenant (voir computescore() )
cette génération de score est basée sur notre réflexion humaine face à des situations de jeu.

ensuite on parcoure ce tableau de score pour trouver une valeur favorable et on teste une série de coups autour de celle-ci en sélectionnant le meilleur

si aucun mouvement intéressant n'a été trouvé on génère un coup aléatoire mais qui respecte toujours les règles
