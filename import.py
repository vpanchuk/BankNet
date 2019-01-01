import csv,sys,os, django

project_dir = os.getcwd() + os.sep + 'bankproject' + os.sep
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from banknet.models import Rating
data = csv.reader(open(project_dir + 'data' + os.sep + 'data.csv'), delimiter=',')
for row in data:
    rating = Rating()
    rating.full_name = row[0]
    rating.term = row[1]
    rating.volume = row[2]
    rating.risk_level = row[3]
    rating.credit_history = row[4]
    rating.wages = row[5]
    rating.save()