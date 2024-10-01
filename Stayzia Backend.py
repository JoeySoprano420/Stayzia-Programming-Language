class StayziaBackend:
    def __init__(self):
        self.compiler = StayziaCompiler()
        self.interpreter = StayziaInterpreter()

    def execute_code(self, code, compile_first=False):
        if compile_first:
            self.compiler.compile_to_cpp(code)
        else:
            self.interpreter.run(code)
