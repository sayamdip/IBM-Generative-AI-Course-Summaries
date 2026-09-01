import mlx_whisper

# Transcribe Directly Using Apple MLX Framework
result=mlx_whisper.transcribe("temp_audio.wav", path_or_hf_repo="mlx-community/whisper-base-mlx")

# Print The Transcription
print(result['text'])