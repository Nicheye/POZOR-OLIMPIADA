
from rest_framework import serializers
from . models import *
class Country_serializer(serializers.ModelSerializer):
	class Meta:
		model=Country
		fields=['name','alpha2','alpha3','region']


from django.contrib.auth.hashers import make_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
   

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError("Old password is incorrect.")
        
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance
    

class Publication_Serializer(serializers.ModelSerializer):
     created_by = serializers.SerializerMethodField()
     created_at = serializers.SerializerMethodField()
     class Meta:
          model = Publication
          fields = ['title','theme','text','created_by','created_at','likesCount','dislikesCount']
     def get_created_by(self,obj):
          return str(obj.created_by.username)
     def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    