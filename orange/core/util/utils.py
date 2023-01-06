def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(f'{message=} \n')

def write_template(message: str):
    with open("log.html", mode="w+") as log:
        log.flush()
        log.write(message)
