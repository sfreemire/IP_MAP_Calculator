#!/usr/bin/env python
import PySimpleGUI as sg

import ipaddress as ip
import os
import sys

'''IP_MAP_Calculator.py: Calculates the results of IP MAP Rule parameters'''

# IP_MAP_ADDRESS_CALCULATOR v0.11.16 - 10/25/2024 - D. Scott Freemire

# Window theme and frame variables
#-------------------------------------#
sg.theme('TanBlue') # Tan is #E5DECF, Blue is #09348A. Text background #fdfdfc works.
# windowfont=('Helvetica', 13) --------------------------------- Commented Out for test
name_tooltip = 'Enter unique rule name'
v6_tooltip = 'Format similar to 2008:8cd:0::/xx'
v6m_tooltip = 'Enter IPv6 mask bits'
v4_tooltip = 'Format similar to 192.168.2.0/24'
v4m_tooltip = 'Enter IPv4 mask bits'
ea_tooltip = 'Max 2 digits'
#psid_tooltip = 'Max 1 digit'
rulestring_tooltip = ('Name|IPv6 Prefix|IPv6 Pfx Len|IPv4 Prefix|'
                      'IPv4 Pfx Len|EA Len|PSID Offset')
v4mask = [n for n in range(16, 33)] # for edit rule Combo
v6mask = [n for n in range(32, 65)] # for edit rule Combo
psidoff = [n for n in range(16)]    # for edit rule Combo
eabits = [n for n in range(33)]     # for edit rule Combo

# Window layout function
#-------------------------------------#
def collapse(title, layout, key):
    return sg.pin(sg.Frame(title, layout,
      border_width=6,
      pad=(0, 0),
      size=(466, 100),
      relief="ridge",
      expand_x=True,
      visible=False,
      key=key))


# Big headings for visibility in text editor "minimap"
'''
██    ██ ██     ██       █████  ██    ██  ██████  ██    ██ ████████ ███████ 
██    ██ ██     ██      ██   ██  ██  ██  ██    ██ ██    ██    ██    ██      
██    ██ ██     ██      ███████   ████   ██    ██ ██    ██    ██    ███████ 
██    ██ ██     ██      ██   ██    ██    ██    ██ ██    ██    ██         ██ 
 ██████  ██     ███████ ██   ██    ██     ██████   ██████     ██    ███████ 
'''

# sg.Push() is like a spring between elements
# sg.Sizer(h_pixels=0, v_pixels=0) is like an adjustable block between elements
# expand_x=True causes container element to expand to widest element contained
# expand_y=True causes container element to expand vertically as needed

