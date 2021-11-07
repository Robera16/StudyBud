from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room # the model that we want to create a form for
        fields = '__all__'

# now we can also create a room from home route create Room link in addition to the admin panel