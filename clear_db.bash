find any/migrations -type f -name "*.py" ! -name "__init__.py" -delete
find any/migrations -type f -name "*.pyc" -delete
rm -f db.sqlite3