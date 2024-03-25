from datetime import timedelta

SCHEDULE = {
    "move_pdf_examination_files": { 
        "task": "data_collector.tasks.pdf_examination_move.task_move_examination_files",
        # "schedule": timedelta(minutes=5),
        "schedule": timedelta(minutes=1),
    },
    "move_pdf_histology_files": {
        "task": "data_collector.tasks.pdf_histology_move.task_move_histology_files",
        # "schedule": timedelta(minutes=6),
        "schedule": timedelta(minutes=1),
    },
    'move_video_files': {
        'task': 'data_collector.tasks.video_move.task_move_video_files',
        # 'schedule': timedelta(minutes=120),
        "schedule": timedelta(minutes=1),
    }
}
