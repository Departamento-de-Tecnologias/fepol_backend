from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from event.serializers import *


"""Para poder acceder al orden de los elementos se escribe ?ord=dsc o ?ord=asc al final de la consulta
ejemplo:    http://127.0.0.1:8000/api/eventos/?ord=dsc
En caso de mas variables se usa el operador &
ejemplo:    http://127.0.0.1:8000/api/eventos/?ordering=dsc&search=A0"""


class EventViewSet(viewsets.ModelViewSet):
    serializer_class=EventSerializer
    queryset=Event.objects.all()
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['date_start']
    search_fields = ['event_type']


class EventList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get_by_type_objects(self, id_organization, event_type):
        try:
            return Event.objects.filter(id_suborg_in_charge=id_organization).filter(event_type=event_type)
        except Event.DoesNotExist:
            raise Http404

    def get_by_order_objects(self, order):
        try:
            if(order=='dsc'):
                return Event.objects.order_by('-date_start')
            if(order=='asc'):
                return Event.objects.order_by('date_start')
        except Event.DoesNotExist:
            raise Http404
 
    def get(self, request, pk=None, order=None, id_organization=None, event_type=None, format=None):
       
        if pk:
            event = self.get_object(pk)
            serializer = EventSerializer(event)
        
        if order:
            events = self.get_by_order_objects(order)
            serializer = EventSerializer(events, many=True)
        if id_organization and event_type:
            events = self.get_by_type_objects(id_organization, event_type)
            serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class=DocumentSerializer
    queryset=Document.objects.all()
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['name']
    search_fields=['doc_type']


class DocumentList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        docs = Document.objects.all()
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    def get_by_order(self, order):
        try:
            if(order=='dsc'):
                return Document.objects.order_by('-name')
            if(order=='asc'):
                return Document.objects.order_by('name')
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, order=None,format=None):
        if pk:
            docs = self.get_object(pk)
            serializer = DocumentSerializer(docs)
        if order:
            events = self.get_by_order(order)
            serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        docs = self.get_object(pk)
        serializer = DocumentSerializer(docs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        docs = self.get_object(pk)
        docs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)