import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('IO.ini')

def get_train():
    return config.get('input', 'enroll_train')

def get_train_log():
    return config.get('input', 'log_train')

def get_test():
    return config.get('input', 'enroll_test')

def get_test_log():
    return config.get('input', 'log_test')

def get_sample():
    return config.get('input', 'sample')

def get_submission():
    return config.get('output', 'submission')

def get_object():
    return config.get('input', 'object')