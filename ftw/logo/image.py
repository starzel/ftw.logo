from wand.image import Image
import os


class Image(Image):

    def __init__(self, filename, extension=None):
        if not os.path.isfile(filename):
            raise ValueError('{} could not be found'.format(filename))

        self.filename = filename
        super(Image, self).__init__(filename=self.filename)

        if extension is None:
            filename, extension = os.path.splitext(filename)
            # from pdb import set_trace; set_trace()
            self.extension = extension.lstrip('.')
        else:
            self.extension = extension

        # behind format is a setter so the extension has to be kept seperately
        self.format = self.extension

        self._blob = None

    def make_blob(self):
        if self._blob:
            return self._blob
        # wand.py is not able to convert mvg to svg
        if self.extension == 'svg':
            with open(self.filename, 'r') as f:
                self._blob = f.read()
        else:
            self._blob = super(Image, self).make_blob(self.extension)
        self.close()
        return self._blob

    def append(self, other):
        self.sequence.append(other)
