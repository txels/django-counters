# Django Counters

Make it easy to implement django fields that are backed by Redis counters.
These fields are initialised by loading the next incremented value of a given
Redis counter. Values should not be altered after an initial save.
