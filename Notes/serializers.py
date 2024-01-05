from rest_framework import serializers
from Auth.serializers import CustomUtilsUserSerializer
from .models import Notes, Share_Notes


class NotesSerializer(serializers.ModelSerializer):
    user = CustomUtilsUserSerializer(source='U_id', read_only=True)

    class Meta:
        model = Notes
        fields = ['N_id', 'title', 'description', 'pub_date', 'updated_date',  'U_id', 'user']

    # Make pub_date optional
    extra_kwargs = {'pub_date': {'required': False},
	                'U_id': {'required': False},
                    'updated_date': {'required': False},
	                }
    def create(self, validated_data):
        # The 'user' field is already included in the validated_data
        return Notes.objects.create(**validated_data)




class NoteShare_Serializer(serializers.Serializer):
    recipient_username = serializers.CharField()



class ShareDetails_Serializer(serializers.ModelSerializer):
    sender = CustomUtilsUserSerializer(source='sender_id', read_only=True)
    recipient = CustomUtilsUserSerializer(source='recipient_id', read_only=True)

    class Meta:
        model = Share_Notes
        fields = ['Share_id', 'Note_id', 'sender', 'recipient', 'shared_at']
    

