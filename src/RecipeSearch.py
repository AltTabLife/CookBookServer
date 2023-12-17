from flask import Blueprint, render_template, jsonify, request
from .RecipeBook import RecipeBook
import cv2
import easyocr
import numpy as np


bp = Blueprint('RecipeSearch', __name__)
book = RecipeBook(output_folder='RecipeBook')


@bp.route('/search')
def search_landing_page():
    return render_template('recipe_searching/landing_page.html')

@bp.route('/search_recipe', methods=['POST'])
def search_recipe():
    recipe_title = request.form.get('recipe_title')
    category = request.form.get('category')

    result = search_for_recipe(recipe_title=recipe_title, category=category)
    if result == 1:
        return jsonify({f'{recipe_title}': 'not found'}), 404
    return jsonify(result)
    

def search_for_recipe(**kwargs):
    # Define the order of priority for criteria
    possible_criteria = ['category', 'recipe_title']

    # Initialize an empty dictionary to store actual criteria
    actual_criteria = {}

    # Update actual_criteria with the provided values
    for criteria in possible_criteria:
        if kwargs.get(criteria) is not None and kwargs.get(criteria) != '':
            actual_criteria[criteria] = kwargs[criteria]

    # Initialize a variable to store the final list of titles
    returning_titles = []

    # Iterate through possible criteria and perform searches
    for criteria in possible_criteria:
        if criteria in actual_criteria:
            if criteria == 'recipe_title':
                # Perform search based on recipe title
                titles = book.check_partial_existence(actual_criteria[criteria])
            elif criteria == 'category':
                # Perform search based on category
                titles = book.search_by_category(actual_criteria[criteria])

            # Filter out titles not in returning_titles
            if len(returning_titles) == 0:
                returning_titles.extend(titles)
            else:
                returning_titles = [title for title in returning_titles if title in titles]

    # Return the final list of titles
    return returning_titles


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




ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}  # Add more extensions as needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sort_coordinates(coordinates):
    return sorted(coordinates, key=lambda x: (x[0], x[1]))

@bp.route('/upload_recipe_file', methods=['POST'])
def upload_recipe_file():
    # Check if the 'recipePhoto' file is in the request.files
    if 'recipePhoto' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['recipePhoto']

    # Check if the file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        # Read the image using OpenCV
        img_stream = file.read()
        img_array = np.frombuffer(img_stream, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Your image processing logic goes here
        max_canvas_size = 2560
        height, width, _ = img.shape
        max_dimension = max(height, width)
        scale_factor = min(1.0, max_canvas_size / max_dimension)

        resized_img = cv2.resize(img, (int(width * scale_factor), int(height * scale_factor)))

        reader = easyocr.Reader(['en'])

        result = reader.readtext(resized_img, paragraph=True)

        # Extract text and sort coordinates
        sorted_result = [(sort_coordinates(item[0]), item[1]) for item in result]

        return jsonify({'result': sorted_result})
    else:
        return jsonify({'error': 'Invalid file format'}), 400