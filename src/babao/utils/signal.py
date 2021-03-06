"""Signal handling"""

import signal

EXIT = 0
SIG_HANDLER = None


def _signalHandler(signal_code, unused_frame):
    """Just store the exit status, for later safe exiting"""
    global EXIT
    EXIT = 128 + signal_code


def catchSignal():
    """Catch signal INT/TERM, so we won't exit while playing with data files"""
    global SIG_HANDLER
    if SIG_HANDLER is None:
        SIG_HANDLER = {}
    SIG_HANDLER.setdefault(
        signal.SIGINT,
        signal.signal(signal.SIGINT, _signalHandler)
    )
    SIG_HANDLER.setdefault(
        signal.SIGTERM,
        signal.signal(signal.SIGTERM, _signalHandler)
    )


def restoreSignal():
    """Restore the previous signal handler"""
    signal.signal(signal.SIGINT, SIG_HANDLER[signal.SIGINT])
    signal.signal(signal.SIGTERM, SIG_HANDLER[signal.SIGTERM])
