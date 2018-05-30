from ftw.logo.image import Image


def make_raw():
    def raw(src):
        return Image(src, 'svg')
    return raw


def make_resizer(width=0, height=0, extension='png'):
    def resizer(src):
        img = Image(src, extension)
        img.sample(width, height)
        return img
    return resizer


def make_transformer(width='', height='', extension='png'):
    def transformer(src):
        img = Image(src, extension)
        img.transform(resize='{}x{}'.format(width, height))
        return img
    return transformer


def make_ico_converter():
    ICO_SCALES = [
        make_resizer(16, 16),
        make_resizer(32, 32),
        make_resizer(48, 48),
    ]

    def converter(src):
        scales = map(lambda resizer: resizer(src), ICO_SCALES)

        def merge_scales(first, other):
            first.format = 'ico'
            first.append(other)
            other.close()
            return first

        return reduce(merge_scales, scales)
    return converter


def flatten_scales(scales):
    merged = scales['LOGOS'].copy()
    merged.update(scales['ICONS'])
    return merged


SCALES = {
    'LOGOS': {
        'LOGO':             make_transformer(height=80),
        'MOBILE_LOGO':      make_transformer(height=50),
        'BASE':             make_raw(),
    },
    'ICONS': {
        'APPLE_TOUCH_ICON': make_resizer(180, 180),
        'FAVICON_32X32':    make_resizer(32, 32),
        'FAVICON_16X16':    make_resizer(16, 16),
        'MSTILE_150X150':   make_resizer(150, 150),
        'ANDROID_192X192':  make_resizer(192, 192),
        'ANDROID_512X512':  make_resizer(512, 512),
        'FAVICON':          make_ico_converter(),
        'BASE':             make_raw(),
    }
}


def convert(source, scale):
    scales = flatten_scales(SCALES)
    if scale not in scales:
        raise Exception('scale: {} is not supported'.format(scale))
    return scales[scale](source)
