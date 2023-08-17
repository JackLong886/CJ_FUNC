from func import *
from datetime import datetime


def run_pansharpen():
    para = PansharpParam()
    with ui.row():
        ui.button('Choose file', on_click=para.select_input_img, icon='folder')
        ui.label().bind_text(para, 'input')

    ui.textarea(label='Input message', placeholder='start typing', on_change=para.parse_input)

    ui.input(label='Output folder', placeholder='D:\龙超俊的文件夹', on_change=para.set_output_dir)

    with ui.row():
        ui.toggle(['FG', 'WG'], value='WG').bind_value(para, 'pan_method')
        ui.checkbox('Build Overview', on_change=para.set_if_build_overview)

    ratio = ui.slider(min=0, max=100, value=50, step=10).bind_value(para, 'ratio')
    ui.label('ratio:').bind_text_from(ratio, 'value')
    winsize = ui.slider(min=0, max=4096, value=1024, step=256).bind_value(para, 'winsize')
    ui.label('winsize:').bind_text_from(winsize, 'value')
    ui.linear_progress().bind_value_from(para, 'program_progress')
    ui.button('Run!', on_click=para.run)


def run_cloud_removal():
    para = CloudRemovalParam()
    ui.icon('cloud_off', color='primary').classes('text-6xl')
    with ui.row():
        # ui.button('Choose file', on_click=para.pick_file, icon='folder')
        ui.input(label='Output folder', placeholder='D:\龙超俊的文件夹').bind_value(para, 'output_dir')
        ui.input(label='work dir', placeholder='workspace').bind_value(para, 'work_dir')
        ui.input(label='resolution', placeholder='2').bind_value(para, 'res')
    with ui.row():
        ui.button('Target Img', on_click=para.select_input_target_img)
        ui.button('Source Img', on_click=para.select_input_source_img)
        ui.button('Valid Shp', on_click=para.select_input_valid_shp)
        ui.button('Cloud Shp', on_click=para.select_input_cloud_shp)

    with ui.row():
        ui.textarea(label='Input target img', placeholder='start typing',
                    on_change=para.parse_input_target_img)
        ui.textarea(label='Input source img', placeholder='start typing',
                    on_change=para.parse_input_source_img)
        ui.textarea(label='Input valid shp', placeholder='start typing',
                    on_change=para.parse_input_valid)
        ui.textarea(label='Input cloud shp', placeholder='start typing',
                    on_change=para.parse_input_cloud)

    with ui.row():
        ui.checkbox('Color Transfer', on_change=para.set_color_trans)
        ui.checkbox('Build Overview', on_change=para.set_if_build_overview)

    ratio = ui.slider(min=0, max=100, value=50, step=5,
                      on_change=lambda x: ui.notify('ratio: {}'.format(x.value))).bind_value(para, 'ratio')
    ui.label('ratio:').bind_text_from(ratio, 'value')

    winsize = ui.slider(min=0, max=4096, value=1024, step=256,
                        on_change=lambda x: ui.notify('winsize: {}'.format(x.value))).bind_value(para, 'win_size')
    ui.label('winsize:').bind_text_from(winsize, 'value')
    ui.linear_progress().bind_value_from(para, 'program_progress')
    with ui.row():
        ui.button('Check!', on_click=para.check)
        ui.button('Run!', on_click=para.run)


def run_mosaic():
    para = MosaicParam()
    with ui.row():
        ui.button('Select Input Image', on_click=para.get_mos_input_list)
        ui.input(label='work dir', placeholder='workspace').bind_value(para, 'work_dir')
        ui.input(label='resolution', placeholder='2').bind_value(para, 'res')
    with ui.row():
        input1 = ui.input(label='mos_union_path', placeholder='union path').bind_value(para, 'mos_union_path')
        input1.style('color: #6E93D6; font-size: 100%; font-weight: 800')
        input2 = ui.input(label='output_region_shp', placeholder='output region').bind_value(para, 'output_region_shp')
        input2.style('color: #6E93D6; font-size: 100%; font-weight: 800')
        input3 = ui.input(label='mos_output_path', placeholder='mos output').bind_value(para, 'mos_output_path')
        input3.style('color: #6E93D6; font-size: 100%; font-weight: 800')

    with ui.row():
        text1 = ui.textarea(label='Input img', placeholder='start typing', on_change=para.parse_input_img)
        text1.style('color: #6E93D6; font-size: 100%; font-weight: 600')
        text2 = ui.textarea(label='Input valid shp', placeholder='start typing', on_change=para.parse_input_valid)
        text2.style('color: #6E93D6; font-size: 100%; font-weight: 600')

    with ui.row():
        ui.checkbox('Color Transfer', on_change=para.set_if_build_overview)
        ui.checkbox('Build Overview', on_change=para.set_if_build_overview)

    ratio = ui.slider(min=0, max=100, value=50, step=5,
                      on_change=lambda x: ui.notify('ratio: {}'.format(x.value))).bind_value(para, 'ratio')
    ui.label('ratio:').bind_text_from(ratio, 'value')

    winsize = ui.slider(min=0, max=4096, value=1024, step=256,
                        on_change=lambda x: ui.notify('winsize: {}'.format(x.value))).bind_value(para, 'win_size')
    ui.label('winsize:').bind_text_from(winsize, 'value')
    ui.linear_progress().bind_value_from(para, 'program_progress')
    ui.button('Run!', on_click=para.run)
    ui.button('Check!', on_click=para.check)


def run_cloud_detect():
    para = CloudDetectParam()
    ui.icon('cloud_queue', color='primary').classes('text-6xl')
    with ui.row():
        ui.input(label='Output folder', placeholder='D:\龙超俊的文件夹').bind_value(para, 'output_dir')
        ui.input(label='work dir', placeholder='workspace').bind_value(para, 'work_dir')
        ui.select(['cpu', 'cuda:0'], value='cuda:0').bind_value(para, 'device')

    with ui.row():
        ui.textarea(label='Input img', placeholder='start typing',
                    on_change=para.parse_input_img)
        ui.button('Select Input Image', on_click=para.select_input_img)

    ui.linear_progress().bind_value_from(para, 'program_progress')
    with ui.row():
        ui.button('Check!', on_click=para.check)
        ui.button('Run!', on_click=para.run)


label = ui.label()
run_cloud_detect()
ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))
ui.run(title='Fast Image')
