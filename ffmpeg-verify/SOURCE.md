# FFmpeg Sources

The upstream source tree is not committed to this verification repository.

## Repository

```text
FFmpeg: https://github.com/FFmpeg/FFmpeg.git
```

## Verified Revision

```text
FFmpeg: 5d7112c60e6f0f0742ce47d448e6da0718a70f4c
```

## Recreate Source Directory

```bash
mkdir -p /data/xumengying/tool-verify/ffmpeg-verify/src
cd /data/xumengying/tool-verify/ffmpeg-verify/src

git clone https://github.com/FFmpeg/FFmpeg.git
git -C FFmpeg checkout 5d7112c60e6f0f0742ce47d448e6da0718a70f4c

git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
```

## External Dependency

```bash
cd ./src/nv-codec-headers
make install
```

The verification commands below assume you run them from `tool-verify`.
