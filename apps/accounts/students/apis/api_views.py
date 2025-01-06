from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.accounts.students.models import Student
from apps.accounts.students.serializers import ListGetStudentSerializers, StudentSerializer, UpdateStudentSerializers
from apps.utils.permissions import IsAdminOrOwner


class CreateStudentAPIView(CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentViewSet(ModelViewSet):
    """
    A viewset that provides `update`, `list`, and `destroy` actions for Students.
    """
    queryset = Student.objects.filter(user__is_delete=False)
    serializer_class = ListGetStudentSerializers
    permission_classes = [IsAuthenticated,IsAdminOrOwner]
    http_method_names =  ['get', 'patch', 'delete',] 
    

    def get_queryset(self):
        """
        Restrict queryset to the authenticated user unless the user is admin.
        """
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Use different serializer class for different methods
        """
           
        if self.request.method in ["PATCH"]:
            return UpdateStudentSerializers
        return super().get_serializer_class()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete()
        return super().destroy(request, *args, **kwargs)