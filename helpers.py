import faker
import random

fake = faker.Faker()


def get_sign_up_data():
    name = fake.name()
    email = f"{fake.email().split('@')[0]}_{random.randint(1000, 9999)}@example.com"
    password = fake.password()
    return name, email, password

