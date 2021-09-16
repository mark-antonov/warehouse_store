#!/usr/bin/env sh

set -o errexit
set -o nounset

if [ -z "$DJANGO_ENV" ]; then
  echo "ERROR: DJANGO_ENV is Empty"
  echo 'Application will not start.'
  exit 1
fi

echo "ENV is $DJANGO_ENV"
if [ "$DJANGO_ENV" = 'dev' ]; then
  echo "Run manage.py migrate"
  python /code/manage.py migrate --noinput
  echo "Run manage.py collectstatic"
  python /code/manage.py collectstatic --noinput
#  echo "Flushing database"
#  python /code/manage.py flush --noinput
#  echo "Importing test data"
#  python /code/manage.py loaddata test_data.json
  echo "Run server"
  exec  python -Wd manage.py runserver 0.0.0.0:8002
else
  echo "ERROR: DJANGO_ENV isn't valid"
  echo 'Application will not start.'
  exit 1
fi