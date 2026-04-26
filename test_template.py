import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_recommendation.settings')
django.setup()

from django.template import Template, Context
from apps.recommendations.forms import RecommendationRequestForm

from apps.farms.models import Farm
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()
if not user:
    user = User.objects.create(username="test")
form = RecommendationRequestForm(user=user)

# let's create a farm just to be sure
Farm.objects.get_or_create(user=user, name="test farm")

t1 = Template("{% if form.farm.queryset.count > 0 %}YES{% else %}NO{% endif %}")
print("t1:", t1.render(Context({'form': form})))

t2 = Template("{% if form.fields.farm.queryset.count > 0 %}YES{% else %}NO{% endif %}")
print("t2:", t2.render(Context({'form': form})))

t3 = Template("{% if form.farm.field.queryset.exists %}YES{% else %}NO{% endif %}")
print("t3:", t3.render(Context({'form': form})))
