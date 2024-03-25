import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()
producer_done = False
count = 0

def producer():
    global count, buffer, producer_done
    while count < MAX_COUNT:
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            count += 1
        with open('all.txt', 'a') as f:
            f.write(str(num) + '\n')
    producer_done = True

def customer_even():
    while not producer_done or buffer:
        with lock:
            if buffer and buffer[-1] % 2 == 0:
                num = buffer.pop()
                with open('odd.txt', 'a') as f:
                    f.write(str(num) + '\n')

def customer_odd():
    while not producer_done or buffer:
        with lock:
            if buffer and buffer[-1] % 2 != 0:
                num = buffer.pop()
                with open('even.txt', 'a') as f:
                    f.write(str(num) + '\n')

if __name__ == '__main__':
    producer_thread = threading.Thread(target=producer)
    customer_even_thread = threading.Thread(target=customer_even)
    customer_odd_thread = threading.Thread(target=customer_odd)

    producer_thread.start()
    customer_even_thread.start()
    customer_odd_thread.start()

    producer_thread.join()
    customer_even_thread.join()
    customer_odd_thread.join()

    print('Program Completed')
