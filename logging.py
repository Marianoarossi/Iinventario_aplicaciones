import datetime


def decorator_log(function):
    def logging(*args, **kwargs):
        date_proc = datetime.date.today()
        time_proc = datetime.datetime.now()
        func_proc = function.__name__
        log_proc = armar_log(args)
        logging.log_to_save = f"{date_proc} {func_proc} {time_proc} {log_proc}\n"
        file_log = open("log_inventario.txt", "a")
        file_log.write(logging.log_to_save)
        file_log.close()
        return function(*args, **kwargs)

    logging.log_to_save = ''
    return logging


def armar_log(args):
    log: str = ''
    for valor in args:
        if type(valor) == str:
            log += ', ' + valor
        elif type(valor) == int:
            log += ', ' + str(valor)

    return log


def decorator_log_nf(cls):
    class Logging:
        def __init__(self, func) -> None:
            self.func = func

        def __call__(self, *args):
            date_proc = datetime.date.today()
            func_proc = self.func.__name__
            # log_proc = ', '.join(args)
            file_log = open("log_inventario.txt", "a")
            file_log.write(f"{date_proc} {func_proc}  \n")
            file_log.close()

    return Logging
