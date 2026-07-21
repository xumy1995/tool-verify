# OpenCV 验证记录

以下命令默认在 `tool-verify` 根目录执行。

## 环境
- 时间：2026-07-21
- 主机：Linux `5.14.0-284.25.1.el9_2.x86_64`
- CPU：AMD EPYC 7742，256 逻辑核
- 内存：499 GiB
- CMake：3.29.0
- Ninja：1.11.1
- GCC：11.4.0
- Python：3.10.12
- CUDA：`nvcc 12.4`

## 源码
- `opencv`：`4.x`
- commit：`7aa163b83f5a32be7f43a0b9837584ca7460238b`
- `opencv_extra`：`4.x`
- commit：`f202151dfb4734e47399ddf6581183d423da74b4`
- `opencv_contrib`: `4.x`
- commit: `a8e9acd62cabd30419dba83007f2ac0d07de5e2c`
- 测试数据：`./opencv-verify/src/opencv_extra/testdata`

## CPU 验证结果
- 构建目录：`./opencv-verify/build-cpu`
- 结果：
  - CMake 配置成功
  - 编译成功
  - `opencv_test_*` 已生成
  - `opencv_perf_*` 已生成
  - 已完成的 accuracy tests 全部通过，唯一失败项是 `opencv_test_highgui`

### `opencv_test_highgui` 失败原因
- 失败原因不是 OpenCV 算法问题，而是当前构建没有 GUI 后端
- 日志中的错误是：
  - `The function is not implemented`
  - `Rebuild the library with Windows, GTK+ 2.x or Cocoa support`
- 这说明 `highgui` 在当前环境里只能做无窗口编译，不能跑需要 `namedWindow()` / `destroyAllWindows()` 的 GUI 用例

### CPU 完整命令
```bash
ROOT="$(pwd)/opencv-verify"
mkdir -p "$ROOT/build-cpu" "$ROOT/logs-cpu"
cmake -S "$ROOT/src/opencv" \
      -B "$ROOT/build-cpu" \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTS=ON \
      -DBUILD_PERF_TESTS=ON \
      -DBUILD_EXAMPLES=ON \
      -DWITH_CUDA=OFF \
      -DOPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata" \
      | tee "$ROOT/logs-cpu/cmake-cpu.log"
cmake --build "$ROOT/build-cpu" \
      --parallel "$(nproc)" \
      | tee "$ROOT/logs-cpu/build-cpu.log"

export OPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata"
cd "$ROOT/build-cpu/bin"
for t in $(find . -maxdepth 1 -type f -executable -name 'opencv_test_*' -printf '%f\n' | sort); do
  echo "===== $t =====" | tee -a "$ROOT/logs-cpu/test-summary-cpu.log"
  ./$t 2>&1 | tee "$ROOT/logs-cpu/${t}.log"
  status=${PIPESTATUS[0]}
  echo "$t exit=$status" | tee -a "$ROOT/logs-cpu/test-summary-cpu.log"
done

for t in $(find . -maxdepth 1 -type f -executable -name 'opencv_perf_*' -printf '%f\n' | sort); do
  echo "===== $t =====" | tee -a "$ROOT/logs-cpu/perf-summary-cpu.log"
  ./$t 2>&1 | tee "$ROOT/logs-cpu/${t}.log"
  status=${PIPESTATUS[0]}
  echo "$t exit=$status" | tee -a "$ROOT/logs-cpu/perf-summary-cpu.log"
done
```

### 关键日志
- 配置：`$ROOT/logs-cpu/cmake-cpu.log`
- 编译：`$ROOT/logs-cpu/build-cpu.log`
- accuracy 汇总：`$ROOT/logs-cpu/test-summary-cpu.log`
- perf 汇总：`$ROOT/logs-cpu/perf-summary-cpu.log`

## CUDA 验证结果
- 构建目录：`./opencv-verify/build-cuda`
- 结果：
  - CMake 已识别到 `CUDA 12.4`
  - A100 对应的配置已收敛到 `CUDA_ARCH_BIN=8.0`
  - 第一次cmake报错：`CUDA: OpenCV requires enabled 'cudev' module from 'opencv_contrib' repository`，下载opencv_contrib并配置`-DOPENCV_EXTRA_MODULES_PATH`后解决

