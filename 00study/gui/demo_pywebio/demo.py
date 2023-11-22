"""
输入函数都定义在 pywebio.input 模块中，可以使用 from pywebio.input import * 引入
输出函数都定义在 pywebio.output 模块中，可以使用 from pywebio.output import * 引入
PyWebIO的输入函数是阻塞式的，并且输入表单会在成功提交后消失。在某些时候，你可能想要输入表单一直显示并可以持续性接收用户输入，这时你可以使用 pywebio.pin 模块

PyWebIO 根据是否在输入函数中传入 name 参数来判断输入函数是在 input_group 中还是被单独调用。
所以当你想要单独调用一个输入函数时，请不要设置 name 参数；
而在 input_group 中调用输入函数时，务必提供 name 参数。

输入表单会在成功提交后销毁, 如果你想让表单可以一直显示在页面上并可以持续性接收输入，你可以考虑使用 pin 模块。


PyWebIO把交互分成了输入和输出两部分：
    - 输入函数为阻塞式调用，会在用户浏览器上显示一个表单，在用户提交表单之前输入函数将不会返回；
    - 输出函数将内容实时输出至浏览器

PyWebIO使用scope模型来控制内容输出的位置。scope为输出内容的容器，你可以创建一个scope并将内容输出到其中

在PyWebIO中，有两种方式用来运行PyWebIO应用：
    - 作为脚本运行 (如果你在代码中没有调用 start_server() 或 path_deploy() 函数，那么你就是以脚本模式在运行PyWebIO应用)
    - 和使用 pywebio.start_server() 或 pywebio.platform.path_deploy() 来作为Web服务运行

Server模式下，如果需要在新创建的线程中使用PyWebIO的交互函数，需要手动调用 register_thread(thread) 对新进程进行注册（这样PyWebIO才能知道新创建的线程属于哪个会话）
"""
import asyncio
from datetime import datetime
import threading
import time

from flask import Flask
import pywebio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import pin, pin_wait_change, put_input
from pywebio.platform import run_event_loop
from pywebio.platform.flask import webio_view
from pywebio.session import download, go_app, register_thread
from pywebio.session import run_asyncio_coroutine


async def hello_word():
    put_text('Hello ...')
    await run_asyncio_coroutine(asyncio.sleep(1))  # can't just "await asyncio.sleep(1)"
    put_text('... World!')


app = Flask(__name__)
app.add_url_rule('/hello', 'webio_view', webio_view(hello_word, cdn=False),
    methods=['GET', 'POST', 'OPTIONS'])

# thread to run event loop
threading.Thread(target=run_event_loop, daemon=True).start()
app.run(host='localhost', port=8080)


async def hello_word():
    put_text('Hello ...')
    await asyncio.sleep(1)  # await awaitable objects in asyncio
    put_text('... World!')


async def main():
    await hello_word()  # await coroutine
    put_text('Bye, bye')


start_server(main, auto_open_webbrowser=True, cdn=False)


async def say_hello():
    name = await input("what's your name?")
    put_text('Hello, %s' % name)


start_server(say_hello, auto_open_webbrowser=True, cdn=False)

app = Flask(__name__)


def task_func():
    print("*" * 20)


