import string
import random


def code_generator(size, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))



def get_unique_code(size, model_):
    code = code_generator(size)
    qs = model_.objects.filter(activation_code=code)
    return get_unique_code(size, model_) if qs.exists() else code