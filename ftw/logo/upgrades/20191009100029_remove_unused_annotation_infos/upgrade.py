from ftw.upgrade import UpgradeStep
from zope.annotation.interfaces import IAnnotations


class RemoveUnusedAnnotationInfos(UpgradeStep):
    """Remove unused annotation infos.
    """

    def __call__(self):
        self.cleanup_annotations(self.portal)
        self.install_upgrade_profile()

    def cleanup_annotations(self):
        query = {'object_provides': 'ftw.logo.manual_override.IManualOverrides'}
        key = 'ftw.logo.logo_overrides'

        for obj in self.objects(query, 'Remove unused annotation infos'):
            annotations = IAnnotations(obj)
            if key in annotations:
                del annotations[key]
