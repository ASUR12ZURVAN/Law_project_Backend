from rest_framework import serializers
from .models import Document_Text

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_Text
        fields = '__all__'