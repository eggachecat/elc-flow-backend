from libs.models import FunctionModel


def create_elc_function():
    FunctionModel.create(name='elc_add', outputs=['sum'])
