import os


def init_debug_mode():
    if (os.getenv('IS_OFFLINE', False) == 'true' or os.getenv('IS_LOCAL', False) == 'true') \
            and os.getenv('DEBUG') == 'true':
        print('Debug is on')
        import pydevd_pycharm
        pydevd_pycharm.settrace('localhost', port=8050, stdoutToServer=True, stderrToServer=True, suspend=False)
    else:
        print('Debug is off')
