from inspect import _void
import logging


def print_heading1_message (message: str) -> _void:
    separator : str = '#'
    middle_message = ''.join(['', separator, ' ', message, ' ', separator])
    container_line = ['']
    empty_line = ['']
    for i, char in enumerate(middle_message):
        container_line.append(separator)
        if i ==0 or i == len(middle_message)-1:
            empty_line.append(separator)
        else:
            empty_line.append(' ')

    logging.info('\n')
    logging.info('\n')
    logging.info(''.join(container_line))
    logging.info(''.join(empty_line))
    logging.info(middle_message)
    logging.info(''.join(empty_line))
    logging.info(''.join(container_line))
    logging.info('\n')
    logging.info('\n')

def print_heading2_message(message: str) -> _void:
    separator : str = '-'
    middle_message = ''.join(['', separator, ' ', message, ' ', separator])
    container_line = ['']
    empty_line = ['']
    for i, char in enumerate(middle_message):
        container_line.append(separator)
        if i ==0 or i == len(middle_message)-1:
            empty_line.append(separator)
        else:
            empty_line.append(' ')

    logging.info(''.join(container_line))
    logging.info(middle_message)
    logging.info(''.join(container_line))

def print_normal_message(message:str) -> _void:
    logging.info('\n')
    logging.info(message)
    logging.info('\n')