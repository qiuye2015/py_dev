#!/usr/bin/env python
import optparse
import os

USER = os.environ.get('USER') or 'root'


def get_option_parser():
    usage = 'usage: %prog [-e engine_name, other options] module1, module2 ...'
    parser = optparse.OptionParser(usage=usage)
    basic = optparse.OptionGroup(parser, 'Basic test options')
    basic.add_option(
        '-e',
        '--engine',
        dest='engine',
        help=(
            'Database engine to test, one of '
            '[sqlite, postgres, mysql, mysqlconnector, apsw, sqlcipher,'
            ' cockroachdb]'
        ),
    )
    basic.add_option('-v', '--verbosity', dest='verbosity', default=1, type='int', help='Verbosity of output')
    basic.add_option(
        '-f', '--failfast', action='store_true', default=False, dest='failfast', help='Exit on first failure/error.'
    )
    basic.add_option(
        '-s', '--slow-tests', action='store_true', default=False, dest='slow_tests', help='Run tests that may be slow.'
    )
    parser.add_option_group(basic)

    db_param_map = (
        (
            'MySQL',
            'MYSQL',
            (
                # param  default disp default val
                ('host', 'localhost', 'localhost'),
                ('port', '3306', ''),
                ('user', USER, USER),
                ('password', 'blank', ''),
            ),
        ),
        (
            'Postgresql',
            'PSQL',
            (
                ('host', 'localhost', os.environ.get('PGHOST', '')),
                ('port', '5432', ''),
                ('user', 'postgres', os.environ.get('PGUSER', '')),
                ('password', 'blank', os.environ.get('PGPASSWORD', '')),
            ),
        ),
        (
            'CockroachDB',
            'CRDB',
            (
                # param  default disp default val
                ('host', 'localhost', 'localhost'),
                ('port', '26257', ''),
                ('user', 'root', 'root'),
                ('password', 'blank', ''),
            ),
        ),
    )
    for name, prefix, param_list in db_param_map:
        group = optparse.OptionGroup(parser, '%s connection options' % name)
        for param, default_disp, default_val in param_list:
            dest = '%s_%s' % (prefix.lower(), param)
            opt = '--%s-%s' % (prefix.lower(), param)
            group.add_option(
                opt, default=default_val, dest=dest, help=('%s database %s. Default %s.' % (name, param, default_disp))
            )

        parser.add_option_group(group)
    return parser


class PeeweeException(Exception):
    def __init__(self, *args):
        if args and isinstance(args[0], Exception):
            self.orig, args = args[0], args[1:]
        super(PeeweeException, self).__init__(*args)


class DatabaseError(PeeweeException):
    pass


class DataError(DatabaseError):
    pass


class InternalError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass


def test_raise_error():
    raise InternalError('Connection already opened.')


if __name__ == '__main__':
    parser = get_option_parser()
    options, args = parser.parse_args()
    pass
