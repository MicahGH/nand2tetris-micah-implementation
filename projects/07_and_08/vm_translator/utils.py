from pathlib import Path


def get_vm_files_to_process(input_vm_path: Path) -> list[Path]:
    """Get all the '.vm' files to process.

    Handling depends on whether the input path is a directory or a file.
    """
    if input_vm_path.is_dir():
        vm_files_to_process = [Path(vm_file) for vm_file in input_vm_path.glob("*.vm")]
        if not vm_files_to_process:
            msg = f"No '.vm' files found in directory: {input_vm_path!s}"
            raise ValueError(msg)
        return vm_files_to_process

    if input_vm_path.suffix != ".vm":
        msg = "Input file is not a valid '.vm' file"
        raise ValueError(msg)
    return [Path(input_vm_path)]