# `task_func` is PyWebIO task function
app.add_url_rule('/tool', 'webio_view', webio_view(task_func),
    methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

# Permission denied
app.run(host='localhost', port=8080)


def task_1():
    put_text('task_1')
    put_buttons(['Go task 2'], [lambda: go_app('task_2')])


def task_2():
    put_text('task_2')
    put_buttons(['Go task 1'], [lambda: go_app('task_1')])


def index():
    put_link('Go task 1', app='task_1')  # Use `app` parameter to specify the task name
    put_link('Go task 2', app='task_2')


# equal to `start_server({'index': index, 'task_1': task_1, 'task_2': task_2})`
start_server([index, task_1, task_2], cdn=False)
print("*" * 20)

put_input('a', type='number', value=0)
put_input('b', type='number', value=0)

while True:
    changed = pin_wait_change('a', 'b')
    with use_scope('res', clear=True):
        put_code(changed)
        put_text("a + b = %s" % (pin.a + pin.b))

put_input('counter', type='number', value=0)

while True:
    pin.counter = pin.counter + 1  # Equivalent to: pin['counter'] = pin['counter'] + 1
    time.sleep(1)

put_input('pin_name')
put_buttons(['Get Pin Value'], lambda _: put_text(pin.pin_name))

put_row([
    put_input('input'),
    put_select('select', options=['A', 'B', 'C'])
])

with use_scope('search-area'):
    put_input('search', placeholder='Search')

put_input('input', label='This is a input widget')

set_env(title='FJP Awesome PyWebIO!!', output_animation=False)

run_js('console.log(a + b)', a=1, b=2)

put_button('Click to download', lambda: download('hello-world.txt', b'hello world!'))

put_grid([
    [put_text('A'), put_text('B'), put_text('C')],
    [None, span(put_text('D'), col=2, row=1)],
    [put_text('E'), put_text('F'), put_text('G')],
], cell_width='100px', cell_height='100px')

# Two code blocks of equal width, separated by 10 pixels
put_row([put_code('A'), None, put_code('B')])

# The width ratio of the left and right code blocks is 2:3, which is equivalent to size='2fr 10px 3fr'
put_row([put_code('A'), None, put_code('B')], size='40% 10px 60%')

with popup('Popup title') as s:
    put_html('<h3>Popup Content</h3>')
    put_text('html: <br/>')
    put_buttons([('clear()', s)], onclick=clear)

put_text('Also work!', scope=s)

popup('popup title', 'popup text content', size=PopupSize.SMALL)

popup('Popup title', [
    put_html('<h3>Popup Content</h3>'),
    'html: <br/>',
    put_table([['A', 'B'], ['C', 'D']]),
    put_buttons(['close_popup()'], onclick=lambda _: close_popup())
])


def show_msg():
    put_text("You clicked the notification.")


toast('New messages', position='right', color='#2188ff', duration=0, onclick=show_msg)

tpl = '''
<details {{#open}}open{{/open}}>
    <summary>{{title}}</summary>
    {{#contents}}
        {{& pywebio_output_parse}}
    {{/contents}}
</details>
'''

put_widget(tpl, {
    "open": True,
    "title": 'More content',
    "contents": [
        'text',
        put_markdown('~~Strikethrough~~'),
        put_table([
            ['Commodity', 'Price'],
            ['Apple', '5.5'],
            ['Banana', '7'],
        ])
    ]
})

with urllib.request.urlopen('https://fakerapi.it/api/v1/persons?_quantity=30') as f:
    data = json.load(f)['data']

put_datatable(
    data,
    actions=[
        ("Edit Email", lambda row_id: datatable_update('user', input("Email"), row_id, "email")),
        ("Insert a Row", lambda row_id: datatable_insert('user', data[0], row_id)),
        None,  # separator
        ("Delete", lambda row_id: datatable_remove('user', row_id)),
    ],
    onselect=lambda row_id: toast(f'Selected row: {row_id}'),
    instance_id='user'
)

put_scrollable(put_scope('scrollable'), height=200, keep_bottom=True)
put_text("You can click the area to prevent auto scroll.", scope='scrollable')

while 1:
    put_text(time.time(), scope='scrollable')
    time.sleep(0.5)

put_collapse('Collapse title', [
    'text',
    put_markdown('~~Strikethrough~~'),
    put_table([
        ['Commodity', 'Price'],
        ['Apple', '5.5'],
    ])
], open=True)

put_collapse('Large text', 'Awesome PyWebIO! ' * 30)

put_tabs([
    {'title': 'Text', 'content': 'Hello world'},
    {'title': 'Markdown', 'content': put_markdown('~~Strikethrough~~')},
    {'title': 'More content', 'content': [
        put_table([
            ['Commodity', 'Price'],
            ['Apple', '5.5'],
            ['Banana', '7'],
        ]),
        put_link('pywebio', 'https://github.com/wang0618/PyWebIO')
    ]},
])

content = open('/Users/leo.fu1/Desktop/china.png', 'rb').read()
put_file('hello-world.txt', content, 'download me')

img = open('/Users/leo.fu1/Desktop/china.png', 'rb').read()
put_image(img, width='50px')

put_image('https://www.python.org/static/img/python-logo.png')


def row_action(choice, id):
    put_text("You click %s button with id: %s" % (choice, id))


put_buttons(['edit', 'delete'], onclick=partial(row_action, id=1))


def edit():
    put_text("You click edit button")


def delete():
    put_text("You click delete button")


put_buttons(['edit', 'delete'], onclick=[edit, delete])

put_table(
    [
        ['C'],
        [span('E', col=2)],  # 'E' across 2 columns
    ],
    header=[span('A', row=2), 'B'],
)  # 'A' across 2 rows

put_grid(
    [
        [put_text('A'), put_text('B')],
        [span(put_text('C'), col=2)],  # 'A' across 2 columns
    ]
)

# 'Name' cell across 2 rows, 'Address' cell across 2 columns
put_table(
    [
        [span('Name', row=2), span('Address', col=2)],
        ['City', 'Country'],
        ['Wang', 'Beijing', 'China'],
        ['Liu', 'New York', 'America'],
    ]
)

"""
Name	Address
        City	Country
Wang	Beijing	 China
Liu	    New York America
"""

# Use `put_xxx()` in `put_table()`
put_table(
    [
        ['Type', 'Content'],
        ['html', put_html('X<sup>2</sup>')],
        ['text', '<hr/>'],
        ['buttons', put_buttons(['A', 'B'], onclick=...)],
        ['markdown', put_markdown('`Awesome PyWebIO!`')],
        ['file', put_file('hello.text', b'hello world')],
        ['table', put_table([['A', 'B'], ['C', 'D']])],
    ]
)

# Set table header
put_table(
    [
        ['Wang', 'M', 'China'],
        ['Liu', 'W', 'America'],
    ],
    header=['Name', 'Gender', 'Address'],
)

# When ``tdata`` is list of dict
put_table(
    [
        {"Course": "OS", "Score": "80"},
        {"Course": "DB", "Score": "93"},
    ],
    header=["Course", "Score"],
    # or header=[(put_markdown("*Course*"), "Course"), (put_markdown("*Score*"), "Score")],
)

for shape in ('border', 'grow'):
    for color in ('primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'):
        put_text(shape, color)
        put_loading(shape=shape, color=color)

# The loading prompt and the output inside the context will disappear
# automatically when the context block exits.
with put_loading():
    put_text("Start waiting...")
    time.sleep(3)  # Some time-consuming operations
put_text("The answer of the universe is 42")

# using style() to set the size of the loading prompt
put_loading().style('width:4rem; height:4rem')

put_progressbar('bar')
for i in range(1, 11):
    set_progressbar('bar', i / 10)
    time.sleep(0.1)

with use_scope('scope1'):
    put_text('A')
    put_text('B', position=0)  # insert B before A -> B A
    put_text('C', position=-2)  # insert C after B -> B C A
    put_text('D', position=1)  # insert D before C B -> B D C A

country2city = {
    'China': ['Beijing', 'Shanghai', 'Hong Kong'],
    'USA': ['New York', 'Los Angeles', 'San Francisco'],
}
countries = list(country2city.keys())
location = input_group(
    "Select a location",
    [
        select(
            'Country',
            options=countries,
            name='country',
            onchange=lambda c: input_update('city', options=country2city[c]),
        ),
        select('City', options=country2city[countries[0]], name='city'),
    ],
)

# Upload a file and save to server
f = file_upload("Upload a file")
open('asset/' + f['filename'], 'wb').write(f['content'])

imgs = file_upload("Select some pictures:", accept="image/*", multiple=True)
for img in imgs:
    put_image(img['content'])

info = input_group(
    'Add user',
    [
        input('username', type=TEXT, name='username', required=True),
        input('password', type=PASSWORD, name='password', required=True),
        actions(
            'actions',
            [
                {'label': 'Save', 'value': 'save'},
                {'label': 'Save and add next', 'value': 'save_and_continue'},
                {'label': 'Reset', 'type': 'reset', 'color': 'warning'},
                {'label': 'Cancel', 'type': 'cancel', 'color': 'danger'},
            ],
            name='action',
            help_text='actions',
        ),
    ],
)
put_code('info = ' + json.dumps(info, indent=4))


def save_user(param, param1):
    pass


def add_next():
    pass


if info is not None:
    save_user(info['username'], info['password'])
    if info['action'] == 'save_and_continue':
        add_next()

confirm = actions('Confirm to delete file?', ['confirm', 'cancel'], help_text='Unrecoverable after file deletion')


def set_now_ts(set_value):
    set_value(int(time.time()))


ts = input('Timestamp', type=NUMBER, action=('Now', set_now_ts))
from datetime import date, timedelta


def select_date(set_value):
    with popup('Select Date'):
        put_buttons(['Today'], onclick=[lambda: set_value(date.today(), 'Today')])
        put_buttons(['Yesterday'], onclick=[lambda: set_value(date.today() - timedelta(days=1), 'Yesterday')])


d = input('Date', action=('Select', select_date), readonly=True)
put_text(type(d), d)


# Server模式下多线程的使用示例:
def show_time():
    import datetime

    while True:
        with use_scope(name='time', clear=True):
            put_text(datetime.datetime.now())
            time.sleep(1)


def app():
    t = threading.Thread(target=show_time)
    register_thread(t)
    put_markdown('## Clock')
    t.start()  # run `show_time()` in background

    # ❌ this thread will cause `SessionNotFoundException`
    # threading.Thread(target=show_time).start()
    # pywebio.exceptions.SessionNotFoundException: Can't find current session. Maybe session closed or forget to use `register_thread()`.

    put_text('Background task started.')


start_server(app, port=8080, debug=True, cdn=False)


def main():  # PyWebIO application function
    name = pywebio.input.input("what's your name")
    pywebio.output.put_text("hello", name)


pywebio.start_server(main, port=8080, debug=True, cdn=False, remote_access=True)
"""
使用 debug=True 来开启debug模式，这时server会在检测到代码发生更改后进行重启
传入 remote_access=True 开启远程访问
"""

put_text('hello').style('color: red; font-size: 20px')

# in combined output
put_row([put_text('hello').style('color: red'), put_markdown('markdown')]).style('margin-top: 20px')

put_row(
    [
        put_column(
            [
                put_code('A'),
                put_row(
                    [
                        put_code('B1'),
                        None,  # None represents the space between the output
                        put_code('B2'),
                        None,
                        put_code('B3'),
                    ]
                ),
                put_code('C'),
            ]
        ),
        None,  # 空格
        put_code('D'),
        None,
        put_code('E'),
    ]
)

put_table(
    [['Name', 'Hobbies'], ['Tom', put_scope('hobby', content=put_text('Coding'))]]  # hobby is initialized to coding
)

with use_scope('hobby', clear=True):
    put_text('Movie')  # hobby is reset to Movie

# append Music, Drama to hobby
with use_scope('hobby'):
    put_text('Music')
    put_text('Drama')

# insert the Coding into the top of the hobby
put_markdown('**Coding**', scope='hobby', position=0)

"""
┌─ROOT────────────────────┐
│                         │
│ ┌─A───────────────────┐ │
│ │ Text in scope A     │ │
│ │ ┌─B───────────────┐ │ │
│ │ │ Text in scope B │ │ │
│ │ └─────────────────┘ │ │
│ └─────────────────────┘ │
│                         │
│ ┌─C───────────────────┐ │
│ │ Text in scope C     │ │
│ └─────────────────────┘ │
└─────────────────────────┘
"""
with use_scope('A'):
    put_text('Text in scope A')

    with use_scope('B'):
        put_text('Text in scope B')

with use_scope('C'):
    put_text('Text in scope C')


@use_scope('time', clear=True)
def show_time():
    """
    第一次调用 show_time 时，将会创建 time 输出域并在其中输出当前时间，之后每次调用 show_time() ，输出域都会被新的内容覆盖
    """
    put_text(datetime.now())


show_time()

show_time()

with use_scope('scope2'):
    put_text('create scope2')

put_text('text in parent scope of scope2')

with use_scope('scope2', clear=True):  # enter the existing scope and clear the previous content
    put_text('text in scope2')

with use_scope('scope1'):  # 创建并进入scope 'scope1'
    put_text('text1 in scope1')  # 输出内容到 scope1

put_text('text in parent scope of scope1')  # 输出内容到 ROOT scope

with use_scope('scope1'):  # 进入之前创建的scope 'scope1'
    put_text('text2 in scope1')  # 输出内容到 scope1

# open('/Users/leo.fu1/Desktop/china.png', 'rb').read()
put_image(open('/Users/leo.fu1/Desktop/china.png', 'rb').read()).onclick(lambda: toast('You click an image'))

# set onclick in combined output
put_table(
    [
        ['Commodity', 'Price'],
        ['Apple', put_text('5.5').onclick(lambda: toast('You click the text'))],
    ]
)


def btn_click(btn_val):
    put_text("You click %s button" % btn_val)


put_buttons(['A', 'B', 'C'], onclick=btn_click)  # a group of buttons

put_button("Click me", onclick=lambda: toast("Clicked"))  # single button


def edit_row(choice, row=0):
    put_text("You click %s button ar row %s" % (choice, row))


put_table(
    [
        ['Idx', 'Actions'],
        [1, put_buttons(['edit', 'delete'], onclick=partial(edit_row, row=1))],
        [2, put_buttons(['edit', 'delete'], onclick=partial(edit_row, row=2))],
        [3, put_buttons(['edit', 'delete'], onclick=partial(edit_row, row=3))],
    ]
)

with put_collapse('This is title 折叠'):
    for i in range(4):
        put_text(i)

    put_table(
        [
            ['Commodity', 'Price'],
            ['Apple', '5.5'],
            ['Banana', '7'],
        ]
    )

popup(
    'Popup title',
    [
        put_html('<h3>Popup Content</h3>'),
        'plain html: <br/>',  # Equivalent to: put_text('plain html: <br/>')
        put_table([['A', 'B'], ['C', 'D']]),
        put_button('close_popup()', onclick=close_popup),
    ],
)

put_table(
    [
        ['Type', 'Content'],
        ['html', put_html('X<sup>2</sup>')],
        ['text', '<hr/>'],  # equal to ['text', put_text('<hr/>')]
        ['buttons', put_buttons(['A', 'B'], onclick=...)],
        ['markdown', put_markdown('`Awesome PyWebIO!`')],
        ['file', put_file('hello.text', b'hello world')],
        ['table', put_table([['A', 'B'], ['C', 'D']])],
    ]
)

# Text Output
put_text("Hello world!")

# Table Output
put_table(
    [
        ['Commodity', 'Price'],
        ['Apple', '5.5'],
        ['Banana', '7'],
    ]
)

# Image Output
put_image(open('/Users/leo.fu1/Desktop/china.png', 'rb').read())  # local image
put_image('http://example.com/some-image.png')  # internet image

# Markdown Output
put_markdown('~~Strikethrough~~')

# File Output
put_file('hello_word.txt', b'hello word!')

# Show a PopUp
popup('popup title', 'popup text content')

# Show a notification message
toast('New message 🔔')


def check_age(p):  # return None when the check passes, otherwise return the error message
    if p < 10:
        return 'Too young!!'
    if p > 60:
        return 'Too old!!'


def check_form(data):  # return (input name, error msg) when validation fail
    if len(data['name']) > 6:
        return ('name', 'Name too long!')
    if data['age'] <= 0:
        return ('age', 'Age can not be negative!')


data = input_group(
    "Basic info",
    [input('Input your name', name='name'), input('Input your age', name='age', type=NUMBER)],
    validate=check_form,
)

data = input_group(
    "Basic info",
    [input('Input your name', name='name'), input('Input your age', name='age', type=NUMBER, validate=check_age)],
)
put_text(data['name'], data['age'])

code = textarea(
    'Code Edit',
    code={
        'mode': "python",
        'theme': 'darcula',
    },
    value='import something\n# Write your python code',
)

age = input("How old are you?", type=NUMBER, validate=check_age)

input('This is label', type=TEXT, placeholder='This is placeholder', help_text='This is help text', required=True)

age = input("How old are you?", type=NUMBER)

# Password input
password = input("Input password", type=PASSWORD)

# Drop-down selection
gift = select('Which gift you want?', ['keyboard', 'ipad'])

# Checkbox
agree = checkbox("User Term", options=['I agree to terms and conditions'])

# Single choice
answer = radio("Choose one", options=['A', 'B', 'C', 'D'])

# Multi-line text input
text = textarea('Text Area', rows=3, placeholder='Some text')

# File Upload
img = file_upload("Select a image:", accept="image/*")
