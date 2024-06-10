import math

from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.core.files import File
from django.conf import settings

import stripe
from xhtml2pdf import pisa
from io import BytesIO

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import *
from .models import *
from .serializers import *
from .permissions import *


class PostViewSet(ModelViewSet):
    permission_classes = [PostPermission]
    filterset_fields = ["type"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()   
        return Post.objects.filter(is_approved=True)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostSerializer
    
class PostApplicationsViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    http_method_names = SAFE_METHODS
    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Application.objects.filter(post__id=post_pk)

class PostTaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsSuperUser | HasApplicantPaid | IsOrganization | IsSystemCoordinator]

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Task.objects.filter(post__id=post_pk)
    def get_serializer_context(self, *args, **kwargs):
        post_pk=self.kwargs.get("post_pk")
        return {'post_pk':post_pk, 'request': self.request }       

class TaskViewSet(ModelViewSet):
    serializer_class = TaskOnlySerializer
    queryset = Task.objects.all()

class TaskSectionsViewSet(ModelViewSet):
    serializer_class = TaskSectionSerializer

    def get_queryset(self):
        task_pk = self.kwargs.get("task_pk")
        return TaskSection.objects.filter(task__id=task_pk)
    def get_serializer_context(self, *args, **kwargs):
        task_pk=self.kwargs.get("task_pk")
        return {'task_pk':task_pk } 
    
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        task_pk = self.kwargs.get("task_pk")
        context = self.get_serializer_context()
        context['task_pk'] = task_pk
        
        serializer = self.get_serializer(data=request.data, context=context, many=is_many)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
    
class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_fields = ["applicant", "post", "status"]

class EvaluationViewSet(ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    http_method_names = SAFE_METHODS
    filterset_fields = ["applicant"]

class PostRequirementsViewSet(ModelViewSet):
    queryset= Requirement.objects.all()
    serializer_class = RequirementSerializer

    def get_serializer_context(self,*args,**kwargs):
        post_pk =  self.kwargs.get('post_pk')
        return {'post_pk':post_pk}
    
class PostStatusViewSet(ModelViewSet):
    queryset = PostStatus.objects.all()
    serializer_class = PostStatusSerializer
    filterset_fields = ["applicant", "post"]

class TaskStatusViewSet(ModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    filterset_fields = ["applicant", "task"]

class CertificateViewSet(ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filterset_fields = ["applicant", "post"]

    @action(detail=True, methods=['post'], url_path="generate-certificate")
    def generate_certificate(self, request, pk=None):
        certificate = self.get_object()
        certificate_serializer = self.get_serializer(certificate)

        if certificate.pdf_file:
            return Response({"error" : "Certificate already created"}, status=403)

        if certificate.post.is_paid:
            template = get_template('premium_certificate_template.html')
        else:
            template = get_template('certificate_template.html') 
        context = {'certificate': certificate_serializer.data}

        html = template.render(context)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.applicant.get_full_name()}_certificate.pdf"'
            certificate.pdf_file.save(f'{certificate.applicant.get_full_name()}_certificate.pdf', File(result), save=True)
            return response

        return Response({'error': 'Error generating PDF'}, status=500)
    
    @action(detail=True, methods=["delete"], url_path="delete-certificate")
    def delete_certificate(self, request, pk=None):
        certificate = self.get_object()

        if certificate.pdf_file:
            pdf_file_path = certificate.pdf_file.path
            certificate.pdf_file.delete()
            default_storage.delete(pdf_file_path)
            return Response({"message": "Certificate file deleted successfully"})
        else:
            return Response({"error": "No Certificate file exists for this certificate"}, status=404)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pdf_file = instance.pdf_file
        if pdf_file:
            file_path = pdf_file.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        return super().destroy(request, *args, **kwargs)


stripe.api_key = settings.STRIPE_SECRET_KEY

class ProcessPayment(APIView):
    def post(self, request, post_id):
        try:
            post_obj = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        unit_amount = int(math.ceil(post_obj.price * 100))

        products = stripe.Product.list()
        product = None
        for p in products:
            if p.name == post_obj.title:
                product = p
                break

        if product:
            product_id = product.id
        else:
            product = stripe.Product.create(
                name=post_obj.title,
                description=post_obj.description
            )
            product_id = product.id

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "unit_amount": unit_amount,
                            "currency": "usd",
                            "product": f"{product_id}"
                        },
                        'quantity': 1
                    }
                ],
                mode='payment',
                success_url=settings.FRONTEND_SUBSCRIPTION_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONTEND_SUBSCRIPTION_CANCEL_URL,
                metadata={
                    'post_id': str(post_obj.id) 
                }
            )
            return JsonResponse({'url': checkout_session.url}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)