# FFmpeg 验证记录

以下命令默认在 `tool-verify` 根目录执行。

## 环境
- 时间：2026-07-22
- CUDA：`nvcc 12.4`

## 源码
- `FFmpeg`：`5d7112c60e6f0f0742ce47d448e6da0718a70f4c`
- 源码目录：`./ffmpeg-verify/src/FFmpeg`

## CPU 完整命令

```bash
cd ./ffmpeg-verify
mkdir -p "build-cpu"
mkdir -p "logs-cpu"
mkdir -p "fate-suite"

# 配置configure
cd "./build-cpu"  # 以下命令均在build-cpu目录下执行
"../src/FFmpeg/configure" \
  --assert-level=2 \
  --prefix="./install" \
  --samples="../fate-suite" \
  --disable-doc \
  --disable-debug \
  --disable-autodetect \
  --enable-pthreads \
  --enable-shared \
  --disable-static \
  --enable-ffmpeg \
  --enable-ffprobe \
  --enable-protocol=file,pipe,concat,data \
  --enable-demuxer=image2,image2pipe,mov,matroska,concat \
  --enable-muxer=mp4,matroska,webm,null,framecrc,md5 \
  --enable-decoder=png,jpeg,h264,hevc,mpeg4,rawvideo \
  --enable-encoder=png,jpeg,h264,hevc,mpeg4,rawvideo \
  --extra-cflags='-O2' \
  --extra-ldflags='' \
  | tee "../logs-cpu/configure-cpu.log"

# 编译
make -j"$(nproc)" | tee "../logs-cpu/make-cpu.log"

# 下载测试数据
make fate-rsync

# 执行fate测试
LD_LIBRARY_PATH=".:./libavdevice:./libavfilter:./libavformat:./libavcodec:./libswresample:./libswscale:./libavutil" \
make fate | tee "../logs-cpu/fate-cpu.log"

# 查看ffmpeg版本
LD_LIBRARY_PATH=".:./libavdevice:./libavfilter:./libavformat:./libavcodec:./libswresample:./libswscale:./libavutil" \
  "./ffmpeg" -version \
  | tee "../logs-cpu/ffmpeg-version.log"

# 查看ffprobe版本
LD_LIBRARY_PATH=".:./libavdevice:./libavfilter:./libavformat:./libavcodec:./libswresample:./libswscale:./libavutil" \
  "./ffprobe" -version \
  | tee "../logs-cpu/ffprobe-version.log"
```

## CUDA 完整命令
```bash
# 首先参考SOURCE.md 安装nv-codec-headers

mkdir -p "build-cuda" 
mkdir -p "logs-cuda"
mkdir -p "fate-suite"

# 配置configure
cd "./build-cuda"   # 以下命令均在build-cuda目录下执行
# CUDA 构建不要加 `--disable-autodetect`，否则 `ffnvcodec` 不会被探测到
"../src/FFmpeg/configure" \
  --assert-level=2 \
  --prefix="./install" \
  --samples="../fate-suite" \
  --disable-doc \
  --disable-debug \
  --enable-pthreads \
  --enable-shared \
  --disable-static \
  --enable-ffmpeg \
  --enable-ffprobe \
  --enable-cuda \
  --enable-cuda-nvcc \
  --enable-nvenc \
  --enable-nvdec \
  --enable-nonfree \
  --enable-cuvid \
  --enable-protocol=file,pipe,concat,data \
  --enable-demuxer=image2,image2pipe,mov,matroska,concat \
  --enable-muxer=mp4,matroska,webm,null,framecrc,md5 \
  --enable-decoder=png,jpeg,h264,hevc,mpeg4,rawvideo \
  --enable-encoder=png,jpeg,h264,hevc,mpeg4,rawvideo \
  --extra-cflags='-O2 -I/usr/local/cuda/include' \
  --extra-ldflags='-L/usr/local/cuda/lib64' \
  | tee "../logs-cuda/configure-cuda.log"

make -j"$(nproc)" | tee "../logs-cuda/make-cuda.log"

# 下载测试数据
make fate-rsync

# 执行fate测试
LD_LIBRARY_PATH=".:./libavdevice:./libavfilter:./libavformat:./libavcodec:./libswresample:./libswscale:./libavutil" \
make fate | tee "../logs-cuda/fate-cuda.log"

# 查看ffmpeg版本
LD_LIBRARY_PATH=".:./libavdevice:./libavfilter:./libavformat:./libavcodec:./libswresample:./libswscale:./libavutil" \
  ./ffmpeg -version \
  | tee "../logs-cuda/ffmpeg-version.log"

# 查看ffprobe版本
LD_LIBRARY_PATH=".:./libavdevice:./libavfilter:./libavformat:./libavcodec:./libswresample:./libswscale:./libavutil" \
  ./ffprobe -version \
  | tee "../logs-cuda/ffprobe-version.log"
```

## 关键日志
- CPU configure：`./ffmpeg-verify/logs-cpu/configure-cpu.log`
- CPU build：`./ffmpeg-verify/logs-cpu/make-cpu.log`
- CPU FATE：`./ffmpeg-verify/logs-cpu/fate-cpu.log`
- CPU version：`./ffmpeg-verify/logs-cpu/ffmpeg-version.log`
- CPU probe：`./ffmpeg-verify/logs-cpu/ffprobe-version.log`
- CUDA configure：`./ffmpeg-verify/logs-cuda/configure-cuda.log`
- CUDA build：`./ffmpeg-verify/logs-cuda/make-cuda.log`
- CUDA FATE：`./ffmpeg-verify/logs-cuda/fate-cuda.log`
- CUDA version：`./ffmpeg-verify/logs-cuda/ffmpeg-version.log`
- CUDA probe：`./ffmpeg-verify/logs-cuda/ffprobe-version.log`


## 结论
- CPU 和 CUDA 路径都已完成构建和 FATE 验证
- 当前 CUDA 验证证明的是编译链路和 FATE 可执行性，不等于 NVENC/NVDEC/CUVID 全功能验证
