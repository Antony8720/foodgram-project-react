import io
from django.db import models
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, views
from .mixins import CreteDestroyModelViewSet
from rest_framework.response import Response


class AddingDeletingViewSet(CreteDestroyModelViewSet):
    model_class = models.Model
    router_pk = 'id'
    error_text_create = 'Невозможно добавить запись'
    error_text_destroy = 'Невозможно удалить запись'
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.model_class, pk=self.kwargs.get(self.router_pk)
        )

    def is_on(self):
        pass

    @staticmethod
    def error(text):
        return Response(
            {
                'errors': text
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def create(self, request, *args, **kwargs):
        if self.is_on():
            return self.error(self.error_text_create)
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.is_on():
            return self.error(self.error_text_destroy)
        return super().destroy(request, *args, **kwargs)


class PdfGenerateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    font_path = './assets/FreeSans.ttf'
    filename = 'file.pdf'

    def get_text_lines(self):
        pass

    def get(self, request):
        buffer = io.BytesIO()
        pdfmetrics.registerFont(TTFont('Font', self.font_path))
        page = canvas.Canvas(buffer, pagesize=A4)
        page.setFont("Font", 14)
        text = page.beginText()
        text.setTextOrigin(80, 750)
        for text_line in self.get_text_lines():
            text.textLine(text=text_line)
        page.drawText(text)
        page.showPage()
        page.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=self.filename,
        )
           


