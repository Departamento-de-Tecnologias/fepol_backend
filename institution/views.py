from django.shortcuts import render

from event.models import Document
from .models import *
from .serializers import *

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from django.http import Http404
from django.core.exceptions import FieldError
from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend

class FacultyViewset(viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()


class FacultyList(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = Faculty.objects.all()
        serializer = FacultySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CareerViewset(viewsets.ModelViewSet):
    serializer_class = CareerSerializer
    queryset = Career.objects.all()


class CareerList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = Career.objects.all()
        serializer = CareerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CareerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationViewset(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        params = self.request.query_params
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        only = params.get('only')
        if only is not None:
            try:
                return Response(queryset.values_list(only))
            except FieldError:
                return Response({"request": "field not found"})
        else:
            return Response(serializer.data)


class AllMembersByOrgViewSet(viewsets.ModelViewSet):
    serializer_class = AllMembersByOrgSerializer
    def retrive(self, request, pk=None):
        queryset=SubOrganization.objects.filter(id_organization=pk).values('sub_org_id','name','members')
        return Response(queryset)

class OrganizationList(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = Organization.objects.all()
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetail(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        organization = self.get_object(pk)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubOrganizationViewset(viewsets.ModelViewSet):
    serializer_class = SubOrganizationSerializer
    queryset = SubOrganization.objects.all()
    filter_backends=[filters.SearchFilter]
    search_fields = ['id_organization__abbreviation']

class SubOrganizationList(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = SubOrganization.objects.all()
        serializer = SubOrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubOrganizationDetail(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return SubOrganization.objects.get(pk=pk)
        except SubOrganization.DoesNotExist:
            raise Http404

    def get_by_org_object(self, id_organization):
        try:
            return SubOrganization.objects.filter(id_organization=id_organization)
        except SubOrganization.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, id_organization=None, format=None):
        if pk:
            sub_org = self.get_object(pk)
            serializer = SubOrganizationSerializer(sub_org)
        if id_organization:
            sub_org = self.get_by_org_object(id_organization)
            serializer = SubOrganizationSerializer(sub_org, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sub_org = self.get_object(pk)
        serializer = SubOrganizationSerializer(sub_org, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sub_org = self.get_object(pk)
        sub_org.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
