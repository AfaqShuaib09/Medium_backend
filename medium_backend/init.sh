file=db.sqlite3
if [ -e "$file" ]; then
  # remove file if $file exists
  rm $file
fi

# User credentials
user=admin
email=admin@admin.com
password=admin

python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$user', '$email', '$password')" | python3 manage.py shell