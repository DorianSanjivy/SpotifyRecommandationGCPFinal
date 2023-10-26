https://spotifyflaskdeploymentfinal.nw.r.appspot.com/

SpotifyRecommandation : Solution de site web pour la recommandation de musique

main.py : Application flask qui gère le backend du site.
Gère :
-les datasets json dans des dataframes
-les trois algorithme de recommandation : emotion, theme, lyrics
-la hiérarchie du site web

content : Contient les jsonl contenant les donnés sur les musique qui on été prétraiter par nos models, sert a la recommandation
Contient :
-FINAL_LYRICS.jsonl
-FINAL_SENTIMENT.jsonl
-FINAL_THEME.jsonl

templates : Contient les fichiers html des différentes pages ainsi que le javascript et css (grace à Bootstrap)
Contient :
-index.html (Recommandation de song en fonction de celui donner par l'utilisateur, donne une recommandation par emotion, theme et lyrics)
-emotion.html (Pour chaque emotion donne les 10 songs qui représente le plus cette emotion)
-theme.html (Pour chaque theme donne 10 songs aléatoire qui représente ce theme)

app.yaml : Setup du pc Google Cloud Platform

requirements.txt : Liste des librairies à installer
