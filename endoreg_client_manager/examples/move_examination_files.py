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
f= RawPdfFile.objects.get()
f.update()

#########################

from endoreg_db.models import RawPdfFile
from agl_report_reader.report_reader import ReportReader
from pprint import pprint
verbose = True

f= RawPdfFile.objects.get()
rr_config = f.get_report_reader_config()

rr = ReportReader(**rr_config)
pdf_path = f.file.path
text, anonymized_text, report_meta = rr.process_report(pdf_path, verbose=verbose)




f.update()
pprint(rr_config)

t, a, rm = f.process_file(verbose = True)

sm = f.sensitive_meta
sm.update_from_dict(rm)
pprint(sm)


pprint(t)

pprint(a)

pprint(rm)

