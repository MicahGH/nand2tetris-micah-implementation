from models.base import BaseCommand, BaseCommandType


class FunctionCommandType(BaseCommandType):
    FUNCTION = "function"
    CALL = "call"
    RETURN = "return"


class BaseFunctionCommand(BaseCommand):
    command: FunctionCommandType  # type: ignore[reportGeneralTypeIssues]
    # Function command specifiers cannot be Enums as they are user-defined
    command_specifier: str  # type: ignore[reportGeneralTypeIssues]
    command_value: int  # type: ignore[reportGeneralTypeIssues]


class CallCommand(BaseFunctionCommand):
    def translate_to_asm(self) -> list[str]:
        return_address_label = self.command_specifier + str(self.line_number)
        push_return_address = f"""
        @{return_address_label}
        D=A

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        push_lcl = """
        @LCL
        D=M

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        push_arg = """
        @ARG
        D=M

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        push_this = """
        @THIS
        D=M

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        push_that = """
        @THAT
        D=M

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        reposition_arg = f"""
        @SP
        D=M

        @R5
        M=A
        D=D-M

        @{self.command_value}
        M=A
        D=D-M

        @ARG
        M=D
        """
        reposition_lcl = """
        @SP
        D=M

        @LCL
        M=D
        """
        goto_function = f"""
        goto {self.command_specifier}
        """
        insert_return_address_label = f"""
        ({return_address_label})
        """
        return [
            push_return_address
            + push_lcl
            + push_arg
            + push_this
            + push_that
            + reposition_arg
            + reposition_lcl
            + goto_function
            + insert_return_address_label,
        ]


class FunctionCommand(BaseFunctionCommand):
    def translate_to_asm(self) -> list[str]:
        insert_function_label = f"""
        ({self.command_specifier})
        """
        local_vars_to_push: list[str] = []
        push_local_var = """
        @R0
        D=M

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        local_vars_to_push = [push_local_var for i in range(self.command_value)]

        return [insert_function_label, *local_vars_to_push]


class ReturnCommand(BaseFunctionCommand):
    # Return commands don't have a specifier or a value
    command_specifier: None  # type: ignore[reportGeneralTypeIssues]
    command_value: None  # type: ignore[reportGeneralTypeIssues]

    def translate_to_asm(self) -> list[str]:
        return []
