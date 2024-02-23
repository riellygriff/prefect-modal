# import modal
# import sys
from prefect import flow

# stub = modal.Stub('example-test')

# @stub.function()
# def f(i):
#     if i % 2 == 0:
#         print('hello', i)
#     else:
#         print('world',i, file=sys.stderr)
#     return i*i

# @stub.local_entrypoint()
# def main():
#     print(f.local(1000))

#     print(f.remote(999))

#     total = 0
#     for ret in f.map(range(20)):
#         total += ret
#     print(total)

@flow
def main():
    print('hello world')

if __name__ == main():
    main()