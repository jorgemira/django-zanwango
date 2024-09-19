from rest_framework import viewsets

from zanwango import generics, mixins


class GenericReadViewSet(viewsets.ViewSetMixin, generics.GenericReadAPIView):
    pass


class GenericWriteViewSet(viewsets.ViewSetMixin, generics.GenericWriteAPIView):
    pass


class GenericViewSet(viewsets.ViewSetMixin, generics.GenericAPIView):
    pass


class ReadOnlyModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericReadViewSet
):
    pass
