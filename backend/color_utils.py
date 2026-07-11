import numpy as np
from collections import Counter

def get_dominant_color(image_crop):

    img = np.array(image_crop)
    img = img.reshape(-1, 3)

    # Remove very dark pixels (noise)
    img = img[np.sum(img, axis=1) > 30]

    if len(img) == 0:
        return "unknown"

    colors = Counter([tuple(pixel) for pixel in img])
    dominant = colors.most_common(1)[0][0]

    r, g, b = dominant

    # Simple color naming
    if r > 200 and g > 200 and b > 200:
        return "white"
    if r < 50 and g < 50 and b < 50:
        return "black"
    if r > g and r > b:
        return "red"
    if g > r and g > b:
        return "green"
    if b > r and b > g:
        return "blue"
    if r > 150 and g > 100:
        return "yellow"
    return "mixed"
