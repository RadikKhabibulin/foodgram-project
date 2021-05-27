sleep 10
echo run migrate
python manage.py migrate

echo run loaddata
python manage.py loaddata --exclude contenttypes fixtures.json

echo run gunicorn
gunicorn foodgram.wsgi:application --bind 0.0.0.0:5002

exec "$@"