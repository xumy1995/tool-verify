# OpenCV 验证记录

以下命令默认在 `tool-verify` 根目录执行。

## 环境
- 时间: 2026-07-21
- 主机: Linux `5.14.0-284.25.1.el9_2.x86_64`
- CPU: AMD EPYC 7742，256 逻辑核
- 内存: 499 GiB
- CMake: 3.29.0
- Ninja: 1.11.1
- GCC: 12.3.0
- Python: 3.10.12
- CUDA: `nvcc 12.4`

## 源码
- `opencv`: `4.x`
- commit: `7aa163b83f5a32be7f43a0b9837584ca7460238b`
- `opencv_extra`: `4.x`
- commit: `f202151dfb4734e47399ddf6581183d423da74b4`
- `opencv_contrib`: `4.x`
- commit: `a8e9acd62cabd30419dba83007f2ac0d07de5e2c`
- 测试数据: `./opencv-verify/src/opencv_extra/testdata`

## CPU 验证结果
- 构建目录: `./opencv-verify/build-cpu`
- CMake 配置成功
- 编译成功
- `opencv_test_*` 失败项: `opencv_test_highgui`

### CPU 完整命令
```bash
# 首先安装ffmpeg
apt update
apt install -y \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libavdevice-dev \
    libavfilter-dev \
    libswresample-dev

ROOT="$(pwd)/opencv-verify"
mkdir -p "$ROOT/build-cpu" "$ROOT/logs-cpu"
cmake -S "$ROOT/src/opencv" \
      -B "$ROOT/build-cpu" \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DWITH_FFMPEG=ON \
      -DBUILD_TESTS=ON \
      -DBUILD_PERF_TESTS=ON \
      -DBUILD_EXAMPLES=ON \
      -DWITH_CUDA=OFF \
      -D CMAKE_C_COMPILER=gcc-12 \
      -D CMAKE_CXX_COMPILER=g++-12 \
      -DOPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata" \
      | tee "$ROOT/logs-cpu/cmake-cpu.log"
cmake --build "$ROOT/build-cpu" \
      --parallel 8 \
      | tee "$ROOT/logs-cpu/build-cpu.log"

export OPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata"
cd "$ROOT/build-cpu/bin"
for t in $(find . -maxdepth 1 -type f -executable -name 'opencv_test_*' -printf '%f\n' | sort); do
  echo "===== $t =====" | tee -a "$ROOT/logs-cpu/test-summary-cpu.log"
  ./$t 2>&1 | tee "$ROOT/logs-cpu/${t}.log"
  status=${PIPESTATUS[0]}
  echo "$t exit=$status" | tee -a "$ROOT/logs-cpu/test-summary-cpu.log"
done
```

### CPU关键日志
- 配置: `$ROOT/logs-cpu/cmake-cpu.log`
- 编译: `$ROOT/logs-cpu/build-cpu.log`
- accuracy 汇总: `$ROOT/logs-cpu/test-summary-cpu.log`

### CPU 测试失败项分析
#### `opencv_test_highgui`
- 结果: `1 / 5` 通过，失败 4 个
- 失败项:
  - `Highgui_GUI.regression`
  - `Highgui_GUI.trackbar_unsafe`
  - `Highgui_GUI.trackbar`
  - `Highgui_GUI.small_width_image`
- 关键日志:
  ```plain
  Exception message: OpenCV(4.14.0-pre) /data/xumengying/tool-verify/opencv-verify/src/opencv/modules/highgui/src/window.cpp:1295: error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvDestroyAllWindows'

  Exception message: OpenCV(4.14.0-pre) /data/xumengying/tool-verify/opencv-verify/src/opencv/modules/highgui/src/window.cpp:1284: error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvNamedWindow'
  ```
- 错误分析:
  - OpenCV 编译时没有启用 HighGUI 的图形界面后端, 可以跳过该测试


