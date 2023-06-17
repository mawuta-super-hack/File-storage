import logging

my_logger = logging.getLogger('base.py')
my_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='tasks.log', mode='a', encoding='UTF-8')
my_logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(funcName)s, %(message)s'
)
handler.setFormatter(formatter)
