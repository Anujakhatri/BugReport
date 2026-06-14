from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BugReport
from .serializers import BugReportSerializer
from .ai_service import review_bug



def index(request):
    return render(request, 'bug.html')


# ── Duplicate check function ─────────────────────────
def check_duplicate(new_title, new_description):
    existing_bugs = BugReport.objects.filter(
        is_duplicate=False
    )
    new_title_words = set(new_title.lower().split())
    new_desc_words  = set(new_description.lower().split())

    for bug in existing_bugs:
        # Title similarity
        existing_title_words = set(bug.title.lower().split())
        common_title    = new_title_words & existing_title_words
        max_title_len = max(len(new_title_words), len(existing_title_words))
        title_similarity = len(common_title) / max_title_len if max_title_len > 0 else 0.0

        # Description similarity
        existing_desc_words = set(bug.description.lower().split())
        common_desc     = new_desc_words & existing_desc_words
        max_desc_len = max(len(new_desc_words), len(existing_desc_words))
        desc_similarity  = len(common_desc) / max_desc_len if max_desc_len > 0 else 0.0

        if title_similarity >= 0.6 or desc_similarity >= 0.6:
            return bug

    return None

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def bug_list_create_view(request):
    if request.method == 'GET':
        bugs = BugReport.objects.all()
        serializer = BugReportSerializer(bugs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        title = request.data.get('title', '')
        description = request.data.get('description', '')

        dublicate = check_duplicate(title, description)
        if dublicate:
            return Response({
                "is_duplicate": True,
                "message": "same bug report before",
                "existing_bug": {
                    "id": dublicate.id,
                    "title": dublicate.title,
                    "description" : dublicate.description,
                    "severity":    dublicate.severity,
                    "status":      dublicate.status,
                    "created_at":  str(dublicate.created_at),

                }
            }, status=status.HTTP_201_CREATED)

        #no dublicate
        serializer = BugReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([AllowAny])
def bug_detail_view(request, pk):
    try:
        bug = BugReport.objects.get(pk=pk)
    except BugReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer = BugReportSerializer(bug)
        return Response(serializer.data)

    elif request.method in ('PUT','PATCH'):
        partial = request.method == 'PATCH'
        serializer=BugReportSerializer(bug, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    elif request.method=='DELETE':
        bug.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def bug_ai_review(request, pk):
    try:
        bug = BugReport.objects.get(pk=pk)
    except BugReport.DoesNotExist:
        return Response({"error": "Bug not found"}, status=status.HTTP_404_NOT_FOUND)

    # Return cached review if it already exists
    if bug.ai_suggestion:
        return Response({"success": True, "review": bug.ai_suggestion}, status=status.HTTP_200_OK)

    # Call Groq AI service
    result = review_bug(
        title=bug.title,
        description=bug.description,
        severity=bug.severity,
        status=bug.status,
        reporter_info=bug.reporter_info or ""
    )

    # Cache the AI suggestion if successful
    if result.get("success"):
        bug.ai_suggestion = result["review"]
        bug.save()

    return Response(result)

