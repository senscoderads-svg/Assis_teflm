import os
import random
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/original'

def fetch_tmdb_data(endpoint, params=None):
    """Função utilitária para requisições à API do TMDb."""
    if params is None:
        params = {}
    
    params['api_key'] = TMDB_API_KEY
    params['language'] = 'pt-BR'
    
    try:
        response = requests.get(f"{TMDB_BASE_URL}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do TMDb [{endpoint}]: {e}")
        return []

@app.route('/')
def home():
    if not TMDB_API_KEY:
        return "Erro: TMDB_API_KEY não configurada no arquivo .env", 500

    # Requisições para os endpoints solicitados
    trending = fetch_tmdb_data('/trending/all/week')
    popular_movies = fetch_tmdb_data('/movie/popular')
    top_rated_tv = fetch_tmdb_data('/tv/top_rated')
    action_movies = fetch_tmdb_data('/discover/movie', {'with_genres': '28'})
    comedy_movies = fetch_tmdb_data('/discover/movie', {'with_genres': '35'})

    # Seleciona um item em alta aleatório para ser a seção Hero
    hero_item = None
    if trending:
        hero_candidates = [item for item in trending if item.get('backdrop_path') and item.get('overview')]
        if hero_candidates:
            hero_item = random.choice(hero_candidates)

    return render_template(
        'index.html',
        hero=hero_item,
        trending=trending,
        popular_movies=popular_movies,
        top_rated_tv=top_rated_tv,
        action_movies=action_movies,
        comedy_movies=comedy_movies,
        img_url=IMAGE_BASE_URL
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)