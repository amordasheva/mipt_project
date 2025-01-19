def cash(f):
    cash = dict()

    def wrapper(*args):
      if args in cash:
        return cash[args]
      else:
        result = f(*args)
        cash[args] = result
        return result

    return wrapper


@cash
def fib(x):
  print(f"вызвана функция Фибоначчи f({x})")
  if x < 2:
    return 1
  else:
    return fib(x-1) + fib(x-2)
  
print(fib(10))