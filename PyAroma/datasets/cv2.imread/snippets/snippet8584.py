from ..utils import *


def load_semantic(image_src, label_src, target_size, scale, mirror, rand_crop, downsample=None):
    img = cv2.imread(image_src)
    (h, w) = img.shape[:2]
    seg = (cv2.imread(label_src, 0) if (label_src is not None) else np.full((h, w), 255, np.uint8))
    if mirror:
        img = img[(:, ::(- 1))]
        seg = seg[(:, ::(- 1))]
    if (scale != 1):
        h = int(((h * scale) + 0.5))
        w = int(((w * scale) + 0.5))
        img = cv2.resize(img, (w, h))
        seg = cv2.resize(seg, (w, h), interpolation=cv2.INTER_NEAREST)
    pad_h = max((target_size - h), 0)
    pad_w = max((target_size - w), 0)
    if ((pad_h > 0) or (pad_w > 0)):
        img = cv2.copyMakeBorder(img, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT)
        seg = cv2.copyMakeBorder(seg, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT)
        (h, w) = img.shape[:2]
    if rand_crop:
        h_bgn = np.random.randint(0, ((h - target_size) + 1))
        w_bgn = np.random.randint(0, ((w - target_size) + 1))
    else:
        h_bgn = ((h - target_size) // 2)
        w_bgn = ((w - target_size) // 2)
    img = img[(h_bgn:(h_bgn + target_size), w_bgn:(w_bgn + target_size))]
    seg = seg[(h_bgn:(h_bgn + target_size), w_bgn:(w_bgn + target_size))]
    if downsample:
        d_size = (((target_size - 1) // downsample) + 1)
        seg = cv2.resize(seg, (d_size, d_size))
    return (img, seg)
