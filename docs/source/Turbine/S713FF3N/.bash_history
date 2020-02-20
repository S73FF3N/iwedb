cd development/
source env/bin/activate
git add .
git commit -m "monthly report adapted."
git push
cd development/
source env/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
cd development/
source env/bin/activate
python manage.py makemigrations
python manage.py migrate
cd development/
source env/bin/activate
git add .
git commit -m "sales report: last_of_next_month corrected"
git push
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
cd development/
source env/bin/activate
git add .
git commit -m "Gutachten: improvements"
git add .
git commit -m "projects: days_to_start corrected"
git push
git add .
git commit -m "actor: excel export"#
cd development/
source env/bin/activate
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
