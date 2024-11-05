# LATEST COLLAPSIBLE MAP CALCULATOR BACKUP

#!/usr/bin/env python
import PySimpleGUI as sg

import ipaddress as ip
import os
import sys

'''IP_MAP_Calculator.py: Calculates the results of IP MAP Rule parameters'''

# IP_MAP_ADDRESS_CALCULATOR v0.11.16 - 10/25/2024 - D. Scott Freemire

# Window theme, variables, and functions
#----------------------------------------------------------------------------#
sg.theme('TanBlue') # Tan is #E5DECE, Blue is #063289, Text backgrounds are #FDFDFC
# windowfont=('Helvetica', 10) # = sg.DEFAULT_FONT
name_tooltip = 'Enter unique rule name'
v6_tooltip = 'Format is 2008:8cd:0::/xx'
# v6m_tooltip = 'Enter IPv6 mask bits'
v4_tooltip = 'Format is 192.168.2.0/24'
# v4m_tooltip = 'Enter IPv4 mask bits'
# ea_tooltip = 'Max 2 digits'
#psid_tooltip = 'Max 1 digit'
rulestring_tooltip = ('Name|IPv6 Prefix|IPv6 Pfx Len|IPv4 Prefix|'
                      'IPv4 Pfx Len|EA Len|PSID Offset')
v4mask = [n for n in range(16, 33)] # for rule editor Combo
v6mask = [n for n in range(32, 65)] # for rule editor Combo
psidoff = [n for n in range(16)]    # for rule editor Combo
eabits = [n for n in range(33)]     # for rule editor Combo

# Create collapsible frame.
#------------------------------------------#
def collapse(title, layout, key, height=100, width=450): # -------------------- vertical size?
    return sg.pin(sg.Frame(title, layout,
      border_width=6,
      pad=(0, 0),
      # size=(466, height),
      size=(width, height),
      relief="ridge",
      # expand_x=True,
      visible=False,
      key=key))

'''
██    ██ ██     ██       █████  ██    ██  ██████  ██    ██ ████████ ███████ 
██    ██ ██     ██      ██   ██  ██  ██  ██    ██ ██    ██    ██    ██      
██    ██ ██     ██      ███████   ████   ██    ██ ██    ██    ██    ███████ 
██    ██ ██     ██      ██   ██    ██    ██    ██ ██    ██    ██         ██ 
 ██████  ██     ███████ ██   ██    ██     ██████   ██████     ██    ███████ 
'''

# sg.Push() is like a spring between elements
# sg.Sizer(h_pixels=0, v_pixels=0) is like an adjustable block between elements
# expand_x=True causes element to expand to width of its container
# expand_y=True causes element to expand to height of its container

