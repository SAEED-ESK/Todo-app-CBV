from rest_framework import serializers
from django.contrib.auth.models import User
from ...models import Todo

class TodoSerializer(serializers.ModelSerializer):
    todo_url = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['id', 'user','todo_url', 'title', 'complete', 'updated_date']
        read_only_fields = ['user', 'created_date']

    def get_todo_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('todo_url')
        return rep

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=self.context.get('request').user.id)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['user'] = User.objects.get(id=self.context.get('request').user.id)
        return super().update(instance, validated_data)