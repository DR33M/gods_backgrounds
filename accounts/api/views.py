from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


class Profile(APIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User doesn\'t exist.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        if user.is_staff:
            return Response({'message': 'You can\'t ban another admin.'}, status=status.HTTP_403_FORBIDDEN)
        if not user.is_active:
            return Response({'message': 'User has already been banned'}, status=status.HTTP_202_ACCEPTED)
        user.is_active = False
        user.save()
        [s.delete() for s in Session.objects.all() if str(s.get_decoded().get('_auth_user_id')) == str(user.id)]
        return Response({'message': 'User has been banned.', 'status': 'success'}, status=status.HTTP_202_ACCEPTED)
