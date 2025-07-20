"""Writer that writes the translated data from the '.vm' file to an '.asm' file."""

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeWriter:
    def __init__(self, output_asm_file_path: str, translated_lines: list[str]) -> None:
        """Initialise the CodeWriter class."""
        self.output_asm_file_path = self.check_valid_asm_file(output_asm_file_path)
        self.translated_lines = translated_lines

    def check_valid_asm_file(self, output_asm_file_path: str) -> str:
        if output_asm_file_path.endswith(".asm"):
            return output_asm_file_path
        msg = f"Not a valid filepath to an '.asm' file: {output_asm_file_path}"
        raise ValueError(msg)

    def write_file(self) -> None:
        with open(self.output_asm_file_path, "w") as asm_file:
            logger.info("Created / Opened ASM file.")
            for translated_line in self.translated_lines:
                asm_file.write(translated_line)
        logger.info("Finished creating ASM file.")
