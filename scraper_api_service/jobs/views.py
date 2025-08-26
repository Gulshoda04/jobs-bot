from rest_framework import generics, filters
from .models import Job
from .serializers import JobSerializer
from rest_framework.pagination import PageNumberPagination

class JobPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    pagination_class = JobPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'company']

class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
