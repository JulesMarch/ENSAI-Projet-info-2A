# ENSAI-Projet-info-2A
Groupe 7

France is divided in several zones : regions, departments, cities... In some cases it can be hard to know what exactly you're talking about.
Thus the goal of this project is to have an API that would help you to find more information about the place you're looking for.

To start the API, it's very easy : just run the file "app.py", at the root of the system, then go to http://localhost:8000
From here, you can manually complete the URL, but I'd advise you to go to http://localhost:8000/docs in order to do the researches more easily.

From now on, you can follow several paths :

- If you want to find informations from a INSEE code, go to /zonageparcode/{niveau}/{annee}/{code_insee}. niveau should be one of the following :
 "Région", "Département", "Commune" or "Arrondissement", annee should be the year you're looking for, and code_insee the code that you're looking for.
 For instance, you can try http://localhost:8000/zonageparcode/Département/2023/35 or http://localhost:8000/zonageparcode/Commune/2023/33009

- If you want to do the same thing, but by starting from the name of the place, go to /zonageparnom/{niveau}/{annee}/{nom}. nom should be the name of the place you're looking for,
and everything else should check the same qualifications as before.
For instance, you can try localhost:8000/zonageparnom/Région/2023/Bretagne or localhost:8000/zonageparnom/Commune/2023/Paris

- If you want to find where a specific point is, go to /coordonees/{niveau}. Niveau should still be one of those discussed above, and then you're supposed to add 3 querys :
the latitude lat, the longitude long and the year annee.
For instance, with The Eiffel Tower, you'll look for http://localhost:8000/coordonees/Commune?lat=48.858&long=2.294&annee=2023

- Finally, if you go to /listepoints/, you can post a json file being a list of list(lat:float, long:float, niveau:str). It will do exactly the same thing as before, but for several points at the same time.
You can try to post this (those points are the Eiffel Tower and the Ensai):
[
    [
        48.858,
        2.294,
        "Commune"
    ],
    [
        48.051,
        -1.742,
        "Département"
    ]
]

For all of these requests, you'll always have the same information : the name, the level you're looking for, the INSEE code, and eventually the higher strats containing your points (for instance, if you're looking for a vity, you'll know in which department and region it is too). If you're searching by coordinates, the webservice will also returns the coordinates you gave in the first place.

Have fun with our API, and don't be afraid to contact us if you're having any issue!
