from rest_framework import mixins, viewsets

class CreteDestroyModelViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass