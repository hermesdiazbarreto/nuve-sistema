release: python backend/almacen/manage.py migrate --noinput
web: cd backend/almacen && gunicorn almacen.wsgi --bind 0.0.0.0:$PORT --log-file -
