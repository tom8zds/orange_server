from datetime import datetime
from io import FileIO
from typing import Any

from inspect import FrameInfo, stack


class Logger:
    log:FileIO
    level = "INFO"

    def __init__(self) -> None:
        self.log = open("log.txt", mode="a", encoding="utf-8")

    def output(self, msg:str, level:str, frame:FrameInfo):
        time = datetime.now().time().isoformat()
        file = frame.filename.replace("\\","/").split("/")[-1].replace(".py", "")
        log = f"{time} | {level} | {file} : {frame.function} : {frame.lineno} - {msg} \n"
        self.log.write(log)
        if(self.level == level):
            print(log)

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None: 
        msg = str(msg).format(args, kwargs)
        self.output(msg, "INFO", stack()[1])

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None: 
        msg = str(msg).format(args, kwargs)
        self.output(msg, "DEBUG", stack()[1])

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None: 
        msg = str(msg).format(args, kwargs)
        self.output(msg, "ERROR", stack()[1])

logger = Logger()