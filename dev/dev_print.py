def print_dev(string, config = {'verbose': 'true'}):
    if config['verbose'] in ['True', 'TRUE', 'true']:
        print(string)
