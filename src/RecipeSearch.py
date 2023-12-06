from flask import Blueprint, render_template, jsonify, request
from .RecipeBook import RecipeBook


bp = Blueprint('RecipeSearch', __name__)

@bp.route('/search')
def search_landing_page():
    return render_template('recipe_searching/landing_page.html')

@bp.route('/search_recipe', methods=['POST'])
def search_recipe():
    recipe_title = request.form.get('recipe_title')

    result = search_for_recipe(recipe_title)
    if result == 1:
        return jsonify({f'{recipe_title}': 'not found'})
    return jsonify(result)

def search_for_recipe(recipe_title):
    book = RecipeBook(output_folder='RecipeBook')
    extracted_recipe = book.extract_recipe(recipe_title)

    return extracted_recipe
