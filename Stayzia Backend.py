class StayziaBackend:
    def __init__(self):
        self.compiler = StayziaCompiler()
        self.interpreter = StayziaInterpreter()

    def execute(self, stayzia_code):
        logging.info("Starting Stayzia execution process.")
        self.compiler.compile_to_cpp(stayzia_code)
        # Assuming successful compilation, run the binary
        self.interpreter.run(stayzia_code)