# Main Results Display (top frame) - Calculated Values
#----------------------------------------------------------------------------#
display_col1 = [
   [sg.Text('Uniq v4 IPs', font=(None, 10, 'bold'), pad=((0, 0),(3, 3)))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-IPS_DSPLY-')]
]

display_col1_b = [
   [sg.Text('Uniq v4 IPs', font=(None, 10, 'bold')),
    sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-IPS_DSPLY-')]
]

display_col2 = [
   [sg.Text('Sharing', font=(None, 10, 'bold'), pad=((2, 0),(3, 3)))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-RATIO_DSPLY-')]
]

display_col2_b = [
   [sg.Text('Sharing', font=(None, 10, 'bold')),
    sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-RATIO_DSPLY-')]
]

display_col3 = [
   [sg.Text('Users', font=(None, 10, 'bold'), pad=((0, 0),(3, 3)))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-USERS_DSPLY-')]
]

display_col3_b = [
   [sg.Text('Users', font=(None, 10, 'bold')),
    sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-USERS_DSPLY-')]
]

display_col4 = [
   [sg.Text('Ports/User', font=(None, 10, 'bold'), pad=((0, 0),(3, 3)))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-PORTS_DSPLY-')]
]

display_col4_b = [
   [sg.Text('Ports/User', font=(None, 10, 'bold')),
    sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-PORTS_DSPLY-')]
]

display_col5 = [
   [sg.Text('Excluded Ports', font=(None, 10, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-EXCL_PORTS_DSPLY-')]
]

display_layout = [
   [sg.Column(display_col1, element_justification='centered', p=0),
    sg.Text('x', pad=((2, 0), (20, 0))),
    sg.Column(display_col2, element_justification='centered', p=0),
    sg.Text('=', pad=((2, 0), (20, 0))),
    sg.Column(display_col3, element_justification='centered', p=0),
    sg.Text(':', font=(None, 10, 'bold'), pad=((2, 0), (20, 0))),
    sg.Column(display_col4, element_justification='centered', p=0),
    # sg.Column(display_col5, element_justification='centered')],
    ],
   # [sg.Text('BMR', font=(None, 10, 'bold')),
    # Addl (widget) formatting at end of layouts
   # [sg.Input('', font=(None, 10, 'bold'), size=(50, 1), disabled=True,
   #  justification='centered', pad=((4, 8), (0, 0)), key='-BMR_STRING_DSPLY-'), # Addl formatting
   #  sg.Button('Save', key='-SAVE-')],
   # [sg.Push(),
   #  sg.Text('Select and copy, or click Save', font=(None, 10, 'italic'),
   #  justification='centered', pad=((5, 5), (0, 5))),
   #  sg.Push()],
   [sg.Text('First User IPv6 PD:', font=(None, 10, 'bold')),
    # Addl (widget) formatting at end of layouts
    sg.Input('', font=(None, 10, 'bold'), size=(28 , 1), disabled=True,
    justification='centered', key='USER_IPV6PD')],
]

# display_layout = [
#    [sg.Text('Uniq v4 IPs', font=(None, 10, 'bold')),
#     sg.Text('', justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-IPS_DSPLY-')],
#    [sg.Text('Sharing', font=(None, 10, 'bold')),
#     sg.Text('', justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-RATIO_DSPLY-')],
#    [sg.Text('Users', font=(None, 10, 'bold')),
#     sg.Text('', justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-USERS_DSPLY-')],
#    [sg.Text('Ports/User', font=(None, 10, 'bold')),
#     sg.Text('', justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-PORTS_DSPLY-')],

#    [sg.Text('First User IPv6 PD:', font=(None, 10, 'bold')),
#     # Addl (widget) formatting at end of layouts
#     sg.Input('', font=(None, 10, 'bold'), size=(28 , 1), disabled=True,
#     justification='centered', key='USER_IPV6PD')],
#    [sg.Text('BMR', font=(None, 10, 'bold')),
#     # Addl (widget) formatting at end of layouts
#     sg.Input('', font=(None, 10, 'bold'), size=(50, 1), disabled=True,
#     justification='centered', pad=((0, 8), (0, 0)), key='-BMR_STRING_DSPLY-'), # Addl formatting
#     # sg.Button('Save', key='-SAVE-')
#    ],
#    # [sg.Push(),
#    [sg.Text('Select and copy, or click Save', font=(None, 10, 'italic'),
#     justification='centered', pad=((5, 5), (0, 5)))],
#     # sg.Push()],
# ]



# BMR Editing Display (2nd frame)
#----------------------------------------------------------------------------#
editor_layout = [
   [sg.Text('Name:', font=(None, 10, 'bold')),
    sg.Input('', font=(None, 10, 'bold'), size=(16, 1),
    enable_events=True, tooltip=name_tooltip, border_width=2,
    pad=((73, 5), (5, 5)), background_color='#fdfdfc', key='-RULENAME-'),
    sg.Push(),
    sg.Text('', text_color='red', font='None 10 bold', key='-PARAM_MESSAGES-'),
    sg.Push()],
   [sg.Text('IPv6 Prefix/Length:', font=(None, 10, 'bold')),
    sg.Input('', font=(None, 10, 'bold'), size=(16, 1), enable_events=True,
    tooltip=v6_tooltip, border_width=2, background_color='#fdfdfc',
    key='-R6PRE-'),
    sg.Text('/'),
    sg.Combo(v6mask, readonly=True, font=(None, 10, 'bold'),
    enable_events=True, background_color='#fdfdfc', key='-R6LEN-')],
   [sg.Text('IPv4 Prefix/Length:', font=(None, 10, 'bold')),
    sg.Input('', font=(None, 10, 'bold'), size=(16, 1), enable_events=True,
    tooltip=v4_tooltip,  border_width=2, background_color='#fdfdfc',
    key='-R4PRE-'),
    sg.Text('/'),
    sg.Combo(v4mask, readonly=True, font=(None, 10, 'bold'),
    enable_events=True, key='-R4LEN-',)],
   [sg.Text('EA Bits Length', font=(None, 10, 'bold')),
    sg.Sizer(h_pixels=23, v_pixels=0),
    sg.Combo(eabits, readonly=True, font=(None, 10, 'bold'),
    background_color='#fdfdfc', enable_events=True, key='-EABITS-',),
    sg.Sizer(h_pixels=26, v_pixels=0),
    sg.Text('PSID Offset', font=(None, 10, 'bold')),
    sg.Combo(psidoff, readonly=True, font=(None, 10, 'bold'),
    background_color='#fdfdfc', enable_events=True, key='-OFFSET-'),
    sg.Sizer(h_pixels=20), # ------------------------ sg.Sizer(h_pixels=202, v_pixels=0),
    sg.Button('Enter', key='-ENTER_PARAMS-')], # ---------------- font=('Helvetica', 11),
   # [sg.Sizer(h_pixels=0, v_pixels=5)],
   # [sg.HorizontalSeparator()],
   # [sg.Sizer(h_pixels=0, v_pixels=5)],
   [sg.Text('Rule String:', font=(None, 10, 'italic', 'bold'),
    pad=((5, 5), (5, 0))),
    sg.Input('', font=('Courier', 10, 'bold'), size=(50, 1),  # ----------- size=(60, 1),
    justification='centered', pad=((5, 5), (5, 0)), enable_events=True,
    background_color='#fdfdfc', tooltip=rulestring_tooltip, key='-STRING_IN-'),
    # sg.Button('Enter', pad=((5, 5), (5, 0)), # --------------------- font='Helvetica 11',
    # key='-ENTER_STRING-')],
   ],
   [sg.Push(),
    sg.Text('Type or paste saved string and click Enter',
    font=(None, 10, 'italic'), justification='centered',
    pad=((5, 5), (0, 5))),
    sg.Push()]
]

# Collapsible Frames in Scrollable Column
#----------------------------------------------------------------------------#

# Dynamic Rule Editor
content_3 = [
    [sg.Multiline(font=('Courier', 10),
                  size=(None, 13),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_1')],
    [sg.Sizer(2, 0),
     sg.Text('IPv6 Prefix Length:', font=('None', 10, 'bold'),
     pad=((0, 1), (5, 0))),
     sg.Slider(range=(32, 64), default_value=32, orientation='h',
     disable_number_display=False, enable_events=True,
     size=(16, 8), trough_color='white', font=('None', 10, 'bold'),
     text_color=None, disabled=True, key='-V6PFX_LEN_SLDR-'),
     # sg.Push(),
     sg.Sizer(8, 0),
     sg.VerticalSeparator(),
     sg.Sizer(8, 0),
     # sg.Push(),
     sg.Text('EA Length:', font=('None', 10, 'bold'),
       pad=((0, 14), (5, 0))),
     # sg.Sizer(h_pixels=5, v_pixels=0),
     sg.Slider(range=(0, 32), default_value=32, orientation='h',
     disable_number_display=False, enable_events=True,
     size=(19, 8), trough_color='white', font=('None', 10, 'bold'),
     text_color=None, disabled=True, key='-EA_LEN_SLDR-'),
     # sg.Sizer(40, 0),
    ],
    [
     sg.Sizer(2, 0),
     sg.Text('IPv4 Prefix Length:', font=(None, 10, 'bold'),
     pad=((0, 1), (5, 0))),
     sg.Slider(range=(16, 32), default_value=16, orientation='h',
     disable_number_display=False, enable_events=True,
     size=(16, 8), trough_color='white', font=(None, 10, 'bold'),
     disabled=True, text_color=None,
     key='-V4PFX_LEN_SLDR-'),
     # sg.Push(),
     sg.Sizer(8, 0),
     sg.VerticalSeparator(),
     sg.Sizer(8, 0),
     # sg.Push(),
     sg.Text('PSID Offset:', font=(None, 10, 'bold'),
     pad=((0, 5), (0, 5))),
     sg.Slider(range=(0, 15), default_value=0, orientation='h',
     disable_number_display=False, enable_events=True,
     size=(19, 8), trough_color='white', font=(None, 10, 'bold'),
     pad=((5, 5), (0, 10)), disabled=True, key='-PSID_OFST_SLDR-'),
     # sg.Push()
    ],
    [sg.Sizer(0, 10)]
]

content_3b = [
    [sg.Multiline(font=('Courier', 10),
                  size=(None, 13),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_1B')
    ],
    [sg.Text('Source Port Index:', pad=((4, 0), (4, 4)),
     font=('None', 10, 'bold')),
     sg.Text('', font=(None, 10, 'bold'), pad=((0, 0), (4, 4)),
     justification='centered',
     size=(16, 1), background_color='#fdfdfc', border_width=4,
     relief='ridge', key='-SP_INDEX-'),
     sg.Text(f'=  Port:', pad=((6, 0), (4, 4)), font=(None, 10, 'bold')),
     sg.Text('', font=(None, 10, 'bold'), pad=((0, 0), (4, 4)),
     justification='centered',
     size=(7, 1), background_color='#fdfdfc', border_width=4,
     relief='ridge', key='-SP_INT-'),
    ],
    [sg.Text('Index Chooser:', font=(None, 10, 'bold')),
     sg.Button(' <<', key='-P_IDX_FIRST-'),
     sg.Button(' + 1', key='-P_IDX_UP_1-'),
     sg.Button(' + 10', key='-P_IDX_UP_10-'),
     sg.Button(' + 100', key='-P_IDX_UP_100-'),
     sg.Button(' >>', key='-P_IDX_LAST-'),
     sg.Push()
    ],
]

# CE Addresses and Ports
content_4 = [
   [sg.Push(),
    sg.Text('CE MAP-T IPv6 Address:', font=(None, 10, 'bold'),
    pad=((0, 0), (5, 5))),
    sg.Input('', size=(28, 1), font=(None, 10, 'bold'),
    pad=((5, 0), (5, 5)), justification='centered',
    use_readonly_for_disable=True, disabled=True, key='CE_MAPT_V6IP',
    disabled_readonly_background_color='#fdfdfc'),
    #sg.Push(),
    # sg.Text('User PD', font=(None, 10, 'bold'), pad=((5, 0), (5, 5))),
    # sg.Input('', size=(24, 1), pad=((4, 5), (5, 5)),
    # font=(None, 10, 'bold'), justification='centered',
    # use_readonly_for_disable=True, disabled=True, key='-USER_PD-',
    # disabled_readonly_background_color='#fdfdfc'),
    sg.Sizer(20),
    sg.Text('CE IPv4 Address', font=(None, 10, 'bold'), pad=((0, 0), (5, 5))),
    sg.Input('', size=(14, 1), font=(None, 10, 'bold'),
    pad=((5, 0), (5, 5)), justification='centered',
    use_readonly_for_disable=True, disabled=True, key='-USER_IP4-',
    disabled_readonly_background_color='#fdfdfc'),
    sg.Sizer(20),
    sg.Text('Current Port', font=(None, 10, 'bold'), pad=((4, 0), (5, 5))),
    sg.Input('', size=((7), 1), font=(None, 10, 'bold'),
    justification='centered', use_readonly_for_disable=True,
    disabled=True, key='-USER_PORT-',
    disabled_readonly_background_color='#fdfdfc'),
    sg.Push()],
   [sg.Multiline(font=('Courier', 10, 'bold'),
                  size=(None, 10),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_2')]
]

# Saved BMR Strings
content_5 = [
    [sg.Multiline(font=('Courier', 10, 'bold'),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True, expand_y=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_3')]
]

# Scrollable column containing collapsible frames
scroll_column_layout = [
    [sg.Text(sg.SYMBOL_RIGHT, enable_events=True, k='OPEN_FRM_3'),
     sg.Text("Dynamic Rule Editor", enable_events=True,
     font=(None, 10, 'bold'), k='OPEN_FRM_3_TXT')],

    [collapse('', content_3, 'FRAME_3', 215, 480), #], # 10pt font = 13px
     collapse('', content_3b, 'FRAME_3B', 215, 420)],
    # [sg.Sizer(0, 4)],
    # [sg.Text(sg.SYMBOL_RIGHT, enable_events=True, k='OPEN_FRM_4'),
    #  sg.Text("CE Addresses and Ports", enable_events=True,
    #  font=(None, 10, 'bold'), k='OPEN_FRM_4_TXT')],
    # [collapse('', content_4, 'FRAME_4', 250)],
    # [sg.Sizer(0, 4)],
    # [sg.Text(sg.SYMBOL_RIGHT, enable_events=True, k='OPEN_FRM_5'),
    #  sg.Text("Saved BMR Strings", enable_events=True,
    #  font=(None, 10, 'bold'), k='OPEN_FRM_5_TXT')],
    # [collapse('', content_5, 'FRAME_5')],
    # [sg.Sizer(0, 4)],
    # # Set width of scroll column. Prevent horizontal scrolling when all frames collapsed.
    # [sg.Sizer(942, 0)] # = collapse() width + 12
]

scroll_column = [
    [sg.Column(scroll_column_layout, scrollable=True, vertical_scroll_only=True,
     expand_x=True, expand_y=True, pad=(4, 4),
     # Set initial height to 100% of contents (no scrolling required)
     size_subsample_height=1, key='SCRL_COLUMN')]
   # From original layout:
   #    sbar_background_color='#D6CFBF', sbar_arrow_color='#09348A',
   #    sbar_relief='solid')],
]


######
######

# All Sections
#-------------------------------------#
# sections_layout = [
#    [sg.Frame('', display_layout, expand_x=True, border_width=6,
#       relief='ridge', element_justification='centered')],
#    [sg.Frame('Enter or Edit BMR Parameters', editor_layout,
#     font=(None, 10, 'bold'), title_location=sg.TITLE_LOCATION_TOP,
#     expand_x=True, border_width=6, relief='ridge')],

   # [sg.Frame('', bin_display_layout, expand_x=True, border_width=6,
   #  relief='ridge')],
   # [sg.Frame('', button_layout, expand_x=True, border_width=6,
   #  relief='ridge')],
   # [sg.Frame('Saved Rule Strings', saved_section_layout, expand_x=True,
   #  font=('Helvetica', 13, 'bold'), title_location=sg.TITLE_LOCATION_TOP,
   #  border_width=6, relief='ridge')]
# ]


# Final Layout
#-----------------------------------------#
layout = [
   [sg.Frame('', editor_layout,),
    sg.Frame('', display_layout, element_justification='centered')],

   # sg.Frame('', display_layout, size=(930, 124), expand_x=True, border_width=6, # height 930
   #    relief='ridge', element_justification='centered', k='DISPLAY_FRM'),
   #    # Add Sizer to expand window so scrollable column can hold similar width frames
   #    sg.Sizer(h_pixels=25)],
   #    # sg.Sizer(h_pixels=55)],
   # [sg.Frame('Enter or Edit BMR Parameters', editor_layout,
   #    font=(None, 10, 'bold'), title_location=sg.TITLE_LOCATION_TOP,
   #    expand_x=True, border_width=6, relief='ridge', k='EDIT_FRM'),
   #    sg.Sizer(h_pixels=25)],
   [scroll_column],
   [sg.Button('Frame Sizes'),
    sg.Button('Column Size'),
    sg.Button(' Exit ')],
]

#-------------------------------------------------------------------------#
# Create Main Window
#-------------------------------------------------------------------------#
# Window uses last screen location when app is started.
# Location is saved when window is closed.
window = sg.Window('IP MAP Calculator', layout, # -----------------------font=windowfont,
   enable_close_attempted_event=True,
   location=sg.user_settings_get_entry('-location-', (None, None)),
   keep_on_top=False, resizable=True, finalize=True) # size=(780, 1260)

# Only vertical window resizing is needed. To prevent horizontal window resizing
# use window.set_resizable(False, True) # This is not available until PySimpleGUI v5

# Additional formats and functions for fields
#--------------------------------------------------------#
# Background and border formatting for disabled Input elements
# window['-BMR_STRING_DSPLY-'].Widget.config(readonlybackground='#fdfdfc',
   # borderwidth=3, relief='ridge')
window['USER_IPV6PD'].Widget.config(readonlybackground='#fdfdfc',
   borderwidth=3, relief='ridge')
# Enable Enter key to trigger event in Rule String field
window['-STRING_IN-'].bind('<Return>', '_Enter')

'''
██████  ██    ██ ██      ███████      ██████  █████  ██       ██████ 
██   ██ ██    ██ ██      ██          ██      ██   ██ ██      ██      
██████  ██    ██ ██      █████       ██      ███████ ██      ██      
██   ██ ██    ██ ██      ██          ██      ██   ██ ██      ██      
██   ██  ██████  ███████ ███████      ██████ ██   ██ ███████  ██████ 
'''


######
######

'''
██████  ██ ███████ ██████  ██       █████  ██    ██ ███████ 
██   ██ ██ ██      ██   ██ ██      ██   ██  ██  ██  ██      
██   ██ ██ ███████ ██████  ██      ███████   ████   ███████ 
██   ██ ██      ██ ██      ██      ██   ██    ██         ██ 
██████  ██ ███████ ██      ███████ ██   ██    ██    ███████ 
'''

######
######

'''
 ██████ ██       █████  ███████ ███████ ███████ ███████         ██ 
██      ██      ██   ██ ██      ██      ██      ██             ██  
██      ██      ███████ ███████ ███████ █████   ███████       ██   
██      ██      ██   ██      ██      ██ ██           ██      ██    
 ██████ ███████ ██   ██ ███████ ███████ ███████ ███████     ██     



███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████ 
██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██      
█████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████ 
██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ 
██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████ 
'''     

#----------------------------------------------------------------------------#
#    Classes & Functions
#----------------------------------------------------------------------------#

# ----------------------------------FOR TESTING---------
def frame_sizes():
    frame1 = window['DISPLAY_FRM'].get_size()
    frame2 = window['EDIT_FRM'].get_size()
    frame3 = window['FRAME_3'].get_size()
    frame4 = window['FRAME_4'].get_size()
    frame5 = window['FRAME_5'].get_size()
    fl = [frame1, frame2, frame3, frame4, frame5]
    cnt = 1
    for x in fl:
      print(f'Frame{cnt} size is {x}')
      cnt += 1
    # return([frame1, frame2])

def column_size():
    column_size = window['SCRL_COLUMN'].get_size()
    return(column_size)
# ----------------------------------END TESTING---------

# Resize column when frames are opened or closed
def column_change(visible, size):
   column_size = window['SCRL_COLUMN'].get_size()
   col_v = column_size[1]
   print(f'col_v is {col_v}')
   if visible:
      window['SCRL_COLUMN'].Widget.canvas.configure(height=col_v + size)
   else:
      window['SCRL_COLUMN'].Widget.canvas.configure(height=col_v - size)

def print_attributes(obj):
    # for attr, value in obj.__dict__.items():
    #     print(f"{attr}: {value}")
    for x in obj.__dict__.items():
      print(x)

######
######

'''
███████ ██    ██ ███████ ███    ██ ████████     ██       ██████   ██████  ██████  
██      ██    ██ ██      ████   ██    ██        ██      ██    ██ ██    ██ ██   ██ 
█████   ██    ██ █████   ██ ██  ██    ██        ██      ██    ██ ██    ██ ██████  
██       ██  ██  ██      ██  ██ ██    ██        ██      ██    ██ ██    ██ ██      
███████   ████   ███████ ██   ████    ██        ███████  ██████   ██████  ██      
'''

#-------------------------------------------------------------------------#
# Resources for main event loop
#-------------------------------------------------------------------------#

window['MLINE_BIN_1'].update("\n   DOMAIN Rule IPv6: 2001:0db8:0000:0000::/46\n")
window['MLINE_BIN_1'].update(" First User IPv6 PD: 2001:0db8:0000:0000::/60\n", append=True)
window['MLINE_BIN_1'].update("\n 0010000000000001:0000110110111000:0000000000000000:0000000000000000::/46\n", append=True)

window['MLINE_BIN_1B'].update(" The PORT is PSID-Offset/PSID/Right-Padding:\n")
window['MLINE_BIN_1B'].update("                 000001-000000-0000 = Port 1024\n", append=True)


# Display frame fields
#----------------------------------#
dframe_ls = ['-BMR_STRING_DSPLY-', '-USERS_DSPLY-',
             '-PORTS_DSPLY-', '-EXCL_PORTS_DSPLY-',
             '-IPS_DSPLY-', '-RATIO_DSPLY-']   # Display Frame fields

# Parameter Editor frame fields
#----------------------------------#
pframe_ls = ['-RULENAME-', '-R6PRE-', '-R6LEN-', '-R4PRE-', '-R4LEN-',
   '-EABITS-', '-OFFSET-']
#stringin = ['-STRING_IN-']  # Rule String field
#bframe_ls = ['-USER_PD-', '-USER_IP4-', '-V6PFX_LEN_SLDR-', '-EA_LEN_SLDR-',
#   '-V4PFX_LEN_SLDR-', '-PSID_OFST_SLDR-', '-V4HOST_SLIDER-',
#   '-PORT_INDEX-', 'MLINE_BIN_1']       # Binary Editor fields
#sframe_ls = ['MLINE_SAVED']                # Don't clear Save frame

# Event Loop Variables
#----------------------------------#
chars = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789().'
v6chars = '0123456789abcdefABCDEF:'
v4chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
examples = None
userpds = None
savctr = False
portidxadd = 0 # used with 'Source Port Index n = Port' section
last_params = None
f3_open, f3b_open, f4_open, f5_open = False, False, False, False

#-------------------------------------------------------------------------#
# Main Event Loop - runs once for each 'event'
#-------------------------------------------------------------------------#
cntr = 1  # Event counter
while True:
   event, values = window.read()    # type: (str, dict)
   print(f'\n#--------- Event {str(cntr)} ----------#')
#   print(event, values)
   print(event)
   cntr += 1
   if event in (' Exit ', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
      # Save screen location when closing window
      sg.user_settings_set_entry('-location-', window.current_location())
      break

   # Dynamic Rule Editor
   if event.startswith('OPEN_FRM_3'):
      f3_open = not f3_open
      f3b_open = not f3b_open
      window['OPEN_FRM_3'].update(sg.SYMBOL_DOWN if f3_open else sg.SYMBOL_RIGHT)
      window['FRAME_3'].update(visible=f3_open)
      window['FRAME_3B'].update(visible=f3b_open)
      # Resize column by frame height. Equals height in frame collapse() call.
      column_change(f3_open, 214) # Use actual frame height - 1
      window.refresh()
      window['SCRL_COLUMN'].contents_changed()

   # CE Addreses and Ports
   if event.startswith('OPEN_FRM_4'):
      f4_open = not f4_open
      window['OPEN_FRM_4'].update(sg.SYMBOL_DOWN if f4_open else sg.SYMBOL_RIGHT)
      window['FRAME_4'].update(visible=f4_open)
      column_change(f4_open, 249) # Use actual frame height - 1
      window.refresh()
      window['SCRL_COLUMN'].contents_changed()

   # Saved BMR Strings
   if event.startswith('OPEN_FRM_5'):
      f5_open = not f5_open
      window['OPEN_FRM_5'].update(sg.SYMBOL_DOWN if f5_open else sg.SYMBOL_RIGHT)
      window['FRAME_5'].update(visible=f5_open)
      column_change(f5_open, 99) # Use actual frame height - 1
      window.refresh()
      window['SCRL_COLUMN'].contents_changed()

   # For testing ----------------------------
   if event == 'Frame Sizes':
      sizes = frame_sizes()
      # print(f'Frame 1: {sizes[0]}, Frame 2: {sizes[1]}')
      # print(f'Frame 3: {sizes[2]}, Frame 4: {sizes[3]}')

   if event == 'Column Size':
      c_size = column_size()
      print(f'Column size: {c_size}')
   # End testing ----------------------------

######
######

   # print('\n ---- VALUES KEYS ----')
   # for x in values.keys():
   #    print(x)

   # # This prints all variables:
   # #----------------------------------------#
   # print(dir())

   # el = window.element_list()
   # for x in el:
   #    print_attributes(x)


   # frames = [str(x) for x in el if "Frame" in str(x)]
   # for line in frames:
   #    print(f'type line {line} is {type(line)}')

# Show all elements:
#   element_list = window.element_list()
#   print(element_list)

   # lmnts = window.element_list()
   # lmnt_keys = []
   # for lmnt in lmnts:
   #    if lmnt.key:
   #       lmnt_keys.append(f'{lmnt} key: {lmnt.key}')
   # print(lmnt_keys)
   
   # layouts = [x.Layout for x in lmnts]
   # print(layouts)


   # for x in lmnts:
      # print(dir(x))
   # print(lmnts[0].Layout)

window.close()