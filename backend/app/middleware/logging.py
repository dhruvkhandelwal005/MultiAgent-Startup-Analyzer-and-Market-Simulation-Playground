import time
import functools


def log_agent_call(agent_role: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            print(f"[AGENT START] role={agent_role}")
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"[AGENT END] role={agent_role} latency={elapsed:.2f}s")
            return result
        return wrapper
    return decorator