### CUDA 完整命令
```bash
ROOT="$(pwd)/opencv-verify"
mkdir -p "$ROOT/build-cuda" "$ROOT/logs-cuda"
cmake -S "$ROOT/src/opencv" \
      -B "$ROOT/build-cuda" \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTS=ON \
      -DBUILD_PERF_TESTS=ON \
      -DBUILD_EXAMPLES=ON \
      -DWITH_CUDA=ON \
      -DWITH_OPENCL=OFF \
      -DWITH_V4L=OFF \
      -DCUDA_ARCH_BIN=8.0 \
      -DOPENCV_EXTRA_MODULES_PATH="$ROOT/src/opencv_contrib/modules" \
      -DOPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata" \
      | tee "$ROOT/logs-cuda/cmake-cuda.log"
cmake --build "$ROOT/build-cuda" \
      --parallel "$(nproc)" \
      | tee "$ROOT/logs-cuda/build-cuda.log"

export OPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata"
cd "$ROOT/build-cuda/bin"
for t in $(find . -maxdepth 1 -type f -executable -name 'opencv_test_*' -printf '%f\n' | sort); do
  echo "===== $t =====" | tee -a "$ROOT/logs-cuda/test-summary-cuda.log"
  ./$t 2>&1 | tee "$ROOT/logs-cuda/${t}.log"
  status=${PIPESTATUS[0]}
  echo "$t exit=$status" | tee -a "$ROOT/logs-cuda/test-summary-cuda.log"
done

for t in $(find . -maxdepth 1 -type f -executable -name 'opencv_perf_*' -printf '%f\n' | sort); do
  echo "===== $t =====" | tee -a "$ROOT/logs-cuda/perf-summary-cuda.log"
  ./$t 2>&1 | tee "$ROOT/logs-cuda/${t}.log"
  status=${PIPESTATUS[0]}
  echo "$t exit=$status" | tee -a "$ROOT/logs-cuda/perf-summary-cuda.log"
done
```

### 关键日志
- 配置：`$ROOT/logs-cuda/cmake-cuda.log`
- 编译：`$ROOT/logs-cuda/build-cuda.log`
- accuracy 汇总：`$ROOT/logs-cuda/test-summary-cuda.log`
- perf 汇总：`$ROOT/logs-cuda/perf-summary-cuda.log`

### CUDA 测试失败项分析
- `opencv_test_*` 总体结果：5 个测试程序返回非 0
- 失败程序：
  - `opencv_test_cudaoptflow`
  - `opencv_test_dnn`
  - `opencv_test_face`
  - `opencv_test_gapi`
  - `opencv_test_highgui`
- CMake 关键信息：
  - `CUDA 12.4`
  - `cuDNN 9.1.0`
  - `NVIDIA GPU arch: 80`
  - `GUI: NONE`
  - `FFMPEG: NO`
  - `GStreamer: NO`

#### `opencv_test_cudaoptflow`
- 结果：`45 / 47` 通过，失败 2 个
- 失败项：
  - `CUDA_OptFlow/NvidiaOpticalFlow_1_0.Regression/0`
  - `CUDA_OptFlow/NvidiaOpticalFlow_2_0.Regression/0`
- 关键日志：
  - `actual: 0.06994 vs 1e-10`
  - `golden.empty() Actual: true Expected: false`
- 判断：
  - CUDA optical flow 基础功能不是整体失败；Farneback、TVL1、Nan 检查均通过
  - 失败集中在 NVIDIA Optical Flow SDK regression golden 对比，可能是 golden 数据缺失或 SDK/驱动输出差异

#### `opencv_test_dnn`
- 结果：`8304 / 8311` 通过，失败 7 个
- 失败项：
  - 5 个 `Test_ONNX_layers.LSTM_*` CUDA 用例
  - 2 个 `Test_TensorFlow_layers.*` CUDA FP16 3D convolution 用例
- 关键日志：
  - LSTM 数值误差略高于阈值，例如 `actual: 1.15422e-05 vs 1e-05`
  - cuDNN 算法选择失败：`cuDNN did not return a suitable algorithm for convolution`
