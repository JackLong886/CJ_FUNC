from nicegui import ui

with ui.row():
    ui.spinner(size='lg')
    ui.spinner('audio', size='lg', color='green')
    ui.spinner('dots', size='lg', color='red')

ui.chat_message('Hello FastImage!',
                name='FastImg',
                stamp='now',
                avatar='https://robohash.org/ui')
ui.image('https://picsum.photos/id/377/640/360')
