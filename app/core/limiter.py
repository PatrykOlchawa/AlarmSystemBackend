from fastapicap import RateLimiter

login_rate_limiter = RateLimiter(
    limit=5,
    minutes=1,
)

pin_rate_limiter = RateLimiter(
    limit =10,
    minutes=1,
)