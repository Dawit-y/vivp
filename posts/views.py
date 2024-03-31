from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.files import File

from xhtml2pdf import pisa
from io import BytesIO

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class PostApplicationsViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Application.objects.filter(post__id=post_pk)

class PostTaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Task.objects.filter(post__id=post_pk)
    def get_serializer_context(self, *args, **kwargs):
        post_pk=self.kwargs.get("post_pk")
        return {'post_pk':post_pk }       

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class TaskSectionsViewSet(ModelViewSet):
    serializer_class = TaskSectionSerializer
    def get_queryset(self):
        task_pk = self.kwargs.get("task_pk")
        return TaskSection.objects.filter(task__id=task_pk)
    def get_serializer_context(self, *args, **kwargs):
        task_pk=self.kwargs.get("task_pk")
        return {'task_pk':task_pk } 
    
class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_fields = ["applicant", "post", "status"]

class CertificateViewSet(ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filterset_fields = ["applicant", "post"]

    @action(detail=True, methods=['post', "delete"], url_path="generate-pdf")
    def generate_pdf(self, request, pk=None):
        certificate = self.get_object()
        certificate_serializer = self.get_serializer(certificate)

        if request.method == 'DELETE':
            # Delete the PDF file associated with the certificate
            if certificate.pdf_file:
                pdf_file_path = certificate.pdf_file.path
                certificate.pdf_file.delete()
                default_storage.delete(pdf_file_path)
                return Response({"message": "Certificate file deleted successfully"})
            else:
                return Response({"error": "No Certificate file exists for this certificate"}, status=404)

        if certificate.pdf_file:
            return Response({"error" : "Certificate already created"}, status=403)

        template = get_template('certificate_template.html')
        context = {'certificate': certificate_serializer.data}

        html = template.render(context)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.applicant.first_name}_certificate.pdf"'
            certificate.pdf_file.save(f'{certificate.applicant.first_name}_certificate.pdf', File(result), save=True)
            return response

        return Response({'error': 'Error generating PDF'}, status=500)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pdf_file = instance.pdf_file
        if pdf_file:
            file_path = pdf_file.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        return super().destroy(request, *args, **kwargs)

class EvaluationViewSet(ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    filterset_fields = ["applicant", "task"]

class PostRequirementsViewSet(ModelViewSet):
    queryset= Requirement.objects.all()
    serializer_class = RequirementSerializer

    def get_serializer_context(self,*args,**kwargs):
        post_pk =  self.kwargs.get('post_pk')
        return {'post_pk':post_pk}

