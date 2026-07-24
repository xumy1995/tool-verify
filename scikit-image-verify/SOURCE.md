# scikit-image Source

The upstream source tree is not committed to this repository.

## Upstream

- Repository: https://github.com/scikit-image/scikit-image.git
- Local path: `./scikit-image-verify/src/scikit-image`
- Verified commit: `93e9da980111f5f1b20e4f97d2067d6f301d25e2`

## Clone

Run from the `tool-verify` root:

```bash
mkdir -p ./scikit-image-verify/src
git clone https://github.com/scikit-image/scikit-image.git ./scikit-image-verify/src/scikit-image
```

Record the exact commit after cloning:

```bash
git -C ./scikit-image-verify/src/scikit-image rev-parse HEAD
git -C ./scikit-image-verify/src/scikit-image status --short
```