# Main Display (top frame) - Calculated Values
#----------------------------------------------#
display_col1 = [
   [sg.Text('Uniq v4 IPs', font=(None, 10, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-IPS_DSPLY-')]
]

display_col2 = [
   [sg.Text('Sharing', font=(None, 10, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-RATIO_DSPLY-')]
]

display_col3 = [
   [sg.Text('Users', font=(None, 10, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-USERS_DSPLY-')]
]

display_col4 = [
   [sg.Text('Ports/User', font=(None, 10, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-PORTS_DSPLY-')]
]

display_col5 = [
   [sg.Text('Excluded Ports', font=(None, 10, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#fdfdfc', border_width=4,
    relief='ridge', key='-EXCL_PORTS_DSPLY-')]
]

# Top frame with results fields
display_layout = [
   [sg.Column(display_col1, element_justification='centered'),
    sg.Text('x', pad=((0, 0), (20, 0))),
    sg.Column(display_col2, element_justification='centered'),
    sg.Text('=', pad=((0, 0), (20, 0))),
    sg.Column(display_col3, element_justification='centered'),
    sg.Text(':', font=('Arial', 16, 'bold'), pad=((0, 0), (20, 0))),
    sg.Column(display_col4, element_justification='centered'),
    sg.Column(display_col5, element_justification='centered')],
   [sg.Text('BMR', font=(None, 10, 'bold')),
    sg.Input('',
   # use_readonly... with disabled creates display field that can be
   # selected and copied with cursor, but not edited (review need for this)
    justification='centered', size=(50, 1), use_readonly_for_disable=True, # --------- size=(60, 1)
    disabled=True, pad=((0, 8), (0, 0)),
    key='-BMR_STRING_DSPLY-'),
    sg.Button('Save', key='-SAVE-')], # ------------------------------- font=('Helvetica', 11),
   [sg.Push(),
    sg.Text('Select and copy, or click Save', font=(None, 10, 'italic'),
    justification='centered', pad=((5, 5), (0, 5))),
    sg.Push()],
]

# Parameter Editing Display (2nd frame)
#---------------------------------------#
# param_edit_col1 = [
editor_layout = [
   [sg.Text('Name:', font=(None, 10, 'bold')),
    sg.Input('', font=(None, 10, 'bold'), size=(20, 1),
    enable_events=True, tooltip=name_tooltip, border_width=2,
    pad=((89, 5), (5, 5)), background_color='#fdfdfc', key='-RULENAME-'),
    sg.Push(),
    sg.Text('', text_color='red', font='None 10 bold', key='-PARAM_MESSAGES-'),
    sg.Push()],
   [sg.Text('IPv6 Prefix/Length:', font=(None, 10, 'bold')),
    sg.Input('', font=(None, 10, 'bold'), size=(20, 1), enable_events=True,
    tooltip=v6_tooltip, border_width=2, background_color='#fdfdfc',
    key='-R6PRE-'),
    sg.Text('/'),
    sg.Combo(v6mask, readonly=True, font=(None, 10, 'bold'),
    enable_events=True, background_color='#fdfdfc', key='-R6LEN-')],
   [sg.Text('IPv4 Prefix/Length:', font=(None, 10, 'bold')),
    sg.Input('', font=(None, 10, 'bold'), size=(20, 1), enable_events=True,
    tooltip=v4_tooltip,  border_width=2, background_color='#fdfdfc',
    key='-R4PRE-'),
    sg.Text('/'),
    sg.Combo(v4mask, readonly=True, font=(None, 10, 'bold'),
    enable_events=True, key='-R4LEN-',)],
   [sg.Text('EA Bits Length', font=(None, 10, 'bold')),
    sg.Sizer(h_pixels=32, v_pixels=0),
    sg.Combo(eabits, readonly=True, font=(None, 10, 'bold'),
    background_color='#fdfdfc', enable_events=True, key='-EABITS-',),
    sg.Sizer(h_pixels=23, v_pixels=0),
    sg.Text('PSID Offset Bits', font=(None, 10, 'bold')),
    sg.Combo(psidoff, readonly=True, font=(None, 10, 'bold'),
    background_color='#fdfdfc', enable_events=True, key='-OFFSET-'),
    sg.Sizer(h_pixels=64),  # ------------------------- sg.Sizer(h_pixels=202, v_pixels=0),
    sg.Button('Enter', key='-ENTER_PARAMS-')], # ----------------- font=('Helvetica', 11),
   [sg.Sizer(h_pixels=0, v_pixels=5)],
   [sg.HorizontalSeparator()],
   [sg.Sizer(h_pixels=0, v_pixels=5)],
   [sg.Text('Rule String:', font=(None, 10, 'italic', 'bold'),
    pad=((5, 5), (5, 0))),
    sg.Input('', font=('Courier', 10, 'bold'), size=(53, 1),  # -------------------- size=(60, 1),
    justification='centered', pad=((5, 5), (5, 0)), enable_events=True,
    background_color='#fdfdfc', tooltip=rulestring_tooltip, key='-STRING_IN-'),
    sg.Button('Enter', pad=((5, 5), (5, 0)), # -------------------- font='Helvetica 11',
    key='-ENTER_STRING-')],
   [sg.Push(),
    sg.Text('Type or paste saved string and click Enter',
    font=(None, 10, 'italic'), justification='centered',
    pad=((5, 5), (0, 5))),
    sg.Push()]
]

# editor_layout = [
#    [sg.Column(param_edit_col1, expand_x=True)],
# ]

###################################################################
#            BEGIN COLLAPSIBLE FRAMES
###################################################################

cont3 = [
    [sg.Multiline(font=('Courier', 10, 'bold'),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True, expand_y=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_1')]
]

cont4 = [
    [sg.Multiline(font=('Courier', 10, 'bold'),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True, expand_y=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_2')]
]

cont5 = [
    [sg.Multiline(font=('Courier', 10, 'bold'),
                  p=0,
                  background_color='#fdfdfc',
                  expand_x=True, expand_y=True,
                  no_scrollbar=True, disabled=True,
                  key='MLINE_BIN_3')]
]

scroll_column_layout = [
    [sg.Text(sg.SYMBOL_RIGHT, enable_events=True, k='OPEN_FRM_3'),
     sg.Text("Dynamic Rule Editor", enable_events=True, k='OPEN_FRM_3_TXT')],
    [collapse('', cont3, 'FRAME_3')],
    [sg.Text(sg.SYMBOL_RIGHT, enable_events=True, k='OPEN_FRM_4'),
     sg.Text("CE Addresses and Ports", enable_events=True, k='OPEN_FRM_4_TXT')],
    [collapse('', cont4, 'FRAME_4')],
    [sg.Text(sg.SYMBOL_RIGHT, enable_events=True, k='OPEN_FRM_5'),
     sg.Text("Saved BMR Strings", enable_events=True, k='OPEN_FRM_5_TXT')],
    [collapse('', cont5, 'FRAME_5')],
    # Block horizontal scrolling
    [sg.Sizer(476, 0)]
]

scroll_column = [
    [sg.Column(scroll_column_layout, scrollable=True, vertical_scroll_only=True,
     expand_x=True, expand_y=True,
     size_subsample_height=1, key='SCRL_COLUMN')]
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
   [sg.Frame('', display_layout, expand_x=True, border_width=6,
      relief='ridge', element_justification='centered', k='DISPLAY_FRM'),
      # Add Sizer to expand window so scrollable column can hold similar width frames
      sg.Sizer(h_pixels=25)],
   [sg.Frame('Enter or Edit BMR Parameters', editor_layout,
      font=(None, 10, 'bold'), title_location=sg.TITLE_LOCATION_TOP,
      expand_x=True, border_width=6, relief='ridge', k='EDIT_FRM'),
      sg.Sizer(h_pixels=25)],
   [scroll_column],
   # [sg.Sizer(h_pixels=466)],
   # [sg.Column([[]], size=(466, 1), background_color='red')],

   # [sg.Column(sections_layout, size=(735, None), expand_y=True,
   #  scrollable=True, vertical_scroll_only = True,
   #  sbar_background_color='#D6CFBF', sbar_arrow_color='#09348A',
   #  sbar_relief='solid')],
   
   [sg.Button('Frame Sizes'),
    sg.Button('Column Size'),
    sg.Button(' Exit ')]
]

#-------------------------------------------------------------------------#
# Create Main Window
#-------------------------------------------------------------------------#
# Window uses last screen location for next start
# Location is set upon Exit or WINDOW_CLOSE... event
# Width 780 allows Final Layout width of 735
window = sg.Window('IP MAP Calculator', layout, # --------------------------font=windowfont,
   enable_close_attempted_event=True,
   location=sg.user_settings_get_entry('-location-', (None, None)),
   # keep_on_top=False, resizable=True, size=(780, 1150), finalize=True) #(755, 1070)
   keep_on_top=False, resizable=True, finalize=True) # size=(780, 1260)

# Prevent horizontal window resizing
#window.set_resizable(False, True) # Not available until PySimpleGUI v5

# Formatting for Rule String field - applied immediately
#--------------------------------------------------------#
window['-BMR_STRING_DSPLY-'].Widget.config(readonlybackground='#fdfdfc',
   borderwidth=3, relief='ridge')
# Enable "Return" key to trigger Enter event in Rule String field
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

def frame_sizes():
    frame1 = window['DISPLAY_FRM'].get_size()
    frame2 = window['EDIT_FRM'].get_size()
    # frame3 = window['FRAME_3'].get_size()
    # frame4 = window['FRAME_4'].get_size()
    # return([frame1, frame2, frame3, frame4])
    return([frame1, frame2])

def column_height(f1, f2):
    if f1 and f2 == True:
        new_height = 250
    elif f1 ^ f2:          # ^ = XOR
        new_height = 150
    else:
        new_height = 45
    return(new_height)

def column_size():
    column_size = window['SCRL_COLUMN'].get_size()
    return(column_size)

def column_change(visible):
   column_size = window['SCRL_COLUMN'].get_size()
   col_v = column_size[1]
   print(f'col_v is {col_v}')
   if visible:
      window['SCRL_COLUMN'].Widget.canvas.configure(height=col_v + 100)
   else:
      window['SCRL_COLUMN'].Widget.canvas.configure(height=col_v - 100)



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
f3_open, f4_open, f5_open = False, False, False

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

   if event.startswith('OPEN_FRM_3'):
      f3_open = not f3_open
      window['OPEN_FRM_3'].update(sg.SYMBOL_DOWN if f3_open else sg.SYMBOL_RIGHT)
      window['FRAME_3'].update(visible=f3_open)
      column_change(f3_open)
      window.refresh()
      window['SCRL_COLUMN'].contents_changed() # For containing columns

   if event.startswith('OPEN_FRM_4'):
      f4_open = not f4_open
      window['OPEN_FRM_4'].update(sg.SYMBOL_DOWN if f4_open else sg.SYMBOL_RIGHT)
      window['FRAME_4'].update(visible=f4_open)
      column_change(f4_open)
      window.refresh()
      window['SCRL_COLUMN'].contents_changed() # For containing columns

   if event.startswith('OPEN_FRM_5'):
      f5_open = not f5_open
      window['OPEN_FRM_5'].update(sg.SYMBOL_DOWN if f5_open else sg.SYMBOL_RIGHT)
      window['FRAME_5'].update(visible=f5_open)
      column_change(f5_open)
      window.refresh()
      window['SCRL_COLUMN'].contents_changed() # For containing columns

   if event == 'Frame Sizes':
      sizes = frame_sizes()
      print(f'Frame 1: {sizes[0]}, Frame 2: {sizes[1]}')
      # print(f'Frame 3: {sizes[2]}, Frame 4: {sizes[3]}')

   if event == 'Column Size':
      c_size = column_size()
      print(f'Column size: {c_size}')

######
######

window.close()