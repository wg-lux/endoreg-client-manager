from endoreg_db.models import PdfType, RawPdfFile
from agl_report_reader.report_reader import ReportReader
from pathlib import Path

pdf_type = PdfType.objects.get(name="ukw-endoscopy-examination-report-generic")
r = RawPdfFile.objects.get(pdf_type=pdf_type)
rr_config = r.get_report_reader_config()

rr = ReportReader(**rr_config)

pdf_path_parent = Path("/mnt/hdd-sensitive/DropOff/data/histology/")

pdf_paths = list(pdf_path_parent.glob("*.pdf"))
pdf_path = pdf_paths[0]

# read pdf text
raw_text = rr.read_pdf(pdf_path)

# write to text file
text_file = pdf_path.with_suffix(".txt")
text_file.write_text(raw_text)



#############
from endoreg_db.models import PdfType, RawPdfFile
from agl_report_reader.report_reader import ReportReader
from pathlib import Path
pdf_path_parent = Path("/mnt/hdd-sensitive/DropOff/data/histology/")
pdf_paths = list(pdf_path_parent.glob("*.pdf"))
pdf_path = pdf_paths[0]

histo = RawPdfFile.create_from_file(
    file_path = pdf_path,
    center_name = "university_hospital_wuerzburg",
    pdf_type_name = "ukw-endoscopy-histology-report-generic",
    destination_dir = Path("/mnt/hdd-sensitive/Pseudo/import/pdf/")
)

########

from endoreg_db.models import PdfType, RawPdfFile
from agl_report_reader.report_reader import ReportReader
from pathlib import Path
from pprint import pprint

r = RawPdfFile.objects.get()
rr_config = r.get_report_reader_config()

pprint(rr_config)

pdf_path = r.file.path

rr = ReportReader(**rr_config)


result = rr.process_report(pdf_path, verbose=True)
