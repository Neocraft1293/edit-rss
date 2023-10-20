import requests
import feedparser
import re
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

# URL du flux RSS d'origine
rss_url = "https://www.torrent911.io/rss/animes"

def generate_modified_rss():
    # Télécharger le flux RSS
    response = requests.get(rss_url)

    # Vérifier si la demande a réussi
    if response.status_code == 200:
        # Analyser le flux RSS
        feed = feedparser.parse(response.text)

        # Créer un nouveau générateur de flux RSS modifié
        fg = FeedGenerator()

        # Remplir les métadonnées du flux modifié
        fg.id(rss_url)
        fg.title(feed.feed.title)
        fg.link(href=rss_url)
        fg.description(feed.feed.subtitle)

        # Afficher chaque élément du flux dans la console
        for entry in feed.entries:
            # Utilisation d'une expression régulière pour extraire l'ID du lien dans la description
            id_match = re.search(r'\/image\/([0-9a-f]+)\.', entry.description)
            if id_match:
                extracted_id = id_match.group(1)

                # Créer une nouvelle entrée dans le flux modifié avec le lien modifié
                fe = fg.add_entry()
                fe.id(entry.link)
                fe.title(entry.title)
                fe.link(href=f"https://www.torrent911.io/get_torrent/{extracted_id}")
                fe.description(entry.description)

        # Générer le flux RSS modifié au format Atom
        rss_feed_modified = fg.atom_str(pretty=True)
    else:
        rss_feed_modified = f"Échec de la demande HTTP (Code de statut : {response.status_code})"

    return rss_feed_modified

@app.route('/rss')
def serve_rss():
    rss_feed_modified = generate_modified_rss()
    return Response(rss_feed_modified, mimetype='application/xml')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
