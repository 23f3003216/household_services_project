from flask_caching import Cache

def init_cache(app):
    cache = Cache()
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 30
    app.config['CACHE_REDIS_HOST'] = "localhost"
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/0"
    cache.init_app(app)
    return cache
