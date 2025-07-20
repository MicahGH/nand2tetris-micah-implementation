from models.arithmetic import (
    AddCommand,
    AndCommand,
    ArithmeticCommandType,
    EqCommand,
    GtCommand,
    LtCommand,
    NegCommand,
    NotCommand,
    OrCommand,
    SubCommand,
)
from models.base import BaseCommand, CommandSpecifierType, BaseCommandType
from models.memory_access import (
    MemoryAccessCommandType,
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
    BaseCommandType, type[BaseCommand] | dict[CommandSpecifierType | str, type[BaseCommand]]
] = {
    ArithmeticCommandType.ADD: AddCommand,
    ArithmeticCommandType.SUB: SubCommand,
    ArithmeticCommandType.NOT: NotCommand,
    ArithmeticCommandType.AND: AndCommand,
    ArithmeticCommandType.OR: OrCommand,
    ArithmeticCommandType.NEG: NegCommand,
    ArithmeticCommandType.EQ: EqCommand,
    ArithmeticCommandType.GT: GtCommand,
    ArithmeticCommandType.LT: LtCommand,
    MemoryAccessCommandType.PUSH: {
        CommandSpecifierType.POINTER: PushPointerCommand,
        CommandSpecifierType.CONSTANT: PushConstantCommand,
        CommandSpecifierType.TEMP: PushTempCommand,
        CommandSpecifierType.STATIC: PushStaticCommand,
        "default": PushCommand,
    },
    MemoryAccessCommandType.POP: {
        CommandSpecifierType.POINTER: PopPointerCommand,
        CommandSpecifierType.TEMP: PopTempCommand,
        CommandSpecifierType.STATIC: PopStaticCommand,
        "default": PopCommand,
    },
}
