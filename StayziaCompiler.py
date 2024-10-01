import re
import subprocess
import logging

# Configure logging for debugging and error tracking
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class StayziaCompiler:
    def __init__(self):
        self.cpp_code = ""
        self.retry_limit = 3  # Number of retries before failing a line

    def compile_to_cpp(self, code):
        try:
            lines = code.split('\n')
            for line in lines:
                self.process_line_with_retry(line.strip())
            self.write_cpp_file()
            self.compile_cpp()
        except Exception as e:
            logging.error(f"Error during compilation: {e}")

    def process_line_with_retry(self, line):
        retries = 0
        while retries < self.retry_limit:
            try:
                logging.info(f"Processing line: {line}")
                self.generate_cpp_line(line)
                return  # Line processed successfully
            except Exception as e:
                retries += 1
                logging.warning(f"Error processing line: {line}. Attempt {retries}/{self.retry_limit}")
                line = self.refurbish_line(line, retries)
        logging.error(f"Failed to process line after {self.retry_limit} attempts: {line}")

    def refurbish_line(self, line, attempt):
        """ Try different fixes based on the attempt number """
        if attempt == 1:
            # Simple fixes, such as trimming white spaces or fixing common syntax issues
            line = line.strip()
        elif attempt == 2:
            # Try adding missing semicolons or braces (if applicable)
            if not line.endswith(';') and 'return' not in line:
                line += ';'
        elif attempt == 3:
            # Last resort, try commenting out the line
            logging.warning(f"Commenting out potentially faulty line: {line}")
            line = f"// {line}"
        return line

    def generate_cpp_line(self, line):
        if line.startswith('@HFGC'):
            self.cpp_code += self.generate_hfgc_code()
        elif line.startswith('@pressurized'):
            self.cpp_code += self.generate_pressurized_code()
        elif 'CACHED' in line:
            self.cpp_code += self.generate_cached_code(line)
        elif 'craft' in line:
            self.cpp_code += self.generate_craft_code(line)
        else:
            raise ValueError(f"Unsupported syntax: {line}")

    def generate_hfgc_code(self):
        return """
        void manage_resources() {
            std::cout << "Managing resources in the VAC Universe..." << std::endl;
        }\n
        """

    def generate_pressurized_code(self):
        return """
        void execute_pressurized_task() {
            std::cout << "Executing task under high pressure in the VAC Universe..." << std::endl;
        }\n
        """

    def generate_cached_code(self, line):
        match = re.match(r"CACHED assign immutable value \[ x: (\d+), y: (\d+) \]", line)
        if match:
            x, y = match.groups()
            return f"""
            void cache_values() {{
                const int x = {x};
                const int y = {y};
                std::cout << "Caching immutable values: " << x << ", " << y << std::endl;
            }}\n
            """
        raise ValueError("Malformed CACHED syntax")

    def generate_craft_code(self, line):
        match = re.match(r"craft (.+?) \[ (.+?) \]", line)
        if match:
            func_name, params = match.groups()
            return f"""
            void {func_name}({params}) {{
                std::cout << "Crafting: " << "{func_name}" << std::endl;
            }}\n
            """
        raise ValueError("Malformed craft syntax")

    def write_cpp_file(self):
        cpp_content = f"""
        #include <iostream>

        {self.cpp_code}

        int main() {{
            manage_resources();
            execute_pressurized_task();
            cache_values();
            return 0;
        }}
        """
        try:
            with open("stayzia_generated.cpp", "w") as f:
                f.write(cpp_content)
            logging.info("C++ file written successfully.")
        except Exception as e:
            logging.error(f"Error writing C++ file: {e}")

    def compile_cpp(self):
        try:
            subprocess.run(["g++", "stayzia_generated.cpp", "-o", "stayzia_binary"], check=True)
            logging.info("Compilation to C++ binary complete.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Compilation failed: {e}")
