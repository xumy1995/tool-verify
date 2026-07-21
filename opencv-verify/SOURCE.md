# OpenCV Sources

The upstream source trees are not committed to this verification repository.

## Repositories

```text
opencv:         https://github.com/opencv/opencv.git
opencv_contrib: https://github.com/opencv/opencv_contrib.git
opencv_extra:   https://github.com/opencv/opencv_extra.git
```

## Verified Revisions

```text
opencv:         7aa163b83f5a32be7f43a0b9837584ca7460238b
opencv_contrib: a8e9acd62cabd30419dba83007f2ac0d07de5e2c
opencv_extra:   f202151dfb4734e47399ddf6581183d423da74b4
```

## Recreate Source Directory

```bash
mkdir -p /data/xumengying/opencv-verify/src
cd /data/xumengying/opencv-verify/src

git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
git clone https://github.com/opencv/opencv_extra.git

git -C opencv checkout 7aa163b83f5a32be7f43a0b9837584ca7460238b
git -C opencv_contrib checkout a8e9acd62cabd30419dba83007f2ac0d07de5e2c
git -C opencv_extra checkout f202151dfb4734e47399ddf6581183d423da74b4
```

If `opencv_extra` is cloned with `--depth=1`, some older or newer test-data history may be unavailable. Use a full clone when debugging missing test data.

