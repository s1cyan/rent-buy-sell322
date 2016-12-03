import os

INSTRUCTIONS = ('rm db.sqlite3',
                'rm rbs_application/migrations/000*.py',
                'python manage.py makemigrations',
                'python manage.py migrate',
                'python manage.py populate_db',
                'python manage.py runserver')

for line in INSTRUCTIONS:
    os.system(line)
