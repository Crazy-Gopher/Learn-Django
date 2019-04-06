from django.db import models

class SeqCounter(models.Model):
    counter_nbr = models.IntegerField(null=False, blank=True, default='0')
    counter_code = models.CharField(max_length=25, null=False, blank=True)
    class Meta:
        db_table='seq_counter'

class BerthType(models.Model):
    berth_type = models.CharField(max_length=25, null=False, unique=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table='berth_type'

class Coach(models.Model):
    coach_nbr = models.CharField(max_length=30, null=False, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table='coach'

class TicketStatus(models.Model):
    status_code = models.CharField(max_length=10, unique=True, blank=True, null = False)
    description = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table='ticket_status'
# Create your models here.


class PassangerDetail(models.Model):
    name = models.CharField(max_length = 100, null = False)
    age  = models.IntegerField(null = False, default = 18) 
    
    GENDER = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )
 
    gender= models.CharField(max_length=10, choices=GENDER, blank=True, default='M', null = False)
    berth_preference_id =  models.ForeignKey('BerthType', null = True,db_column = 'berth_preference_id', on_delete = models.SET_NULL)
    ticket_id =  models.ForeignKey('TicketDetail', null = True, db_column = 'ticket_id', on_delete = models.SET_NULL)
    with_child = models.BooleanField(default=False)
    
    class Meta:
        db_table='passanger_detail'
    
class TicketDetail(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    ticket_nbr =  models.CharField(max_length=30, null=False, unique=True)
    berth_type_id =  models.ForeignKey('BerthType', null = True, db_column = 'berth_type_id' ,on_delete = models.SET_NULL)
    status_id = models.ForeignKey('TicketStatus', null = True, db_column = 'status_id',on_delete = models.SET_NULL)
    coach_id = models.ForeignKey('Coach', null = True, db_column = 'coach_id',on_delete = models.SET_NULL)
    booked_ts  = models.DateTimeField(auto_now=True)
    mod_ts  = models.DateTimeField(auto_now=True)
    date_of_journey  = models.DateField(auto_now = True, null = False)

    class Meta:
        db_table='ticket_detail'

