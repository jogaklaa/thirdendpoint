from django.db import models
from django.contrib.postgres.fields import JSONField


class Fabrication(models.Model):
    # TODO(Consider using a UUIDField as the primary key.)

    # The sample id will be extracted from JSON.
    sample_id = models.CharField(max_length=255, blank=True)

    # The shared location is the path to the files transferred via 
    # Globus.
    # TODO(Consider using a FilePathField rather than a CharField.)
    shared_location = models.CharField(max_length=255, blank=True)

    metadata = JSONField(default=dict)

    date_received = models.DateTimeField(auto_now_add=True)

    # # TODO(Implement these fields.)
    #
    # # The protected location is a directory not accessible via Globus.
    # # Files will be kept there as insurance against user errors or 
    # # deliberate sabotage.
    # protected_location = models.CharField(max_length=255, blank=True)
    #
    # # The checksum will be used to ensure files are completely received.
    # # It may also be used to check whether redundant service calls need
    # # to be handled.
    # checksum = models.IntegerField(null=True, blank=True)


class XRD(models.Model):
    fabrication = models.ForeignKey('Fabrication', null=True, blank=True,
        related_name='xrd_characterizations')
    shared_location = models.CharField(max_length=255, blank=True)
    metadata = JSONField(default=dict)
    # TODO(Consider making similar updates as in Fabrication.)


class Queue(models.Model):
    # NOTE: treat the id field as a ticket number.
    
    xrd = models.ForeignKey('XRD', null=True, blank=True,
        related_name='queued_jobs')
    date_added = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    SAMPLE_NOT_RECEIVED = 1
    STARTED = 2
    COMPLETED = 3
    status_choices = (
        (SAMPLE_NOT_RECEIVED, 'physical sample not received'),
        (STARTED, 'started'),
        (COMPLETED, 'completed')
    )
    status = models.IntegerField(choices=status_choices, default=STARTED)