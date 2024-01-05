from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Auth.token_utils import get_user_id_from_token
from Auth.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotesSerializer, NoteShare_Serializer, ShareDetails_Serializer
from .models import Notes, Share_Notes
from .documents import create_notes_index, NotesDocument

# Create your views here.

#-----view to create questions-----
@api_view(['POST'])
def create_note(request):
    # Get user ID from token
    user_id = get_user_id_from_token(request)
    print(user_id)

    if user_id is not None:
        # Retrieve user instance based on user ID
        try:
            user = CustomUser.objects.get(U_id=user_id)
            print(user)

            # Create a new question with user association
            request.data['U_id'] = user_id
            deserializer = NotesSerializer(data=request.data, partial=True)
            if deserializer.is_valid():
            # serializer.validated_data['user'] = user  # Associate the question with the user
                deserializer.save()
                return Response({'data' : deserializer.data, 'api_status' : True}, status=status.HTTP_201_CREATED)
        
            else:
                return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)






@api_view(['GET'])
def AllNotes_by_user(request):
    user_id = get_user_id_from_token(request)
    if user_id is not None:
        try:
                # Retrieve questions for the specified user
                notes = Notes.objects.filter(U_id=user_id)
        
                # Serialize the questions
                serializer = NotesSerializer(notes, many=True)
        
                return Response({'data':serializer.data, 'api_status':True}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    




@api_view(['GET'])
def get_note(request, uid):
    user_id = get_user_id_from_token(request)
    print('flag1')
    if user_id is not None:
        try:
            # Retrieve questions for the specified user
            notes = Notes.objects.filter(N_id=uid)
            print('flag2')
        
            # Serialize the questions
            serializer = NotesSerializer(notes, many=True)
            print('flag3')
            print(serializer)
        
            return Response({'data':serializer.data, 'api_status':True}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)





@api_view(['PUT'])
def update_note(request, uid):
    user_id = get_user_id_from_token(request)
    if user_id is not None:
        # Retrieve user instance based on user ID
        try:
            user = CustomUser.objects.get(U_id=user_id)
            
            note = Notes.objects.get(N_id=uid)
            deserializer = NotesSerializer(instance=note, data=request.data, partial=True)
            print('flag2')
            if deserializer.is_valid():
                deserializer.save()
                return Response({'data' : deserializer.data, 'api_status' : True}, status=status.HTTP_201_CREATED)
        
            else:
                return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['DELETE'])
def delete_Note(request,uid):
    user_id = get_user_id_from_token(request)
    if user_id is not None:
        try:
            note = Notes.objects.get(N_id=uid)
            if str(user_id) == str(note.U_id):    # note  convert  <class 'restAPI.models.CustomUser'> = question.user_id  in to string 
                return Response({"error": "You do not have permission to delete this question.",
                "userids" :f"user->{type(user_id)} note-> {type(note.U_id)}"
                }, status=status.HTTP_403_FORBIDDEN)

            # Delete the question
            note.delete()

            return Response({"message": f"Note with id {uid} deleted successfully"
            "userids"
            }, status=status.HTTP_204_NO_CONTENT)

        except Notes.DoesNotExist:
            return Response({"error": "Notes not found"}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    




@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def share_note(request, note_id):
    user_id = get_user_id_from_token(request)

    if user_id is not None:
        try:
            note = Notes.objects.get(N_id=note_id)
        except Notes.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)    

         # Check if the authenticated user is the owner of the note
        if str(note.U_id_id) != str(user_id) :
            return Response({"error" : "You are not the owner of this note"}, status=status.HTTP_403_FORBIDDEN)

        serializer = NoteShare_Serializer(data=request.data)

        if serializer.is_valid():
            recipient_username = serializer.validated_data['recipient_username']
        
            try:
                recipient_user = CustomUser.objects.get(userName=recipient_username)
            except CustomUser.DoesNotExist:
                return Response({"error": "Recipient user not found"}, status=status.HTTP_404_NOT_FOUND)

             # Retrieve the sender user instance using the user_id obtained from the token
            try:
                sender_user = CustomUser.objects.get(U_id=user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "Sender user not found"}, status=status.HTTP_404_NOT_FOUND)
            
            
             # Create a Share record
            share_instance = Share_Notes.objects.create(Note_id_id=note.N_id, sender_id_id=user_id, recipient_id_id=recipient_user.U_id)

            # Serialize the Share instance and return it in the response
            deserializer = ShareDetails_Serializer(share_instance)
            return Response({'data' : deserializer.data, 'message': 'Note shared successfully', 'api_status': True}, status=status.HTTP_200_OK)

        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    


# Ensure the Elasticsearch index is created or updated
create_notes_index()


@api_view(['GET'])
def note_search(request):
    user_id = get_user_id_from_token(request)

    if user_id is not None:
        
        #Search for notes based on keywords for the authenticated user.
        query = request.GET.get('q', 'what')
    
        if not query:
            return Response({'error': 'Please provide a search query'}, status=status.HTTP_400_BAD_REQUEST)
        
        search_results = NotesDocument.search().query("multi_match", query=query, fields=["title", "description"])

        # notes = Notes.objects.filter(title__icontains=query) | Notes.objects.filter(description__icontains=query)
        notes = [hit.to_dict() for hit in search_results]
        serializer = NotesSerializer(notes, many=True)

        return Response({'data' : serializer.data, 'message':'Success', 'api_status':True}, status=status.HTTP_200_OK)
    
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)