from datetime import timedelta

SCHEDULE = {
    "process_pdf_files": {
        "task": "data_collector.tasks.pdf_all_process.task_pdf_process",
        # "schedule": timedelta(minutes=15),
        "schedule": timedelta(minutes=1),
    }
}