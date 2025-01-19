def even(f):
    count = 0

    def wrapper(*args, **kwargs):
      nonlocal count
      count += 1
      if count % 2 != 0:
        pass
      else:
        return f(*args, **kwargs)

    return wrapper

@even
def print_hello(x):
    print("hello", x)

print_hello(1)
print_hello(2)
print_hello(3)
print_hello(4)