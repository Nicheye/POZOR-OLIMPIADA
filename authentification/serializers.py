from rest_framework import serializers
from .models import User,Friend_Link
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields =['id','username','password','name','last_name','age']
		extra_kwargs = {
			'password':{'write_only':True}
		}

	def create(self,validated_data):
		password = validated_data.pop('password',None)
		instance =  self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

class Friend_Link_Serializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Friend_Link
        fields = ['receiver', 'created_at']

    def get_receiver(self, obj):
					try:
						user = obj.receiver
						user_ser = UserSerializer(user)
						return user_ser.data
					except:
						return None
			

