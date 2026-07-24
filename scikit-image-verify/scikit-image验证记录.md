# scikit-image 验证记录

以下命令默认在 `tool-verify` 根目录执行。涉及下载的源码、Python 包和外部测试数据由宿主机或手动方式准备，本记录只保留可复现命令和日志路径。

## 环境

- 时间：2026-07-23
- Python：`3.12.13`
- 虚拟环境工具：`uv`
- 验证方式：源码 editable 安装后执行官方 pytest 测试
- CUDA：scikit-image 本身没有 CUDA 构建路径，本项只做 CPU/Python 功能验证

## 源码

- 源码目录：`./scikit-image-verify/src/scikit-image`
- Commit：`93e9da980111f5f1b20e4f97d2067d6f301d25e2`
- 获取方式见：`./scikit-image-verify/SOURCE.md`

## CPU 完整命令

```bash
cd ./scikit-image-verify
mkdir -p ./src
mkdir -p ./logs-cpu
mkdir -p ./uv-cache
export UV_CACHE_DIR="$(pwd)/uv-cache"

# 正常情况下，第一次调用skimage.data.xxx()会通过pooch自动下载，如果下载失败，可以手动从 https://gitlab.com/scikit-image/data 下载到 ./skimage-cache/main/data    
mkdir -p ./skimage-cache/main/data    
export SKIMAGE_DATADIR="$(pwd)/skimage-cache"

# scikit-image 当前源码要求 Python >= 3.12，Python 3.11 会失败。
uv venv ./venv-cpu-py312 --python 3.12
source ./venv-cpu-py312/bin/activate

# 安装基础构建工具和源码构建依赖
uv pip install -U pip setuptools wheel pytest-xdist
uv pip install 'meson-python>=0.16' 'Cython>=3.0.10,!=3.2.0b1' 'pythran>=0.16' 'ninja>=1.11.1.1' 'spin>=0.13' 'build>=1.2.1' # \

# 安装 scikit-image 和测试依赖。
# 使用 --no-build-isolation，避免 editable loader 引用 uv 临时 build 目录里的 pythran。
cd ./src/scikit-image
uv pip install -e ".[test]" --no-build-isolation \
  2>&1 | tee ../../logs-cpu/pip-install-test.log

# 记录安装后的版本和依赖
python - <<'PY' 2>&1 | tee ../../logs-cpu/skimage-version.log
import skimage
print(skimage.__version__)
PY
python -m pip freeze \
  2>&1 | tee ../../logs-cpu/pip-freeze.log

# 收集测试用例。
# -o filterwarnings=default 用于绕过当前环境中 pytest 解析 pyproject warning filter 时的导入问题。
# 如果报错下载不到数据，可以手动下载缺少的数据到./skimage-cache/main/data

python -m pytest --collect-only -q -o filterwarnings=default \
  2>&1 | tee ../../logs-cpu/pytest-collect.log

# 执行完整测试
python -m pytest -o filterwarnings=default \
  2>&1 | tee ../../logs-cpu/pytest-cpu.log

deactivate
```

## 关键日志

- Python 依赖列表：`./scikit-image-verify/logs-cpu/pip-freeze.log`
- scikit-image 安装：`./scikit-image-verify/logs-cpu/pip-install-test.log`
- scikit-image 版本：`./scikit-image-verify/logs-cpu/skimage-version.log`
- pytest 收集：`./scikit-image-verify/logs-cpu/pytest-collect.log`
- pytest 执行：
  - 前序失败的版本：`./scikit-image-verify/logs-cpu/pytest-cpu-v1.log`, `./scikit-image-verify/logs-cpu/pytest-cpu-v2.log`, `./scikit-image-verify/logs-cpu/pytest-cpu-v3.log`  
  - 最终通过的版本：`./scikit-image-verify/logs-cpu/pytest-cpu.log`  

## 结论

- editable 安装已通过，安装版本为 `0.26.1rc0.dev0+git20260722.93e9da980`。
- pttest 评测结果：18722 passed，65 skipped，194 xfailed，1877 warnings（xfail是预期失败的意思，是正常的）

