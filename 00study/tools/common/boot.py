import logging
import signal
import sys
import time
from concurrent import futures

from flask import Flask

from tools.common import ftimes
from config import Config


class Boot(object):
    def __init__(self):
        super(Boot, self).__init__()
        self._boot_entry = []
        self._after_shutdown = None

    @staticmethod
    def start_server_and_wait():
        time.sleep(2)
        pass
        # app = Flask()
        # port = (int(sys.argv[1]) or 8080) if len(sys.argv) > 1 else 8080
        # app.run(port=port, host='0.0.0.0', debug=False)
        # logging.info('web server shutdown!!!')

    def add(self, name, fn_start, fn_close):
        self._boot_entry.append(
            {'name': name, 'fn_start': fn_start, 'fn_close': fn_close}
        )
        logging.info('add to start: %s', name)

    def set_after_shutdown(self, after_shutdown):
        """after_shutdown is a function"""
        self._after_shutdown = after_shutdown

    def boot(self):
        _start = ftimes.current_milliseconds()

        _black_list = Config.get('BOOT_BLACK_LIST')
        for e in self._boot_entry:
            _name = e['name']
            if _name in _black_list:
                logging.info('do not start: %s', _name)

            else:
                e['fn_start']()
                logging.info('start %s', _name)

        logging.info('start time cost: %sms', ftimes.current_milliseconds() - _start)

    def shutdown(self, parallel=True):
        _start = ftimes.current_milliseconds()

        def _do_close(entry):
            name, fn = entry['name'], entry['fn_close']
            try:
                logging.info("%s closing", name)
                fn()
                logging.info("%s closed", name)
            except Exception as ex:
                logging.error("error in close: %s, error: %s", name, ex)

        if parallel:
            pool = futures.ThreadPoolExecutor(max_workers=8)
            fs = []
            for e in self._boot_entry:
                fs.append(pool.submit(_do_close, e))

            for f in fs:
                try:
                    f.result()
                except BaseException as e:
                    logging.error(e)

            pool.shutdown()

        else:
            for e in self._boot_entry:
                _do_close(e)

        if self._after_shutdown:
            self._after_shutdown()

        _end = ftimes.current_milliseconds()
        logging.info('shutdown cost: %sms', _end - _start)

    def registry_exit_hook(self):
        def signal_handler(sig, frame):
            logging.info('got signal: {}. Server will exit.'.format(sig))
            self.shutdown()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


boot = Boot()

if __name__ == '__main__':
    boot.registry_exit_hook()
    boot.add('test_name', lambda: print("start"), lambda: print("end"))
    boot.boot()
    boot.start_server_and_wait()
