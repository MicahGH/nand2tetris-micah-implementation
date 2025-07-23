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
        @{self.command_specifier}
        0;JMP
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
        push_local_var = """
        @R0
        D=A

        @SP
        A=M
        M=D

        @SP
        M=M+1
        """
        local_vars_to_push = [push_local_var for _ in range(self.command_value)]

        return [insert_function_label, *local_vars_to_push]


class ReturnCommand(BaseFunctionCommand):
    # Return commands don't have a specifier or a value
    command_specifier: None  # type: ignore[reportGeneralTypeIssues]
    command_value: None  # type: ignore[reportGeneralTypeIssues]

    def translate_to_asm(self) -> list[str]:
        end_frame_var_name = "end_frame"
        return_address_var_name = "return_address"
        get_end_frame = f"""
        @LCL
        D=M
        @{end_frame_var_name}
        M=D
        """

        get_return_address = f"""
        @R5
        D=A

        @{end_frame_var_name}
        D=M-D
        A=D
        D=M

        @{return_address_var_name}
        M=D
        """
        pop_top_value_to_arg = """
        @SP
        M=M-1

        A=M
        D=M

        @ARG
        A=M
        M=D
        """
        reposition_sp = """
        @ARG
        D=M+1

        @SP
        M=D
        """
        recover_that = f"""
        @R1
        D=A

        @{end_frame_var_name}
        D=M-D

        @temp_var_that
        A=D
        D=M

        @THAT
        M=D
        """
        recover_this = f"""
        @R2
        D=A

        @{end_frame_var_name}
        D=M-D

        @temp_var_this
        A=D
        D=M

        @THIS
        M=D
        """
        recover_arg = f"""
        @R3
        D=A

        @{end_frame_var_name}
        D=M-D

        @temp_var_arg
        A=D
        D=M

        @ARG
        M=D
        """
        recover_lcl = f"""
        @R4
        D=A

        @{end_frame_var_name}
        D=M-D

        @temp_var_lcl
        A=D
        D=M

        @LCL
        M=D
        """
        goto_return_address = f"""
        @{return_address_var_name}
        A=M
        0;JMP
        """
        return [
            get_end_frame
            + get_return_address
            + pop_top_value_to_arg
            + reposition_sp
            + recover_that
            + recover_this
            + recover_arg
            + recover_lcl
            + goto_return_address
        ]
