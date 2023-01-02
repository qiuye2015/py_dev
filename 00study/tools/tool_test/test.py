import sys


# def exception_hook(exc_type, exc_value, tb):
#     print('Traceback:')
#     filename = tb.tb_frame.f_code.co_filename
#     name = tb.tb_frame.f_code.co_name
#     line_no = tb.tb_lineno
#     print(f"File {filename} line {line_no}, in {name}")
#     # Exception type 和 value
#     print(f"{exc_type.__name__}, Message: {exc_value}")

# Traceback:
# File /Users/leo.fu1/workspace/github/icoding/py_dev/00study/tools/tool_test/test.py line 22, in <module>
# ValueError, Message: Some error message

# def exception_hook(exc_type, exc_value, tb):
#     local_vars = {}
#     while tb:
#         filename = tb.tb_frame.f_code.co_filename
#         name = tb.tb_frame.f_code.co_name
#         line_no = tb.tb_lineno
#         print(f"File {filename} line {line_no}, in {name}")
#         local_vars = tb.tb_frame.f_locals
#         tb = tb.tb_next
#     print(f"Local variables in top frame: {local_vars}")


# File /Users/leo.fu1/workspace/github/icoding/py_dev/00study/tools/tool_test/test.py line 37, in <module>
# File /Users/leo.fu1/workspace/github/icoding/py_dev/00study/tools/tool_test/test.py line 34, in do_stuff
# Local variables in top frame: {}

# sys.excepthook = exception_hook


def do_stuff():
    # 写一段会产生异常的代码
    raise ValueError("Some error message")


# from rich.traceback import install

# install(show_locals=True)
# do_stuff()  # Raises ValueError

# import better_exceptions
# #
# # better_exceptions.MAX_LENGTH = None
# # better_exceptions.SUPPORTS_COLOR = True
# # better_exceptions.hook()

# import pretty_errors
# # 如果你对默认配置满意的话，则无需修改
# pretty_errors.configure(
#    filename_display    = pretty_errors.FILENAME_EXTENDED,
#    line_number_first   = True,
#    display_link        = True,
#    line_color          = pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
#    code_color          = '  ' + pretty_errors.default_config.line_color,
#    truncate_code       = True,
#    display_locals      = True
# )

# import IPython.core.ultratb
# # Also ColorTB, FormattedTB, ListTB, SyntaxTB
# sys.excepthook = IPython.core.ultratb.VerboseTB(color_scheme='Linux')  # Other colors: NoColor, LightBG, Neutral


# import stackprinter
# stackprinter.set_excepthook(style='darkbg2')

# do_stuff()  # Raises ValueError


from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
