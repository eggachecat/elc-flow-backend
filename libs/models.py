import datetime

from peewee import Model
from playhouse.postgres_ext import *

from libs.envs import DATABASE_APP_PROXY

ELC_TABLES = []


def register_tables(cls):
    ELC_TABLES.append(cls)
    return cls


class BaseModel(Model):
    class Meta:
        database = DATABASE_APP_PROXY


@register_tables
class FunctionModel(BaseModel):
    name = TextField(unique=True)
    inputs = JSONField(null=True)
    outputs = JSONField(null=True)
    parameters = JSONField(null=True)
    description = TextField(null=True)
    display_name = TextField(null=True)

    class Meta:
        table_name = 'elc_function'


@register_tables
class GraphModel(BaseModel):
    graph = JSONField()

    class Meta:
        table_name = 'elc_graph'


@register_tables
class RunModel(BaseModel):
    # 跑的图
    graph = ForeignKeyField(GraphModel)
    # 跑的状态
    state = JSONField()

    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'elc_run'
