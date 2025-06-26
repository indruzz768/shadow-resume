from rest_framework import generics, permissions
from .models import Resume
from .serializers import ResumeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ai_service.utils import extract_skills

class ResumeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ResumeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extract_skills_api(request):
    text = request.data.get('text', '')
    
    if not text.strip():
        return Response({'error': 'No resume text provided.'}, status=400)

    skills = extract_skills(text) or []
    return Response({'skills': skills}, status=200)
