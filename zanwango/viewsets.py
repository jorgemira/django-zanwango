from rest_framework import viewsets

from zanwango import generics


class GenericReadViewSet(viewsets.ViewSetMixin, generics.GenericReadAPIView):
    pass
