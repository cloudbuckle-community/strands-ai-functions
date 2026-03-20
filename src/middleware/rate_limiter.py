import time
from collections import defaultdict


class SlidingWindowRateLimiter:
    """Per-user rate limiter using a sliding window counter."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Remove expired timestamps
        self._requests[user_id] = [
            ts for ts in self._requests[user_id] if ts > window_start
        ]

        if len(self._requests[user_id]) >= self.max_requests:
            return False

        self._requests[user_id].append(now)
        return True

    def remaining(self, user_id: str) -> int:
        now = time.time()
        window_start = now - self.window_seconds
        active = [ts for ts in self._requests[user_id] if ts > window_start]
        return max(0, self.max_requests - len(active))
