from exam.core.dataobjects.bases.Pet import Pet


class Cat(Pet):

    def info(self):
        print('I am a cat and I am called', self.name)


