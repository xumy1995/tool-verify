# Pillow Source

The upstream source tree is not committed to this repository.

## Upstream

- Repository: https://github.com/python-pillow/Pillow.git
- Local path: `./Pillow-verify/src/Pillow`
- Verified commit: `9e282f5d754fe49ede35fde65fd862c6c50d1f9f`

## Clone

Run from the `tool-verify` root:

```bash
mkdir -p ./Pillow-verify/src
git clone https://github.com/python-pillow/Pillow.git ./Pillow-verify/src/Pillow
```

Record the exact commit after cloning:

```bash
git -C ./Pillow-verify/src/Pillow rev-parse HEAD
git -C ./Pillow-verify/src/Pillow status --short
```
