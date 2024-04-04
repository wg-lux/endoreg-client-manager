import torch

print("CUDA Available:", torch.cuda.is_available())
print("Device Count:", torch.cuda.device_count())


from endoreg_db.models.data_file.import_classes.processing_functions import perform_initial_prediction_on_videos
from pathlib import Path
model_path = Path("/etc/multilabel_ai_models/colo_segmentation_RegNetX800MF_6.ckpt")
assert model_path.exists()
win_size = 1
seq_len = 0.5

r = perform_initial_prediction_on_videos(
    model_path=model_path,
    window_size_s=win_size,
    min_seq_len_s=seq_len
)

print(r)
