
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BugReport
from .serializer import BugReportSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def bug_report_view(request):
    bug_report = BugReport.objects.all()
    serializer = BugReportSerializer(bug_report, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def bug_report_post(request):

    serializer = BugReportSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def bug_report_detail(request, pk):
    try:
        bug = BugReport.objects.get(pk=pk)
        serializer = BugReportSerializer(bug, many=False)
        return Response(serializer.data)

    except BugReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BugReportSerializer(bug)
        return Response(serializer.data)

    # if request.method == 'PUT':
    #     serializer = BugReportSerializer(bug, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # if request.method == 'DELETE':
    #     bug = Bug_Report.objects.get(pk=pk)
    #     bug.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)