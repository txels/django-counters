import redis


class Counter(object):

    def __init__(self, host='localhost', port=6379, namespace='rbx'):
        self._redis = redis.StrictRedis(host=host, port=port, db=0)
        self._namespace = namespace

    def _name(self, counter):
        return '{}.{}'.format(self._namespace, counter)

    def next(self, counter):
        """
        Get the next value for the counter.
        """
        return self._redis.incr(self._name(counter))

    def latest(self, counter):
        """
        Get the latest known value for the counter.
        """
        return self._redis.get(self._name(counter))


class UniqueIdMixin(object):
    """
    Mix in to any django model where you want a unique id based on a counter.

    A ``next_id`` method will give you a next unique ID based on the class
    name, lowercased.
    """
    def __init__(self, host='localhost', port=6379, namespace='rbx'):
        self._counter = Counter(host, port, namespace)

    @property
    def _key_name(self):
        return self.__class__.__name__.lower()

    def next_id(self):
        return self._counter.next(self._key_name)


class CounterModelMixin(Counter):
    """
    Mix in to your Django models where you want certain fields as counters.

    """
    # list of tuples (field_name, counter_name)
    counter_fields = []

    def save(self, *args, **kwargs):
        if not self.id:
            for f, c in self.counter_fields:
                setattr(self, f, self.next(c))
        super(CounterModelMixin, self).save(*args, **kwargs)
