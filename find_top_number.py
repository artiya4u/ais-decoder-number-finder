import json
import operator


def is_prime(num):
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                return False
        else:
            return True


if __name__ == '__main__':
    numbers = []
    with open('number.txt') as fp:
        for line in fp:
            detail = json.loads(line)
            numbers.append(detail)

    numbers.sort(key=operator.itemgetter('power'), reverse=True)

    print('Top 100 power numbers:')
    count = 0
    with open("top_number.txt", "w") as f:
        for s in numbers:
            f.write(json.dumps(s) + '\n')
            if count < 100:
                count += 1
                print(s)

    print('\nFinding prime number...')
    with open("top_number_prime.txt", "a") as f:
        for s in numbers:
            if is_prime(int(s['number'])):
                print(s)
                f.write(json.dumps(s) + '\n')
                f.flush()
