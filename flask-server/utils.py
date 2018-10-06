import os

def DEV_PROD_VALUE(dev_value, prod_value):
    stage = os.environ.get('stage')
    if stage == 'prod':
        return prod_value
    return dev_value