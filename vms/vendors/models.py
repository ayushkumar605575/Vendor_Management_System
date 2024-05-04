from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, F
from django.utils import timezone

class Vendor(models.Model):
    """
    A model representing a vendor in the system.

    Attributes:
        vendor_code (CharField): A unique identifier for the vendor.
        name (CharField): The name of the vendor.
        contact_details (TextField): The contact details of the vendor.
        address (TextField): The address of the vendor.
        on_time_delivery_rate (FloatField): The on-time delivery rate of the vendor.
        quality_rating_avg (FloatField): The average quality rating of the vendor.
        average_response_time (FloatField): The average response time of the vendor.
        fulfillment_rate (FloatField): The fulfillment rate of the vendor.

    Methods:
        __str__(self):
            Returns a string representation of the vendor, using its name.
    """
    vendor_code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        """
        Returns a string representation of the vendor, using its name.

        Args:
            self: An instance of the Vendor class.

        Returns:
            str: A string representation of the vendor's name.
        """
        return self.name


class PurchaseOrder(models.Model):
    """
    A class that represents a purchase order in the system.

    Attributes:
        po_number (str): The unique number of the purchase order.
        vendor (Vendor): The vendor associated with this purchase order.
        order_date (datetime): The date when the purchase order was created.
        delivery_date (datetime, optional): The expected delivery date of the purchase order.
        delivered_data (datetime, optional): The actual delivery date of the purchase order.
        items (dict): A JSON object containing details of the items ordered.
        status (str): The current status of the purchase order.
        quality_rating (float, optional): The quality rating of the purchase order.
        issue_date (datetime, optional): The date when the purchase order was issued.
        acknowledgment_date (datetime, optional): The date when the purchase order was acknowledged.

    Methods:
        __str__(self):
            Returns a string representation of the purchase order, using its unique number.
    """
    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_data = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the purchase order, using its unique number.

        Args:
            self: An instance of the PurchaseOrder class.

        Returns:
            str: A string representation of the purchase order's unique number.
        """
        return self.po_number
    

# from django.db.models import Avg, Count, F, Q
# from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    orders = PurchaseOrder.objects.filter(vendor=vendor)
    completed_orders = orders.filter(status='completed')
    
    # Update On-Time Delivery Rate
    on_time_count = completed_orders.filter(delivery_date__gte=F('delivered_data')).count()
    on_time_delivery_rate = on_time_count / completed_orders.count() if completed_orders.exists() else 0
    
    # Update Quality Rating Average
    quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    
    # Update Average Response Time
    response_times = orders.filter(acknowledgment_date__isnull=False).annotate(
        response_time=F('acknowledgment_date') - F('issue_date')
    ).aggregate(average_response_time=Avg('response_time'))
    average_response_time = response_times['average_response_time'].total_seconds() / 3600 if response_times['average_response_time'] else 0
    
    # Update Fulfillment Rate
    fulfillment_rate = completed_orders.count() / orders.count() if orders.exists() else 0
    
    # Apply updates
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()


# @receiver(post_save, sender=PurchaseOrder)
# def update_vendor_performance(sender, instance, **kwargs):
#     """
#     This method is a post-save signal receiver that updates the vendor's performance metrics.
#     It is triggered when a PurchaseOrder instance is saved.

#     Args:
#         sender (type): The sender of the signal, which is the PurchaseOrder model.
#         instance (PurchaseOrder): The instance of the PurchaseOrder model that triggered the signal.
#         **kwargs: Additional keyword arguments passed to the signal receiver.

#     Updates the following vendor performance metrics:

#         - On-Time Delivery Rate: Calculates the percentage of orders delivered on time.
#         - Quality Rating Average: Calculates the average quality rating of the vendor's orders.

#     If the PurchaseOrder instance has a status of 'completed' and the delivered_data field is None, the method sets the delivered_data field to the current date and time.

#     If the vendor has completed orders, the method calculates the On-Time Delivery Rate and Quality Rating Average. The On-Time Delivery Rate is the ratio of on-time deliveries to the total number of completed orders. The Quality Rating Average is the average quality rating of the completed orders.

