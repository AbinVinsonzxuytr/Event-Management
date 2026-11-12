


from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from booking.models import Booking
import uuid
from events.models import Event


@receiver(post_save,sender=Booking)

def update_after_staus_changes(sender,instance,created,**kwargs):
    #create ticket code after payment

    if instance.status=="confirmed":
        code=f"TICK-{uuid.uuid4().hex[:8]}"
        instance.ticket_code=code
        instance.save(update_fields=['ticket_code'])

        event=instance.event
        event.available_seats=instance.seats
        event.save(update_fields=['available_seats'])

    elif instance.status=="cancelled":
        if instance.ticket_code:
            event=instance.event
            event.available_seats+=instance.seats
            event.save(update_fields=['available_seats'])

@receiver(post_delete, sender=Booking)
def update_seats_after_deletion(sender,instance,**kwargs):
    if instance.status=="confirmed":
        event = instance.event
        event.available_seats += instance.seats
        event.save(update_fields=['available_seats'])


