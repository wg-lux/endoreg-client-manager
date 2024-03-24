from data_collector.tasks import (
    move_examination_files
)

from django.conf import settings

from endoreg_db.models import RawPdfFile

PDF_TYPE_EXAMINATION = settings.PDF_TYPE_EXAMINATION
PDF_TYPE_HISTOLOGY = settings.PDF_TYPE_HISTOLOGY

move_examination_files(
    pdf_type_name=PDF_TYPE_EXAMINATION,
    center_name = settings.ENDOREG_CENTER_NAME
)

# get an an e
#########################

from endoreg_db.models import RawPdfFile
from pprint import pprint

f= RawPdfFile.objects.get()
t, a, rm = f.process_file(verbose = True)

sm = f.sensitive_meta
sm.update_from_dict(rm)
pprint(sm)


pprint(t)

pprint(a)

pprint(rm)

