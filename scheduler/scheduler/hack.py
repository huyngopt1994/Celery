from tasks import add

for _ in range(50):
    add.delay(4, 4)
