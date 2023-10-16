from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, \
                                  RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from .models import File
from .serializers import FileSerializer
from .tasks import process_file
from base.celery import debug_task

class FileViewSet(ListModelMixin, 
                RetrieveModelMixin,
                UpdateModelMixin,
                DestroyModelMixin,GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileUploadViewSet(CreateModelMixin,
                  GenericViewSet):
    
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        file = serializer.save()
        process_file.apply_async(args=[file.id])
        debug_task.delay()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


