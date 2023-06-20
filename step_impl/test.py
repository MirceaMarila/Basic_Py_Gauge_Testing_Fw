from getgauge.python import step


@step("breakpoint")
def put_breakpoint():
    breakpoint()
