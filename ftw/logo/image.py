from wand.image import Image


class Image(Image):

    def __init__(self, filename, extension):
        self.filename = filename
        # behind format is a setter so the extension has to be kept seperately
        self.extension = extension

        super(Image, self).__init__(filename=self.filename)
        self.format = self.extension

    def make_blob(self):
        # wand.py is not able to convert mvg to svg
        if self.extension == 'svg':
            return open(self.filename, 'r').read()
        return super(Image, self).make_blob(self.extension)

    def append(self, other):
        self.sequence.append(other)
