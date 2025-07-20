from pathlib import Path


def get_vm_files_to_process(input_vm: Path) -> list[str]:
    """
    Get all the '.vm' files to process.

    Handling depends on whether the input path is a directory or a file.
    """
    if input_vm.is_dir():
        vm_files_to_process = [str(vm_file) for vm_file in input_vm.glob("*.vm")]
        if not vm_files_to_process:
            msg = f"No '.vm' files found in directory: {str(input_vm)}"
            raise ValueError(msg)
        return vm_files_to_process

    if not str(input_vm).endswith(".vm"):
        msg = "Input file is not a valid '.vm' file"
        raise ValueError(msg)
    return [str(input_vm)]
