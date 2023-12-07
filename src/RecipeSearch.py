from flask import Blueprint, render_template, jsonify, request
from .RecipeBook import RecipeBook


bp = Blueprint('RecipeSearch', __name__)
book = RecipeBook(output_folder='RecipeBook')


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

    try:
        list_of_partials = book.check_partial_existence(recipe_title)



        return book.check_partial_existence(recipe_title)
    except:
        return "recipe searching failed"

@bp.route('/recipe/<selected_link>')
def dynamic_route(selected_link):
    recipe_title = selected_link.strip('/').split('/')[-1]
    json_data = book.extract_recipe(recipe_title)
    
    recipe_data = {
        "ingredient": json_data["ingredient"],
        "instructions": json_data["instructions"]
    }
    return render_template('recipe_searching/recipe_display.html', recipe_name=recipe_title, recipe_data=recipe_data)