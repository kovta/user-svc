# utils.py
import trafaret as T


TRAFARET = T.Dict({
    T.Key('couchbase'):
        T.Dict({
            'bucket': T.String(),
            'collection': T.String(),
            'user': T.String(),
            'password': T.String(),
            'host': T.String(),
            'port': T.Int(),
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
})
