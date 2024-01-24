#use "uwsgi --http :5000 --wsgi-file wsgi.py"
from src import create_app

application = create_app()