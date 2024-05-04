from django.shortcuts import render
from .models import Vendor, PurchaseOrder
from .serializer import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class VendorListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all().order_by('vendor_code')
    serializer_class = VendorSerializer

vendorListCreateView = VendorListCreateView.as_view()

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all().order_by('vendor_code')
    serializer_class = VendorSerializer

vendorRetrieveUpdateDeleteView = VendorRetrieveUpdateDeleteView.as_view()

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all().order_by('-issue_date')
    serializer_class = PurchaseOrderSerializer

purchaseOrderListCreateView = PurchaseOrderListCreateView.as_view()

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all().order_by('-issue_date')
    serializer_class = PurchaseOrderSerializer

purchaseOrderRetrieveUpdateDeleteView = PurchaseOrderRetrieveUpdateDeleteView.as_view()


class VendorPerformanceView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all().order_by('vendor_code')
    serializer_class = VendorSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'on_time_delivery_rate': serializer.data['on_time_delivery_rate'],
                 'quality_rating_avg': serializer.data['quality_rating_avg'],
                 'average_response_time': serializer.data['average_response_time'],
                 'fulfillment_rate': serializer.data['fulfillment_rate']})

vendorPerformanceView = VendorPerformanceView.as_view()

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all().order_by('-issue_date')
    serializer_class = PurchaseOrderSerializer
    
    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = request.data.get('acknowledgment_date')    #timezone.now()
        instance.save()
        response_times = PurchaseOrder.objects.filter(vendor=instance.vendor, acknowledgment_date__isnull=False).values_list('acknowledgment_date', 'issue_date').order_by('-issue_date')
        average_response_time = sum(abs((ack_date - issue_date).total_seconds()) for ack_date, issue_date in response_times) #/ len(response_times)
        if response_times:
            average_response_time = average_response_time / len(response_times)
        else:
            average_response_time = 0  # Avoid division by zero if there are no response times
        instance.vendor.average_response_time = average_response_time
        instance.vendor.save()
        return Response({'acknowledgment_date': instance.acknowledgment_date})

acknowledgePurchaseOrderView = AcknowledgePurchaseOrderView.as_view()
