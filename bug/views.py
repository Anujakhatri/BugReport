from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BugReport
from .serializers import BugReportSerializer


def index(request):
    return render(request, 'bug.html')


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def bug_list_create_view(request):
    if request.method == 'GET':
        bugs = BugReport.objects.all()
        serializer = BugReportSerializer(bugs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
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

    elif request.method==('PUT','PATCH'):
        partial = request.method == 'PATCH'
        serializer=BugReportSerializer(bug, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    elif request.method=='DELETE':
        bug.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)