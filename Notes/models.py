from django.db import models
import uuid
from Auth.models import CustomUser 
from Notes.documents import create_notes_index


# Create your models here

class Notes(models.Model):
    N_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    U_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to link with the User model
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)  # Automatically updated on each save


create_notes_index()  # Call this function when you want to create or update the index



class Share_Notes(models.Model):
    Share_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Note_id = models.ForeignKey(Notes, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(CustomUser, related_name='sent_shares', on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(CustomUser, related_name='received_shares', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Share from {self.sender_id.userName} to {self.recipient_id.userName} for Note {self.note_id.title}'