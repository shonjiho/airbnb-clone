import os

# User Seed
os.system("python manage.py seed_users --number 50")
# Room Seed
os.system("python manage.py seed_amenities")
os.system("python manage.py seed_facilities")
os.system("python manage.py seed_house_rules")
os.system("python manage.py seed_room_types")
os.system("python manage.py seed_rooms --number 50")

# reviews Seed
os.system("python manage.py seed_reviews --number 100")
os.system("python manage.py seed_reservations --number 50")
