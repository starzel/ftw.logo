from ftw.upgrade import UpgradeStep


class MoveBASEToLOGO(UpgradeStep):
    """Move BASE to LOGO.
    """

    def __call__(self):
        self.move_base_to_logo_field()
        self.install_upgrade_profile()

    def move_base_to_logo_field(self):
        query = {'object_provides': 'ftw.logo.manual_override.IManualOverrides'}

        for obj in self.objects(query, 'Remove unused annotation infos'):
            if hasattr(obj, 'logo_BASE'):
                base_image = obj.logo_BASE
                if base_image:
                    obj.logo_LOGO = base_image
