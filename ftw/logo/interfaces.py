from zope.interface import Interface


class IFtwLogo(Interface):
    """ftw.logo Browser Layer
    """


class IIconConfig(Interface):
    """Adapter interface for logo customization adapter.
    """

    def __init__(file):
        """Adapts the zope application.
        """


class ILogoConfig(Interface):
    """Adapter interface for logo customization adapter.
    """

    def __init__(file):
        """Adapts the zope application.
        """
