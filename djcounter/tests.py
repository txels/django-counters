from djcounter import *  # NOQA


class SomeClass(UniqueIdMixin):
    key_name = 'something'


class OtherClass(UniqueIdMixin):
    pass


class Model(object):
    def save(self, *args, **kwargs):
        for f, c in self.counter_fields:
            print("{} = {}".format(f, self.latest(c)))


class DummyModel(CounterModelMixin, Model):

    counter_fields = [
        ('a', 'a'),
        ('b', 'b'),
    ]
    id = None
