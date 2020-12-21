from products.utils import random_string_generator, unique_slug_generator
import random
import string

def unique_order_id_generator(instance):
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id