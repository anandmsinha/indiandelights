ma = raw_input()
a, b = ma.split(' ')
a, b = int(a), int(b)

op = ['FizzBuzz' if x % 15 == 0 else 'Fizz' if x % 3 == 0 else 'Buzz' if x % 5 ==0 else x for x in range(a, b + 1)]

print " ".join(str(v) for v in op)