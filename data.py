import sys
import json

from faker import Faker
fake = Faker()


if __name__ == "__main__":
    n = int(sys.argv[1])

    for _ in range(n):
        data = {}
        data['name'] = fake.name()
        data['bool'] = fake.boolean()
        data['abc']  = fake.random_choices(elements=('a', 'b', 'c'), length=1)[0]
        data['int']  = fake.pyint()
        data['true'] = fake.boolean(chance_of_getting_true=99.99)

        print(json.dumps(data))
