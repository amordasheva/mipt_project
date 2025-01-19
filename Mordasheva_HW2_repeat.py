import random

def repeat(x):
    def decorator(f):
        def wrapper(*args, **kwargs):
          results = []
          for i in range(x):
            results.append(f(*args, **kwargs))
          return tuple(results)

        return wrapper
    return decorator


@repeat(50)
def random_sum(n):
    return sum(random.random() for i in range(n))

print(random_sum(1000000))