from models.arithmetic import (
    AddCommand,
    AndCommand,
    EqCommand,
    GtCommand,
    LtCommand,
    NegCommand,
    NotCommand,
    OrCommand,
    SubCommand,
)
from models.base import BaseCommand, CommandSpecifierType, CommandType
from models.memory_access import (
    PopCommand,
    PopPointerCommand,
    PopStaticCommand,
    PopTempCommand,
    PushCommand,
    PushConstantCommand,
    PushPointerCommand,
    PushStaticCommand,
    PushTempCommand,
)

COMMAND_TYPE_COMMAND_CLASS_MAP: dict[
    CommandType, type[BaseCommand] | dict[CommandSpecifierType | str, type[BaseCommand]]
] = {
    CommandType.ADD: AddCommand,
    CommandType.SUB: SubCommand,
    CommandType.NOT: NotCommand,
    CommandType.AND: AndCommand,
    CommandType.OR: OrCommand,
    CommandType.NEG: NegCommand,
    CommandType.EQ: EqCommand,
    CommandType.GT: GtCommand,
    CommandType.LT: LtCommand,
    CommandType.PUSH: {
        CommandSpecifierType.POINTER: PushPointerCommand,
        CommandSpecifierType.CONSTANT: PushConstantCommand,
        CommandSpecifierType.TEMP: PushTempCommand,
        CommandSpecifierType.STATIC: PushStaticCommand,
        "default": PushCommand,
    },
    CommandType.POP: {
        CommandSpecifierType.POINTER: PopPointerCommand,
        CommandSpecifierType.TEMP: PopTempCommand,
        CommandSpecifierType.STATIC: PopStaticCommand,
        "default": PopCommand,
    },
}
