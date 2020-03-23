from login import tg

result = tg.get_me()
result.wait()
print(result.update['id'])
