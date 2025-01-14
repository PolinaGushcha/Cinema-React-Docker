from enum import Enum


class UpdateStatus(str, Enum):
    FAIL = "fail"
    SUCCESS = "success"
