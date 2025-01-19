def clip(f):
    def wrapper(*args, **kwargs):
      return f(*args)

    return wrapper


@clip
def print_clip(*args, **kwargs):
    print(*args, **kwargs)

print_clip(1, 2, z = 3, s = "_")
print_clip(1, 2, 3, sep = "_") 