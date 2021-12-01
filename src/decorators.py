import logging
logger = logging.getLogger(__name__)


def cache(ttl=0):
    def cache_decorator(func):
        import time
        cached = {}
        cached_ttls = {}

        def wrapper(*args, **kwargs):
            key = (*args,) + tuple([(k, v) for k, v in kwargs.items()])

            if ttl != 0:
                while True:
                    try:
                        oldest_key, *_ = list(cached.keys())
                    except ValueError:
                        break

                    if cached_ttls[oldest_key] < time.time():
                        del cached[oldest_key]
                    else:
                        break

            if key in cached:
                result = cached[key]
                result["cached"] = True
                logger.info(f"Get cached data of {key[1]}")

            else:
                result = func(*args, **kwargs)
                cached[key] = result

                if ttl != 0:
                    cached_ttls[key] = time.time() + ttl

            return result
        return wrapper
    return cache_decorator
