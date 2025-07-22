import logging

from models.base import BaseCommand, BaseCommandType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArithmeticCommandType(BaseCommandType):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class BaseArithmeticCommand(BaseCommand):
    command: ArithmeticCommandType  # type: ignore[reportGeneralTypeIssues]
    # These are never needed in arithmetic commands
    # so they are set to always be None
    command_specifier: None  # type: ignore[reportGeneralTypeIssues]
    command_value: None  # type: ignore[reportGeneralTypeIssues]


class AddCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        add_logic = """
        M=M+D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + add_logic + increment_pointer_addr]


class SubCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        sub_logic = """
        M=M-D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + sub_logic + increment_pointer_addr]


class NotCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        not_value = """
        M=!M
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + not_value + increment_pointer_addr]


class AndCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        and_logic = """
        M=M&D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + and_logic + increment_pointer_addr]


class OrCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        or_logic = """
        M=M|D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + or_logic + increment_pointer_addr]


class NegCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        neg_value = """
        M=-M
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + neg_value + increment_pointer_addr]


class EqCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        eq_logic = f"""
        D=D-M

        @EQUAL_{self.line_number}
        D;JEQ

        @NOT_EQUAL_{self.line_number}
        D;JNE

        (EQUAL_{self.line_number})
        @SP
        A=M
        M=-1
        @DONE_{self.line_number}
        0;JMP

        (NOT_EQUAL_{self.line_number})
        @SP
        A=M
        M=0
        @DONE_{self.line_number}
        0;JMP

        (DONE_{self.line_number})
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + eq_logic + increment_pointer_addr]


class GtCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        gt_logic = f"""
        D=M-D

        @GT_SUCCESS_{self.line_number}
        D;JGT

        @GT_FAILURE_{self.line_number}
        0;JMP

        (GT_SUCCESS_{self.line_number})
        @SP
        A=M
        M=-1
        @DONE_{self.line_number}
        0;JMP

        (GT_FAILURE_{self.line_number})
        @SP
        A=M
        M=0
        @DONE_{self.line_number}
        0;JMP

        (DONE_{self.line_number})
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + gt_logic + increment_pointer_addr]


class LtCommand(BaseArithmeticCommand):
    def translate_to_asm(self) -> list[str]:
        pop_value_1 = """
        @SP
        M=M-1
        A=M
        D=M
        """
        pop_value_2 = """
        @SP
        M=M-1
        A=M
        """
        lt_logic = f"""
        D=M-D

        @LT_SUCCESS_{self.line_number}
        D;JLT

        @LT_FAILURE_{self.line_number}
        0;JMP

        (LT_SUCCESS_{self.line_number})
        @SP
        A=M
        M=-1
        @DONE_{self.line_number}
        0;JMP

        (LT_FAILURE_{self.line_number})
        @SP
        A=M
        M=0
        @DONE_{self.line_number}
        0;JMP

        (DONE_{self.line_number})
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [pop_value_1 + pop_value_2 + lt_logic + increment_pointer_addr]
