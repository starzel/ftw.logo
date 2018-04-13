from ftw.logo.converter import convert
from ftw.logo.converter import SCALES


def collect_icons(config):
    for scale in SCALES['ICONS']:
        config.add_scale(scale, convert(config.base, scale))


def collect_logos(config):
    for scale in SCALES['LOGOS']:
        config.add_scale(scale, convert(config.base, scale))
