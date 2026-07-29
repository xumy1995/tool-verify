# Tool Verification

This repository records local verification steps and logs for image/video related tool libraries.

## Directory Layout

- `opencv-verify/`: OpenCV CPU/CUDA build and test records.
- `ffmpeg-verify/`: FFmpeg CPU/CUDA build and test verification.
- `Pillow-verify/`: Pillow CPU build and test verification.
- `scikit-image-verify/`: scikit-image CPU build and test verification.

## Source Policy

Do not commit upstream source trees or build directories. Source repositories are large and reproducible from public upstream links and pinned commits. Each verification folder should record source URLs, branches, commits, and clone commands in its own `SOURCE.md`.

## Artifact Policy

- Keep human-readable verification records and logs.
- Exclude `build/`, `build-*`, `src/`, compiled libraries, caches, and generated binaries.
- If a required artifact is too large for GitHub, record how to regenerate or download it instead of committing it.

