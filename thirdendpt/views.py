from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from thirdendpt.models import (
    Fabrication, XRD, Queue 
)


def extract_sample_id(sample_metadata):
    # TODO(Remove hard-coding.)
    sample_id = None
    try:
        key = sample_metadata.keys()[0]
        sample_id = sample_metadata[key]['sample']['identifier']['id']
    except Exception:
        pass
    return sample_id


def create_xrd_shared_location(fabrication):
    # stub
    return ''


def get_characterization_metadata():
    # stub
    return {
        'haiku': {
            'author': 'Yosa Buson',
            'stanzas': [
                {
                    'lines': [
                        'A summer river being crossed',
                        'how pleasing',
                        'with sandals in my hands!',
                    ]
                },
                {
                    'lines': [
                        'Light of the moon',
                        "Moves west, flowers' shadows",
                        'Creep eastward.',
                    ]
                },
                {
                    'lines': [
                        'In the moonlight,',
                        'The color and scent of the wisteria',
                        'Seems far away.',
                    ]
                }
            ]
        }
    }


def process_sample(sample, short_info):
    # Create fabrication record.
    filepath = sample.pop('globusPath')
    sample_metadata = sample
    sample_id = extract_sample_id(sample_metadata)
    short_info['sample_ids'].append(sample_id)
    fabrication = Fabrication(
        sample_id=sample_id,
        metadata=sample_metadata,
        shared_location=filepath
    )
    fabrication.save()
    short_info['fabrication_ids'].append(fabrication.pk)
    # Create xrd record.
    xrd_shared_location = create_xrd_shared_location(fabrication)
    xrd = XRD(
        fabrication=fabrication,
        shared_location=xrd_shared_location
    )
    xrd.save()
    short_info['characterization_ids'].append(xrd.pk)
    # Add to processing queue.
    queue = Queue(
        xrd=xrd
    )
    queue.save()
    # Process item in queue and update queue record.
    queue.status = Queue.COMPLETED
    queue.date_completed = datetime.now()
    queue.save()
    short_info['characterization_statuses'].append('completed')
    # Update xrd record.
    xrd.metadata = get_characterization_metadata()
    xrd.save()


class FabricationData(APIView):
    def post(self, request, format=None):
        """Receive fabrication data from other lims system."""
        fabrication_data = request.data
        fab_ids = []
        xrd_ids = []
        result = {
            'sample_ids': [],
            'fabrication_ids': [],
            'characterization_ids': [],
            'characterization_statuses': []
        }
        for sample in fabrication_data:
            process_sample(sample, result)
        return Response(result)