## CUDA 验证结果
- 参考文档：https://www.cs.hmc.edu/~ndodds/opencv-cuda-installation-ubuntu.html
- 构建目录: `./opencv-verify/build-cuda`
- CMake 配置成功
- 编译成功
- `opencv_test_*` 失败项: 
  - `opencv_test_cudaoptflow`
  - `opencv_test_dnn`
  - 【已修复】`opencv_test_face`
  - `opencv_test_highgui`


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
      -DWITH_FFMPEG=ON \
      -DWITH_CUDA=ON \
      -DWITH_CUDNN=ON \
      -DOPENCV_DNN_CUDA=ON \
      -DCUDA_ARCH_BIN=8.0 \
      -D CMAKE_C_COMPILER=gcc-12 \
      -D CMAKE_CXX_COMPILER=g++-12 \
      -DOPENCV_EXTRA_MODULES_PATH="$ROOT/src/opencv_contrib/modules" \
      -DOPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata" \
      | tee "$ROOT/logs-cuda/cmake-cuda.log"
cmake --build "$ROOT/build-cuda" \
      --parallel 32 \
      | tee "$ROOT/logs-cuda/build-cuda.log"

export OPENCV_TEST_DATA_PATH="$ROOT/src/opencv_extra/testdata"
cd "$ROOT/build-cuda/bin"
for t in $(find . -maxdepth 1 -type f -executable -name 'opencv_test_*' -printf '%f\n' | sort); do
  echo "===== $t =====" | tee -a "$ROOT/logs-cuda/test-summary-cuda.log"
  ./$t 2>&1 | tee "$ROOT/logs-cuda/${t}.log"
  status=${PIPESTATUS[0]}
  echo "$t exit=$status" | tee -a "$ROOT/logs-cuda/test-summary-cuda.log"
