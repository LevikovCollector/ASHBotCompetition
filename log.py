import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                                filename=u'logs\log.log')


def add_log_row(message, t_message='mes'):
    if t_message == 'mes':
        logging.info(message)
    elif t_message == 'war':
        logging.warning(message)