from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.accounts.students.serializers import StudentSerializer

class CreateStudentAPIView(CreateAPIView):
    serializer_class = StudentSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