done
```

### CUDA关键日志
- 配置: `$ROOT/logs-cuda/cmake-cuda.log`
- 编译: `$ROOT/logs-cuda/build-cuda.log`
- accuracy 汇总: `$ROOT/logs-cuda/test-summary-cuda.log`

### CUDA 测试失败项分析
#### `opencv_test_cudaoptflow`
- 结果: `45 / 47` 通过，失败 2 个
- 失败项: 
  - `CUDA_OptFlow/NvidiaOpticalFlow_1_0.Regression/0`
  - `CUDA_OptFlow/NvidiaOpticalFlow_2_0.Regression/0`
- 关键日志: 
    ```plain
    [ RUN      ] CUDA_OptFlow/NvidiaOpticalFlow_1_0.Regression/0, where GetParam() = NVIDIA A100-SXM4-40GB
    /data/xumengying/opencv-verify/src/opencv_contrib/modules/cudaoptflow/test/test_optflow.cpp:581: Failure
    Expected: (checkSimilarity(golden, upsampledFlow)) <= (1e-10), actual: 0.06994 vs 1e-10
    [  FAILED  ] CUDA_OptFlow/NvidiaOpticalFlow_1_0.Regression/0, where GetParam() = NVIDIA A100-SXM4-40GB (283 ms)

    [ RUN      ] CUDA_OptFlow/NvidiaOpticalFlow_2_0.Regression/0, where GetParam() = NVIDIA A100-SXM4-40GB
    /data/xumengying/opencv-verify/src/opencv_contrib/modules/cudaoptflow/test/test_optflow.cpp:665: Failure
    Value of: golden.empty()
      Actual: true
    Expected: false
    [  FAILED  ] CUDA_OptFlow/NvidiaOpticalFlow_2_0.Regression/0, where GetParam() = NVIDIA A100-SXM4-40GB (279 ms)
    ```
- 错误分析: 
  - 有人提过相同的issue: https://github.com/opencv/opencv_contrib/issues/3374
  - NvidiaOpticalFlow_1_0 测试失败，是由于与 golden 结果不同，这可能是因为测试硬件（NVIDIA A100-SXM4-40GB）与生成 testdata/gpu/opticalflow/nvofGolden.flo 的硬件不同
  - NvidiaOpticalFlow_2_0 测试失败，是由于 golden 结果文件 `testdata/gpu/opticalflow/nvofGolden_2.flo` 不存在

#### `opencv_test_dnn`
- 结果: `8304 / 8311` 通过，失败 7 个
- 失败项: 
  - `Test_ONNX_layers.LSTM_Activations/0, where GetParam() = CUDA/CUDA`
  - `Test_ONNX_layers.LSTM_hidden/0, where GetParam() = CUDA/CUDA`
  - `Test_ONNX_layers.LSTM_hidden_bidirectional/0, where GetParam() = CUDA/CUDA`
  - `Test_ONNX_layers.LSTM_cell_forward/0, where GetParam() = CUDA/CUDA`
  - `Test_ONNX_layers.LSTM_cell_bidirectional/0, where GetParam() = CUDA/CUDA`
  - `Test_TensorFlow_layers.Convolution3D/1, where GetParam() = CUDA/CUDA_FP16`
  - `Test_TensorFlow_layers.concat_3d/1, where GetParam() = CUDA/CUDA_FP16`
- 关键日志: 
  ```plain
  [ RUN      ] Test_ONNX_layers.LSTM_Activations/0, where GetParam() = CUDA/CUDA
  cudnn_WorkspaceSize: 8389472
  reserveSpaceSize: 0
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:84: Failure
  Expected: (normL1) <= (l1), actual: 1.15422e-05 vs 1e-05
  lstm_cntk_tanh  |ref| = 0.16841614246368408
  [  FAILED  ] Test_ONNX_layers.LSTM_Activations/0, where GetParam() = CUDA/CUDA (18 ms)

  [ RUN      ] Test_ONNX_layers.LSTM_hidden/0, where GetParam() = CUDA/CUDA
  cudnn_WorkspaceSize: 8390080
  reserveSpaceSize: 0
  cudnn_WorkspaceSize: 8390016
  reserveSpaceSize: 0
  cudnn_WorkspaceSize: 8390016
  reserveSpaceSize: 0
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:84: Failure
  Expected: (normL1) <= (l1), actual: 1.45709e-05 vs 1e-05
  hidden_lstm  |ref| = 0.57614982128143311
  [  FAILED  ] Test_ONNX_layers.LSTM_hidden/0, where GetParam() = CUDA/CUDA (14 ms)

  [ RUN      ] Test_ONNX_layers.LSTM_hidden_bidirectional/0, where GetParam() = CUDA/CUDA
  cudnn_WorkspaceSize: 16780576
  reserveSpaceSize: 0
  cudnn_WorkspaceSize: 16780768
  reserveSpaceSize: 0
  cudnn_WorkspaceSize: 16780768
  reserveSpaceSize: 0
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:84: Failure
  Expected: (normL1) <= (l1), actual: 1.53468e-05 vs 1e-05
  hidden_lstm_bi  |ref| = 0.25425195693969727
  [  FAILED  ] Test_ONNX_layers.LSTM_hidden_bidirectional/0, where GetParam() = CUDA/CUDA (16 ms)

  [ RUN      ] Test_ONNX_layers.LSTM_cell_forward/0, where GetParam() = CUDA/CUDA
  cudnn_WorkspaceSize: 8390080
  reserveSpaceSize: 0
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:84: Failure
  Expected: (normL1) <= (l1), actual: 3.52899e-05 vs 1e-05
  lstm_cell_forward  |ref| = 0.49361768364906311
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:87: Failure
  Expected: (normInf) <= (lInf), actual: 0.000242293 vs 0.0001
  lstm_cell_forward  |ref| = 0.49361768364906311
  [  FAILED  ] Test_ONNX_layers.LSTM_cell_forward/0, where GetParam() = CUDA/CUDA (11 ms)

  [ RUN      ] Test_ONNX_layers.LSTM_cell_bidirectional/0, where GetParam() = CUDA/CUDA
  cudnn_WorkspaceSize: 16780576
  reserveSpaceSize: 0
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:84: Failure
  Expected: (normL1) <= (l1), actual: 3.76163e-05 vs 1e-05
  lstm_cell_bidirectional  |ref| = 1.058696985244751
  /data/xumengying/opencv-verify/src/opencv/modules/dnn/test/test_common.impl.hpp:87: Failure
  Expected: (normInf) <= (lInf), actual: 0.00024122 vs 0.0001
  lstm_cell_bidirectional  |ref| = 1.058696985244751
  [  FAILED  ] Test_ONNX_layers.LSTM_cell_bidirectional/0, where GetParam() = CUDA/CUDA (10 ms)

  [ RUN      ] Test_TensorFlow_layers.Convolution3D/1, where GetParam() = CUDA/CUDA_FP16
  unknown file: Failure
  C++ exception with description "OpenCV(4.14.0-pre) /data/xumengying/opencv-verify/src/opencv/modules/dnn/src/layers/../cuda4dnn/primitives/../csl/cudnn/convolution.hpp:303: error: (-217:Gpu API call) cuDNN did not return a suitable algorithm for convolution. in function 'ConvolutionAlgorithm'
  " thrown in the test body.
  [  FAILED  ] Test_TensorFlow_layers.Convolution3D/1, where GetParam() = CUDA/CUDA_FP16 (7 ms)

  [ RUN      ] Test_TensorFlow_layers.concat_3d/1, where GetParam() = CUDA/CUDA_FP16
  unknown file: Failure
  C++ exception with description "OpenCV(4.14.0-pre) /data/xumengying/opencv-verify/src/opencv/modules/dnn/src/layers/../cuda4dnn/primitives/../csl/cudnn/convolution.hpp:303: error: (-217:Gpu API call) cuDNN did not return a suitable algorithm for convolution. in function 'ConvolutionAlgorithm'
  " thrown in the test body.
  [  FAILED  ] Test_TensorFlow_layers.concat_3d/1, where GetParam() = CUDA/CUDA_FP16 (6 ms)
  ```
- 错误分析: 
  - 5个 `Test_ONNX_layers` 失败是由于计算误差超过了阈值，但整体超过幅度不大
  - 2个 `Test_TensorFlow_layers` 失败可能是由于cudnn 9.1.0 对FP16的Convolution3D和concat_3d不支持

#### 【已修复】`opencv_test_face`
- 结果: `18 / 19` 通过，失败 1 个
- 失败项: 
  - `CV_Face_FacemarkKazemi.can_detect_landmarks`
- 关键日志: 
  ```plain
  [ RUN      ] CV_Face_FacemarkKazemi.can_detect_landmarks
  unknown file: Failure
  C++ exception with description "OpenCV(4.14.0-pre) /data/xumengying/opencv-verify/src/opencv/modules/ts/src/ts.cpp:1060: error: (-2:Unspecified error) OpenCV tests: Can't find required data file: face/face_landmark_model.dat in function 'findData'
  " thrown in the test body.
  [  FAILED  ] CV_Face_FacemarkKazemi.can_detect_landmarks (7 ms)
  ```
- 错误分析: 
  - github有人提过相同的issue：https://github.com/opencv/opencv_contrib/issues/2153
  - 把缺失的文件复制一下：`cp build-cuda/share/opencv4/testdata/cv/face/face_landmark_model.dat src/opencv_extra/testdata/cv/face/`，然后重新执行测试即可：
    ```bash
    cd build_cuda/bin
    ./opencv_test_face 2>&1 | tee ../../logs-cuda/opencv_test_face.log.fix
    ```

#### `opencv_test_highgui`
- 同CPU情形