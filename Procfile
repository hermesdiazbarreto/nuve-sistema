web: python backend/almacen/manage.py migrate --noinput && python backend/almacen/manage.py collectstatic --noinput && cd backend/almacen && gunicorn almacen.wsgi --bind 0.0.0.0:$PORT --log-file -
