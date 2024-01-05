from . import views
from django.urls import path

urlpatterns = [
    path('notes/create-note', views.create_note, name='create-note'),
    path('notes/AllNotes-by-user', views.AllNotes_by_user, name='all_notes_by_user'),
    path('notes/get-note/<uuid:uid>', views.get_note, name='get-note'),
    path('notes/update-note/<uuid:uid>', views.update_note, name='update-note'),
    path('notes/delete-note/<uuid:uid>', views.delete_Note, name='Delete-note'),
    path('notes/<uuid:note_id>/share-note', views.share_note, name='share-note'),
    path('search', views.note_search, name='search-note'),
]
