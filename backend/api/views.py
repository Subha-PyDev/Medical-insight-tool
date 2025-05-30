from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from .models import Document
from .serializers import DocumentSerializer

class DocumentUploadView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Upload endpoint is active. Use POST to upload files."})

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentListView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentQueryView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        matching_documents = Document.objects.filter(name__icontains=query)
        serializer = DocumentSerializer(matching_documents, many=True)
        return Response(serializer.data)

class DocumentDeleteView(DestroyAPIView):
    queryset = Document.objects.all()
    lookup_field = 'id'
    serializer_class = DocumentSerializer