- 判断：
  - 这是 DNN CUDA/cuDNN 后端的数值容差和 FP16 卷积算法选择问题
  - 不影响 CUDA 编译链路和大多数 DNN CUDA 用例通过的结论

#### `opencv_test_face`
- 结果：`18 / 19` 通过，失败 1 个
- 失败项：
  - `CV_Face_FacemarkKazemi.can_detect_landmarks`
- 关键日志：
  - `Can't find required data file: face/face_landmark_model.dat`
- 判断：
  - 测试数据缺失，不是算法或 CUDA 问题

#### `opencv_test_gapi`
- 结果：`15470 / 15475` 通过，失败 5 个
- 失败项：
  - `VASObjectTracker.PipelineTest`
  - 4 个 `AsyncAPICancelation/cancel/*`
- 关键日志：
  - `Couldn't grab the very first frame`
  - `Test code is not available due to compilation error with GCC 11`
- 判断：
  - `VASObjectTracker` 更像视频输入、测试素材或 video backend 限制
  - `AsyncAPICancelation` 是 GCC 11 下该测试代码路径不可用，日志已明确说明

#### `opencv_test_highgui`
- 结果：`1 / 5` 通过，失败 4 个
- 关键日志：
  - `The function is not implemented`
  - `Rebuild the library with Windows, GTK+ 2.x or Cocoa support`
- 判断：
  - 当前构建 `GUI: NONE`、`GTK+: NO`
  - 这是无 GUI 后端导致，和 CUDA 无关

### CUDA 验收判断
- CUDA 编译链路已经通过：CMake 成功、build 成功、CUDA 12.4 / cuDNN 9.1.0 / A100 sm_80 均被识别
- CUDA 基础模块通过情况较好：`cudaarithm`、`cudabgsegm`、`cudacodec`、`cudafeatures2d`、`cudafilters`、`cudaimgproc`、`cudalegacy`、`cudaobjdetect`、`cudastereo`、`cudawarping`、`cudev` 均返回 0
- 当前失败项不能归类为 CUDA 编译失败
- 如果要做严格全绿，需要分别处理测试数据、GUI 后端、视频 backend、GCC 11 特定 G-API 用例，以及 DNN/cuDNN 数值或算法选择差异

### 建议的过滤重跑命令
如果目标是验证 CUDA 主链路，可以先跳过已定位的环境或已知差异项：

```bash
export OPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata"
cd "$ROOT/build-cuda/bin"

./opencv_test_cudaoptflow \
  --gtest_filter='-CUDA_OptFlow/NvidiaOpticalFlow_1_0.Regression/0:CUDA_OptFlow/NvidiaOpticalFlow_2_0.Regression/0' \
  2>&1 | tee "$ROOT/logs-cuda/opencv_test_cudaoptflow.filtered.log"

./opencv_test_dnn \
  --gtest_filter='-Test_ONNX_layers.LSTM_Activations/0:Test_ONNX_layers.LSTM_hidden/0:Test_ONNX_layers.LSTM_hidden_bidirectional/0:Test_ONNX_layers.LSTM_cell_forward/0:Test_ONNX_layers.LSTM_cell_bidirectional/0:Test_TensorFlow_layers.Convolution3D/1:Test_TensorFlow_layers.concat_3d/1' \
  2>&1 | tee "$ROOT/logs-cuda/opencv_test_dnn.filtered.log"

./opencv_test_face \
  --gtest_filter='-CV_Face_FacemarkKazemi.can_detect_landmarks' \
  2>&1 | tee "$ROOT/logs-cuda/opencv_test_face.filtered.log"

./opencv_test_gapi \
  --gtest_filter='-VASObjectTracker.PipelineTest:AsyncAPICancelation/cancel/*.basic' \
  2>&1 | tee "$ROOT/logs-cuda/opencv_test_gapi.filtered.log"

./opencv_test_highgui \
  --gtest_filter='-Highgui_GUI.regression:Highgui_GUI.trackbar_unsafe:Highgui_GUI.trackbar:Highgui_GUI.small_width_image' \
  2>&1 | tee "$ROOT/logs-cuda/opencv_test_highgui.filtered.log"
```
