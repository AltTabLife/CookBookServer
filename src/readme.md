<h1>
CookBook Server
</h1>

<p>
    Welcome to the personal server to consolidate all recipes from your family's history, and make them accessible to the family through the source that everyone has. A smart phone. No dependencies on subscriptions or thumbing through several cookbooks.
</p>
<p>
    This is a flask server using:
</p>

* FlatPages to display recipes stored in JSON files
* EasyOCR for adding text from physical cookbooks through a simple photo

<h2>
    Features to Come
</h2>

* Selenium to scrape new recipes, adding to the JSON files
    * This is meant to be a web tool for those that don't understand programming, breaking it down into usable bites that will scrape an entire website for you.
* Accounts for family members
    * A basic account system with just a username and a password to favorite recipes and suggest ones for making food in the future
* Meal Plan with suggestions
    * A weekly mealplan page for food to be added by the primary cook, or suggested by those that aren't the primary cook
* Shopping list
    * A shopping list adding the primary ingredients up so whomever is shopping that week can understand what is needed from the store/shopping market.
    * If integration with a local store's marketplace API is possible, then that'd be cool, but don't get hopes up. Pretty sure walmart and other stores have it blocked when not going through the website like normal. Doubt selenium would be useful without a metric ton of work.

    