#     The method updates the vendor's performance metrics by setting the appropriate fields on the vendor instance and saving the instance.
#     """

#     if instance.status == 'completed' and instance.delivered_data is None:
#         instance.delivered_data = timezone.now()
#         instance.save()

#     # Update On-Time Delivery Rate
#     completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
#     on_time_deliveries = completed_orders.filter(delivery_date__gte=F('delivered_data'))
#     if completed_orders.count() == 0:
#         on_time_delivery_rate = None
#     else:
#         on_time_delivery_rate = on_time_deliveries.count() / completed_orders.count()
#     instance.vendor.on_time_delivery_rate = on_time_delivery_rate or 0

#     # Update Quality Rating Average
#     completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
#     quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
#     instance.vendor.quality_rating_avg = quality_rating_avg or 0
#     instance.vendor.save()


class HistoricalPerformance(models.Model):
    """
    A model representing the historical performance of a vendor.

    Attributes:
        vendor (ForeignKey): The vendor associated with this historical performance record.
        date (DateTimeField): The date when the historical performance data was recorded.
        on_time_delivery_rate (FloatField): The on-time delivery rate of the vendor at the time of this record.
        quality_rating_avg (FloatField): The average quality rating of the vendor's orders at the time of this record.
        average_response_time (FloatField): The average response time of the vendor at the time of this record.
        fulfillment_rate (FloatField): The fulfillment rate of the vendor at the time of this record.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


# @receiver(post_save, sender=PurchaseOrder)
# def update_response_time(sender, instance, **kwargs):
#     """
#     This method is a post-save signal receiver that updates the vendor's response time metric.
#     It is triggered when a PurchaseOrder instance is saved.

#     Args:
#         sender (type): The sender of the signal, which is the PurchaseOrder model.
#         instance (PurchaseOrder): The instance of the PurchaseOrder model that triggered the signal.
#         **kwargs: Additional keyword arguments passed to the signal receiver.

#     Updates the following vendor performance metrics:

#     - Average Response Time: Calculates the average response time of the vendor's orders.

#     If the PurchaseOrder instance has an acknowledgment_date field that is not None, the method calculates the average response time. The average response time is the average time taken by the vendor to acknowledge the purchase order after issuing it.

#     The method updates the vendor's performance metrics by setting the appropriate fields on the vendor instance and saving the instance.
#     """
#     response_times = PurchaseOrder.objects.filter(vendor=instance.vendor, acknowledgment_date__isnull=False).values_list('acknowledgment_date', 'issue_date')
#     average_response_time = sum((ack_date - issue_date ).total_seconds() for ack_date, issue_date in response_times)   #/ len(response_times)
#     average_response_time = max(average_response_time, 0)
#     if response_times:
#         average_response_time = average_response_time / len(response_times)
#     else:
#         average_response_time = 0  # Avoid division by zero if there are no response times
#     instance.vendor.average_response_time = average_response_time
#     instance.vendor.save()

# @receiver(post_save, sender=PurchaseOrder)
# def update_fulfillment_rate(sender, instance, **kwargs):
#     """
#     This method is a post-save signal receiver that updates the vendor's fulfillment rate metric.
#     It is triggered when a PurchaseOrder instance is saved.

#     Args:
#         sender (type): The sender of the signal, which is the PurchaseOrder model.
#         instance (PurchaseOrder): The instance of the PurchaseOrder model that triggered the signal.
#         **kwargs: Additional keyword arguments passed to the signal receiver.

#     Updates the following vendor performance metrics:

#     - Fulfillment Rate: Calculates the percentage of orders completed by the vendor.

#     If the PurchaseOrder instance has a status of 'completed', the method calculates the fulfillment rate. The fulfillment rate is the ratio of completed orders to the total number of orders placed with the vendor.

#     The method updates the vendor's performance metrics by setting the appropriate fields on the vendor instance and saving the instance.
#     """
#     completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
#     fulfillment_rate = completed_orders.count() / PurchaseOrder.objects.filter(vendor=instance.vendor).count()
#     instance.vendor.fulfillment_rate = fulfillment_rate
#     instance.vendor.save()

