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
    category = request.form.get('category')

    result = search_for_recipe(recipe_title, category)
    if result == 1:
        return jsonify({f'{recipe_title}': 'not found'}), 404
    return jsonify(result)
    

def search_for_recipe(recipe_title=None, category=None):
    
    if recipe_title is None or recipe_title == '':
        return book.search_by_category(category=category)
    else:
        possible_titles = book.check_partial_existence(recipe_title)
        possible_category_titles = book.search_by_category(category=category)
        definite_titles = [title for title in possible_titles if title in possible_category_titles]
        return definite_titles

@bp.route('/recipe/<selected_link>')
def dynamic_route(selected_link):
    recipe_title = selected_link.strip('/').split('/')[-1]
    json_data = book.extract_recipe(recipe_title)
    
    recipe_data = {
        "ingredient": json_data["ingredient"],
        "instructions": json_data["instructions"]
    }
    return render_template('recipe_searching/recipe_display.html', recipe_name=recipe_title, recipe_data=recipe_data)

@bp.route('/add_custom_recipe')
def add_custom_recipe():
    return render_template('recipe_searching/add_custom_recipe.html')

@bp.route('/acr', methods=['POST'])
def acr():

    recipe_data = request.json
    
    if not book.check_recipe_existence(recipe_title=recipe_data['title']):
        book.add_recipe(
            category_title=recipe_data['categories'],
            recipe_title=recipe_data['title'],
            ingredients_array=recipe_data['ingredients'],
            instructions_array=recipe_data['instructions']
            )
        return "Recipe Added Successfully", 200
    else:
        return "Recipe Already Exists", 409
