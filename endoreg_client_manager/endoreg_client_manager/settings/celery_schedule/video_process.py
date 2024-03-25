from datetime import timedelta

_PREFLIGHT = {
    "video_ocr_preflight": {
        "task": "data_collector.tasks.video_process.task_video_ocr_preflight",
        # "schedule": timedelta(minutes=15),
        "schedule": timedelta(minutes=1),
    },
    "video_initial_prediction_preflight": {
        "task": "data_collector.tasks.video_process.task_video_initial_prediction_preflight",
        # "schedule": timedelta(minutes=15),
        "schedule": timedelta(minutes=1),
    },
    "video_prediction_import_preflight": {
        "task": "data_collector.tasks.video_process.task_video_prediction_import_preflight",
        # "schedule": timedelta(minutes=15),
        "schedule": timedelta(minutes=1),
    },
    "delete_frames_preflight": {
        "task": "data_collector.tasks.video_process.task_delete_frames_preflight",
        # "schedule": timedelta(minutes=15),
        "schedule": timedelta(minutes=1),
    },
}

SCHEDULE = {
    "extract_frames": {
        "task": "data_collector.tasks.video_process.task_extract_frames",
        # "schedule": timedelta(minutes=90),
        "schedule": timedelta(minutes=1),
    },
    "video_ocr": {
        "task": "data_collector.tasks.video_process.task_video_ocr",
        # "schedule": timedelta(minutes=45),
        "schedule": timedelta(minutes=1),
    },
    "video_initial_prediction": {
        "task": "data_collector.tasks.video_process.task_video_initial_prediction",
        # "schedule": timedelta(minutes=120),
        "schedule": timedelta(minutes=1),
    },
    "video_prediction_import": {
        "task": "data_collector.tasks.video_process.task_video_prediction_import",
        # "schedule": timedelta(minutes=15),
        "schedule": timedelta(minutes=1),
    },
    "delete_frames": {
        "task": "data_collector.tasks.video_process.task_delete_frames",
        # "schedule": timedelta(minutes=30),
        "schedule": timedelta(minutes=1),
    },
}

SCHEDULE.update(_PREFLIGHT)