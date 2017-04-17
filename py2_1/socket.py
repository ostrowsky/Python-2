def decorator(func):
    def decorated(text):
        new_args = '<b>' + text + '</b>'
        return func(new_args)
    return decorated


def hello(text):
    print(text)


c = decorator(hello)
print(c)
c('you')
