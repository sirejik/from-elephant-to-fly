import argparse
import logging
import sys

from settings import LOG_FILE_NAME, WORD_LENGTH
from utils import configure_logging, dijkstra, init_graph, print_result, read_dictionary, GameException


logger = logging.getLogger()


def main():
    configure_logging()
    logger.info('The from-elephant-to-fly game was started.')
    try:
        from_word, to_word = parse_options()
        result = run(from_word, to_word)
        print_result(*result)
    except GameException as e:
        logger.info('The from-elephant-to-fly game was stopped with the following error: {}.'.format(e))
        return 1
    except SystemExit as e:
        logger.info('The from-elephant-to-fly game finished work with the exit code {exit_code}.'.format(
            exit_code=e.code
        ))
        return e.code
    except Exception as e:
        logger.debug('An unexpected error occurred: %s' % str(e), **{'exc_info': 1})
        logger.error('An unexpected error occurred. See the details in the log file \'%s\'.' % LOG_FILE_NAME)
        return 1


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--from-word', type=str, required=True, metavar='FROM', help='The word with which the game will start.'
    )
    parser.add_argument(
        '--to-word', type=str, required=True, metavar='TO', help='The word with which the game will finish.'
    )
    options = parser.parse_args()
    from_word, to_word = options.from_word, options.to_word
    if len(from_word) != WORD_LENGTH or len(to_word) != WORD_LENGTH:
        raise GameException('only words of length 4 are suitable for the game')

    return options.from_word, options.to_word


def run(from_word, to_word):
    dictionary = read_dictionary()
    graph = init_graph(dictionary)
    return dijkstra(graph, graph.get_node(from_word), graph.get_node(to_word))


if __name__ == '__main__':
    sys.exit(main())
