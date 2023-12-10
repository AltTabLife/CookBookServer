'''
This isn't really meant to be an extensive package. It's mainly just for consistency.
'''

import json, os
from pathlib import Path

class CategoryNotProvided(Exception):
    pass

class RecipeBook:
    '''
    Recipe Book handler that takes an output folder to name it, storing by either category or the first letter of each recipe.

    book = RecipeBook(output_folder, category_sort=True/False)
    
    Methods:
        add_category(category_title, category_href)

        add_recipe(category_title=None recipe_title=None, recipe_link=None, ingredients_array=None, instructions_array=None)

    '''
    #Be sure to have distinguishability between categories and raw recipes
    def __init__(self, output_folder, category_sort = False):
        #init the book
        self.output_folder = Path(output_folder)
        self.category_sort = category_sort
        #Sort by alphabet if no category_sort
        if not self.output_folder.exists() and category_sort == False:
            self.output_folder.mkdir(exist_ok=True)
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                json_filename = f"{letter}_recipes.json"
                json_path = self.output_folder / json_filename
                with json_path.open(mode='w') as json_file:
                    pass
        elif not self.output_folder.exists() and category_sort == True:
            self.output_folder.mkdir(exist_ok = True)
    
    def extract_json(self, json_filename):
        if os.path.getsize(json_filename) <= 2:
            return {}
        else:
            with open(json_filename, 'r') as jf:
                return json.load(jf)

    def check_file_string(self, category_title = None, recipe_title = None):
        '''
        Returns the sanitized Path(output_folder / file_string) for either a category title or a recipe title.

        '''
        if self.category_sort == True:
        
            try:
                #Sanitize to uniform format
                category_words = category_title.split()

                formatted_category = ''.join(word.capitalize() for word in category_words)
                
                #create file string
                category_file = self.output_folder / f'{formatted_category}_recipes.json'
                return category_file
            except:
                "Category processing failed"
        elif self.category_sort == False:
                #Sanitize
                for char in recipe_title:
                    if char.isalpha():
                        first_letter = char.lower()
                        recipe_file = self.output_folder / f'{first_letter}_recipes.json'
                        
                        return recipe_file
                    
    def check_partial_existence(self, partial_string):
        #for loop through <a-z>_recipes.json files
        recipe_files = []
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            json_filename = f"{letter}_recipes.json"
            json_path = self.output_folder / json_filename
            recipe_files.append(json_path)
        
        matching_recipes = []
        split_partial_string = [partial.lower() for partial in partial_string.split()]
        for file in recipe_files:
            fj = self.extract_json(file)

            for recipe_title in fj.keys():
                
                split_recipe_title = [word.lower() for word in recipe_title.split()]
                
                num_matches = sum(word in split_recipe_title for word in split_partial_string)

                if num_matches > 0:
                    matching_recipes.append((recipe_title, num_matches))

        matching_recipes = sorted(matching_recipes, key=lambda x: x[1], reverse=True)

        return [recipe[0] for recipe in matching_recipes]

    '''
    Returns True if recipe is found in the file
    Returns False if recipe is not found
    '''
    def check_recipe_existence(self, category_title = None, recipe_title = None):
        recipe_file = self.check_file_string(recipe_title=recipe_title)

        if self.category_sort == True:
            try:
                if category_title == None:
                    raise CategoryNotProvided("Category title is not provided")
                
                category_file = self.check_file_string(category_title=category_title)

                category_dict = self.extract_json(category_file)
                if recipe_title in category_dict:
                    return True
                else:
                    return False
            except CategoryNotProvided as e:
                print(f'Error: {e}')

        elif self.category_sort == False:
            #If no category sort, check it in the file.
            rf_dict = self.extract_json(recipe_file)

            if recipe_title in rf_dict.keys():
                return True
            else:
                return False

    def extract_recipe(self,  recipe_title, category_title = None):
        if self.check_recipe_existence(recipe_title=recipe_title):
            if self.category_sort == True:
                try:
                    if category_title == None:
                        raise CategoryNotProvided("Category title is not provided")

                    category_file = self.check_file_string(category_title=category_title)

                    category_dict = self.extract_json(category_file)
                    if recipe_title in category_dict:
                        return category_dict[recipe_title]
                    else:
                        return 1
                except CategoryNotProvided as e:
                    print(f'Error: {e}')
            elif self.category_sort == False:
                #If no category sort, check it in the file.
                recipe_file = self.check_file_string(recipe_title=recipe_title)

                rf_dict = self.extract_json(recipe_file)

                if recipe_title in rf_dict.keys():
                    returning_dict = rf_dict[recipe_title]
                    return returning_dict
                else:
                    print('recipe not found')
                    return 1
    def add_category(self, category_title, category_href):
        
        category_path = self.check_file_string(category_title=category_title)
        if not category_path.exists():
            file_dict = {
                'links': [category_href]

            }
            with open(category_path, 'w') as category_file:
                category_file.write(json.dumps(file_dict, indent=4))
        elif category_path.exists():
            file_dict = self.extract_json(category_path)
            if len(file_dict) == 0:
                link_dict = {'links': [category_href]}
                file_dict.update(link_dict)
                with open(category_path, 'w+') as category_file:
                    category_file.write(json.dumps(file_dict, indent=4))
            elif category_href in file_dict['links']:
                print(f'Category {category_path} with link {category_href} found')
                return
            else:
                file_dict['links'].append(category_href)
                with open(category_path, 'w+') as category_file:
                    category_file.write(json.dumps(file_dict, indent=4))

    def add_recipe(
        self,
        category_title=None,
        recipe_title=None, 
        recipe_link=None,
        ingredients_array=None,
        instructions_array=None
        ):
        recipe_file = self.check_file_string(recipe_title=recipe_title)

        if self.category_sort == True:
            try:
                if category_title == None:
                    raise CategoryNotProvided("Category title is not provided")
                else:
                    category_file = self.check_file_string(category_title=category_title)

                    recipe_dict = {
                        recipe_title:{
                            'link':recipe_link,
                            'ingredient':ingredients_array,
                            'instructions':instructions_array
                            }
                    }
                    rf_dict = self.extract_json(category_file)

                    if recipe_title in rf_dict:
                        print(f'{recipe_title} found in {recipe_file}')
                        return
                    else:
                        rf_dict.update(recipe_dict)
                        with open(category_file, 'w+') as rf:
                            rf.write(json.dumps(rf_dict, indent=4))
    
            except CategoryNotProvided as e:
                print(f'Error: {e}')

        elif self.category_sort == False:
            #If no category sort, check it in the file.
            rf_dict = self.extract_json(recipe_file)
            recipe_dict = {
                recipe_title:{
                    'link':recipe_link,
                    'ingredient':ingredients_array,
                    'instructions':instructions_array,
                    'category': category_title
                    }
            }
            if recipe_title in rf_dict:
                print(f'{recipe_title} found in {recipe_file}')
                return
            else:
                rf_dict.update(recipe_dict)
                with open(recipe_file, 'w') as rf:
                    rf.write(json.dumps(rf_dict, indent=4))


    '''
Script to swap from category sort to the standard <letter>_recipes.json

While category sort was fine originally, it's easier to search for recipes when sorted by the first letter, so I'm changing the default behavior to that, but will still leave the category option available.

New methods/functions to come will be defaulted to "title" based sort (<letter>_recipes.json), with True and False taking on meaning in:
    True == "file" category sort
    False == "title" based sort with categories fed as an array attribute of the recipe title.

In this particular script, categories stands for whether or not they will exist in the list based organization output, so standard "True"/"False"
Default is the category attribute will exist
'''
    def convert_to_title_based(self, categories=True):
        #Find the files that aren't title based
        ## Populate array of current non-title json files
        ftr = []
        for file in self.output_folder.iterdir():
            if file.is_file() and file.suffix == '.json':
                split_filename = file.stem.split('_')
                if len(split_filename[0]) == 1:
                    continue
                    
                ftr.append(file)
        
        ##For each non-title file, iterate through the recipes, adding the category as a parameter like {category: <category>}

        for non_title_file in ftr:
            fd = self.extract_json(non_title_file)
            category = non_title_file.stem.split('_')[0]
            for recipe in fd.keys():
                ###If it doesn't exist, move the dict to the new file
                if recipe == 'links' or self.check_recipe_existence(recipe_title=recipe):
                    continue
                else:
                    self.add_recipe(
                        category_title=category, 
                        recipe_title=recipe,
                        recipe_link=fd[recipe]['link'],
                        ingredients_array=fd[recipe]['ingredient'],
                        instructions_array=fd[recipe]['instructions']
                        )
    
    #Sorting funtions by different sections within the json

    '''
    Updates existing or creates category file (if none exists). Simple format below for fast searching anything with a category tag, or under a category file
    
    recipe_categories.json
    {
    <category>:[<recipe_titles>] 
    }
    '''

    '''
    Search for recipes by category
    '''
    def search_by_category(self, category):
        #loop through recipe files
        ##establish what will be returned
        category_array = []
        category = category.lower()
        ##check category sort    
        if self.category_sort == False:
            ##loop through title-based files
            ftr = []
            for file in self.output_folder.iterdir():
                if file.is_file() and file.suffix == '.json':
                    split_filename = file.stem.split('_')
                    if len(split_filename[0]) == 1:
                        ftr.append(file)
        
            for title_file in ftr:
                fd = self.extract_json(title_file)
                for recipe in fd:
                    if 'category' not in fd[recipe]:
                        continue
                    elif category in fd[recipe]['category'].lower():
                        category_array.append(recipe)
            
        elif self.category_sort == True:
            category_file = self.check_file_string(category_title=category)
            
            category_array = list(self.extract_json(category_file).items())

        return category_array