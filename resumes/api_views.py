from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Resume
from .serializers import ResumeSerializer
from .utils import extract_skills

class ResumeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        text = f"{resume.summary or ''}\n{resume.experience or ''}\n{resume.projects or ''}"
        skills = extract_skills(text)
        resume.skills = ", ".join(skills)
        resume.save()

class ResumeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        resume = serializer.save()
        text = f"{resume.summary or ''}\n{resume.experience or ''}\n{resume.projects or ''}"
        skills = extract_skills(text)
        resume.skills = ", ".join(skills)
        resume.save()

class ExtractSkillsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        text = request.data.get("text", "")
        if not text.strip():
            return Response({"error": "Text is required."}, status=400)

        skills = extract_skills(text)
        return Response({'skills': skills}, status=200)
