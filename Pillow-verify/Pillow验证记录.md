# Pillow 验证记录

以下命令默认在 `tool-verify` 根目录执行。

## 环境

- 时间：2026-07-23
- Python：`Python 3.11.15`（通过 `uv` 创建；当前 Pillow 源码要求 Python >= 3.11）
- 虚拟环境工具：`uv 0.11.31`
- 验证方式：源码 editable 安装后执行官方 pytest 测试
- CUDA：Pillow 本身没有 CUDA 构建路径，本项只做 CPU/Python 功能验证

## 源码

- 源码目录：`./Pillow-verify/src/Pillow`
- Commit：`9e282f5d754fe49ede35fde65fd862c6c50d1f9f`
- 获取方式见：`./Pillow-verify/SOURCE.md`

## CPU 完整命令

```bash
cd ./Pillow-verify
mkdir -p ./logs-cpu
mkdir -p ./uv-cache
export UV_CACHE_DIR="$(pwd)/uv-cache"

# 创建 Python 虚拟环境
# Pillow 当前源码要求 Python >= 3.11；如果系统 python3 是 3.10，直接用 uv 拉取/创建 3.11 环境
uv venv ./venv-cpu-py311 --python 3.11
source ./venv-cpu-py311/bin/activate

# 安装基础构建工具
uv pip install -U pip setuptools wheel 

# 安装 Pillow 测试依赖
cd ./src/Pillow
uv pip install -e ".[tests]" \
  2>&1 | tee ../../logs-cpu/pip-install-tests.log

# 收集测试用例
python -m pytest --collect-only \
  2>&1 | tee ../../logs-cpu/pytest-collect.log

# 执行测试
python -m pytest \
  2>&1 | tee ../../logs-cpu/pytest-cpu.log

# 记录安装后的 Pillow 版本和特性
python -m PIL \
  2>&1 | tee ../../logs-cpu/pillow-features.log

deactivate
```

## 关键日志

- 依赖安装：`./Pillow-verify/logs-cpu/pip-install-tests.log`
- pytest 收集：`./Pillow-verify/logs-cpu/pytest-collect.log`
- pytest 执行：`./Pillow-verify/logs-cpu/pytest-cpu.log`
- Pillow 特性：`./Pillow-verify/logs-cpu/pillow-features.log`

## 结论

- editable 安装成功：`pillow==13.0.0.dev0`
- pytest 收集：`5148 tests collected / 7 skipped`
- pytest 执行：`4283 passed, 869 skipped, 3 xfailed in 27.37s`4283 passed, 869 skipped, 3 xfailed in 27.28s （xfail是预期失败的意思，是正常的）
- 跳过主要来自可选系统库/依赖缺失：`freetype2`、`littlecms2`、`webp`、`avif`、`openjpeg`、`libtiff`、`raqm`、`libimagequant`、`xcb`、`numpy`、`Qt`、无 `$DISPLAY` 等
- 本次 CPU/Python 功能验证通过；Pillow 无 CUDA 验证项
