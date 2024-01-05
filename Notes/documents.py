from django_elasticsearch_dsl import Document, fields, Index
# from .models import Notes
from elasticsearch_dsl import analyzer

class NotesDocument(Document):
    title = fields.TextField(analyzer=analyzer('standard'))
    description = fields.TextField(analyzer=analyzer('standard'))

    class Index:
        name = 'notes'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

def create_notes_index():
    notes_index = Index('notes')
    notes_index.settings(number_of_shards=1, number_of_replicas=0)
    notes_index.doc_type(NotesDocument)
    notes_index.create()
