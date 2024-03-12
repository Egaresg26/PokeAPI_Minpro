from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Review
import requests
from datetime import datetime

@app.route('/')
def pokemon_list():
    category = request.args.get('category', 'all')
    url = 'https://pokeapi.co/api/v2/pokemon/'
    
    if category != 'all':
        url += f'?type={category}'

    response = requests.get(url)

    if response.status_code == 200:
        pokemon_list = response.json()['results']
        return render_template('index.html', pokemon_list=pokemon_list)
    else:
        return 'Failed to fetch Pokemon list from PokeAPI'


@app.route('/pokemon/<pokemon_name>')
def pokemon_detail(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    if response.status_code == 200:
        pokemon_data = response.json()
        abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
        types = [type['type']['name'] for type in pokemon_data['types']]
        stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
        moves = [move['move']['name'] for move in pokemon_data['moves']]
        image_url = pokemon_data['sprites']['front_default']
        return render_template('pokemon_detail.html', pokemon_name=pokemon_name, 
                               abilities=abilities, types=types, stats=stats, moves=moves, image_url=image_url)
    else:
        return 'Pokemon not found'

@app.route('/add_review', methods=['POST'])
def add_review():
    pokemon_name = request.form['pokemon_name']
    rating = int(request.form['rating'])
    comment = request.form['comment']
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    new_review = Review(pokemon_name=pokemon_name, rating=rating, comment=comment,
                        user_ip=user_ip, user_agent=user_agent, created_at=datetime.utcnow())

    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('pokemon_list'))
