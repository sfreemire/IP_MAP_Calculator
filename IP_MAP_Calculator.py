#!/usr/bin/env python3
import PySimpleGUI as sg
import ipaddress as ip
import os
import sys

'''IP_MAP_Calculator.py: Calculates the results of IP MAP Rule parameters'''

# IP_MAP_ADDRESS_CALCULATOR v0.12.00 - 11/13/2024 - D. Scott Freemire

# Window theme and frame variables
#-------------------------------------#
sg.theme('TanBlue') # Tan is #E5DECF, Blue is #09348A
windowfont=('Helvetica', 13)
name_tooltip = 'Enter unique rule name'
v6_tooltip = 'Format similar to 2008:8cd:0::/xx'
v6m_tooltip = 'Enter IPv6 mask bits'
v4_tooltip = 'Format similar to 192.168.2.0/24'
v4m_tooltip = 'Enter IPv4 mask bits'
ea_tooltip = 'Max 2 digits'
#psid_tooltip = 'Max 1 digit'
rulestring_tooltip = ('Name|IPv6 Prefix|IPv6 Pfx Len|IPv4 Prefix|'
                      'IPv4 Pfx Len|EA Len|PSID Offset')
fmr_tooltip = 'Create FMR option string (forwarding)'
v4mask = [n for n in range(16, 33)] # for edit rule Combo
v6mask = [n for n in range(32, 65)] # for edit rule Combo
psidoff = [n for n in range(16)]    # for edit rule Combo
eabits = [n for n in range(33)]     # for edit rule Combo

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
# expand_x=True causes an element to expand to the width of its container
# expand_y=True causes element to expand to the height of its container

# # Main Display (top frame) - Calculated Values
# #----------------------------------------------#
# display_col1 = [
#    [sg.Text('Uniq v4 IPs', font=('Arial', 14, 'bold'))],
#    [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-IPS_DSPLY-')]
# ]

# display_col2 = [
#    [sg.Text('Sharing', font=('Arial', 14, 'bold'))],
#    [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-RATIO_DSPLY-')]
# ]

# display_col3 = [
#    [sg.Text('Users', font=('Arial', 14, 'bold'))],
#    [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-USERS_DSPLY-')]
# ]

# display_col4 = [
#    [sg.Text('Ports/User', font=('Arial', 14, 'bold'))],
#    [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-PORTS_DSPLY-')]
# ]

# display_col5 = [
#    [sg.Text('Excluded Ports', font=('Arial', 14, 'bold'))],
#    [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
#     size=(7, 1), background_color='#fdfdfc', border_width=4,
#     relief='ridge', key='-EXCL_PORTS_DSPLY-')]
# ]

# Display Layouts
#----------------------------------------------#
# Main Results Display Elements
display_col1 = [
   [sg.Text('Uniq v4 IPs', font=(None, 11, 'bold'))], # font=('Arial', 14, 'bold')
   [sg.Text('', justification='centered', # ............font=('Arial', 16, 'bold')
    size=(7, 1), background_color='#f5f2eb', border_width=2,
    relief='sunken', key='-IPS_DSPLY-')]
]

display_col2 = [
   [sg.Text('Sharing', font=(None, 11, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#f5f2eb', border_width=2,
    relief='sunken', key='-RATIO_DSPLY-')]
]

display_col3 = [
   [sg.Text('Users', font=(None, 11, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#f5f2eb', border_width=2,
    relief='sunken', key='-USERS_DSPLY-')]
]

display_col4 = [
   [sg.Text('Ports/User', font=(None, 11, 'bold'), pad=((0, 4), (4, 4)))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#f5f2eb', border_width=2,
    relief='sunken', key='-PORTS_DSPLY-')]
]

display_col5 = [
   [sg.Text('Excluded Ports', font=(None, 11, 'bold'))],
   [sg.Text('', justification='centered',
    size=(7, 1), background_color='#f5f2eb', border_width=2,
    relief='sunken', key='-EXCL_PORTS_DSPLY-')]
]

# Main Results Display Frame
display_layout = [
   [sg.Column(display_col1, element_justification='centered',
      pad=0),
    sg.Text('x', font=(None, 12, 'bold'), pad=((0, 5), (20, 0))),
    sg.Column(display_col2, element_justification='centered'),
    sg.Text('=', font=(None, 12, 'bold'), pad=((0, 0), (20, 0))),
    sg.Column(display_col3, element_justification='centered',
      pad=((4, 5), (4, 4))),
    sg.Text(':', font=('Arial', 16, 'bold'), pad=((0, 0), (20, 0))),
    sg.Column(display_col4, element_justification='centered',
      pad=((0, 9), (2, 4))),
    sg.Column(display_col5, element_justification='centered')],
   [sg.Sizer(0, 6)],
]

# BMR Parameter Entry Frame
editor_layout = [
   [sg.Sizer(h_pixels=40),
    sg.Text('Name (optional)', font=(None, 10), pad=(4, 0))],
   [sg.Sizer(h_pixels=40),
    sg.Input('', size=(25, 1), font=('Courier', 12),
      justification='centered', background_color='#fdfdfc', pad=(4, 0),
      enable_events=True, tooltip=name_tooltip, key="-RULENAME-"),
    sg.Push(),
    sg.Text('', text_color='red', font='None 12 bold', key='-PARAM_MESSAGES-'),
    sg.Push()],
   [sg.Sizer(h_pixels=40),
    sg.Text('Rule IPv6 Prefix / Length', font=(None, 10), pad=(4, 0)),
    sg.Sizer(h_pixels=103),
    sg.Text('Rule IPv4 Prefix / Length', font=(None, 10), pad=(4, 0)),
    sg.Sizer(h_pixels=67),
    sg.Text('EA Bits', font=(None, 10), pad=(4, 0)),
    sg.Text('PSID Offset', font=(None, 10), pad=(3, 0))],
   [sg.Sizer(h_pixels=40),
    sg.Input('', size=(25, 1), font=('Courier', 12),
      justification='centered', background_color='#fdfdfc',
      enable_events=True, pad=((4, 0), (3, 0)), tooltip=v6_tooltip,
      key='-R6PRE-'),
    sg.Text('/', font=(None, 12, 'bold'), pad=((0, 0), (0, 2))),
    sg.Combo(v6mask, readonly=True, font=('Helvetica', 11),
    enable_events=True, background_color='#fdfdfc', 
    size=(2, 1), pad=((0, 4), (2, 0)), key='-R6LEN-'),
    sg.Sizer(h_pixels=4),
    sg.Input('', size=(20, 1), font=('Courier', 12),
      justification='centered', background_color='#fdfdfc', pad=((4, 0), (2, 0)),
      enable_events=True, tooltip=v4_tooltip, key='-R4PRE-'),
    sg.Text('/', font=(None, 12, 'bold'), pad=((0, 0), (0, 2))),
    sg.Combo(v4mask, readonly=True, font=('Helvetica', 11),
    enable_events=True, background_color='#fdfdfc', 
    size=(2, 1), pad=((0, 7), (2, 0)), key='-R4LEN-'),
    sg.Combo(eabits, readonly=True, font=('Helvetica', 11),
    enable_events=True, background_color='#fdfdfc', 
    size=(2, 1), pad=((6, 2), (2, 0)), key='-EABITS-'),
    sg.Sizer(h_pixels=4),
    sg.Combo(psidoff, readonly=True, font=('Helvetica', 11),
    enable_events=True, background_color='#fdfdfc', 
    size=(2, 1), pad=((6, 2), (2, 0)), key='-OFFSET-')],
   [sg.Sizer(v_pixels=4)],
   [sg.Sizer(h_pixels=40),
    sg.Text('BMR String (optional)', font=(None, 10), pad=(4, 0))],
   [sg.Sizer(h_pixels=40),
    sg.Input('',
      size=(65, 1), font=('Courier', 12), justification='centered',
      background_color='#fdfdfc', pad=(4, 0), tooltip=rulestring_tooltip,
      enable_events=True, key='-STRING_IN-'),
      # Move focus out of input fields so "focus_in" works for all of them on app start
      sg.Button('Enter', font='None 8 bold', key="-ENTER_PARAMS-"),
      sg.Button('Save', font='None 8 bold', pad=0, focus=True, key="SAVE")], 
   # [sg.Sizer(v_pixels=8)],

   [sg.Sizer(h_pixels=40),
    sg.Text('IPv6 Prefix Length:', font=(None, 10),
      background_color="#e5dfcf", pad=((6, 0), (14, 0))),
    sg.Slider(range=(32, 64), default_value=32, orientation='h',
      disable_number_display=False, enable_events=True,
      size=(22, 9), trough_color='white', font=(None, 10),
      text_color=None, background_color="#e5dfcf", disabled=True,
      border_width=2, pad=((0, 4), (0, 0)), key='-V6PFX_LEN_SLDR-'),
    sg.Push(background_color="#e5dfcf"),
    sg.Text('EA Length:', font=(None, 10), background_color="#e5dfcf",
      pad=((0, 0), (14, 0))),
    sg.Slider(range=(0, 32), default_value=0, orientation='h', # Per RFC 7598 (dhcp) 0-48 is valid.
      disable_number_display=False, enable_events=True,
      size=(22, 9), trough_color='white', font=(None, 10),
      text_color=None, disabled=True, background_color="#e5dfcf",
      border_width=2, pad=((0, 4), (0, 0)), key='-EA_LEN_SLDR-'),
    sg.Sizer(h_pixels=150)
   ],
   [sg.Sizer(h_pixels=40),
    sg.Text('IPv4 Prefix Length:', font=(None, 10),
      background_color="#e5dfcf", pad=((6, 0), (10, 0))),
    sg.Slider(range=(16, 32), default_value=16, orientation='h',
      disable_number_display=False, enable_events=True,
      size=(22, 9), trough_color='white', font=(None, 10),
      text_color=None, background_color="#e5dfcf", disabled=True,
      border_width=2, pad=((0, 4), (0, 4)), key='-V4PFX_LEN_SLDR-'),
    sg.Push(background_color="#e5dfcf"),
    sg.Text('PSID Offset:', font=(None, 10),
      background_color="#e5dfcf", pad=((0, 0), (10, 0))),
    sg.Slider(range=(0, 15), default_value=0, orientation='h',
      disable_number_display=False, enable_events=True,
      size=(22, 9), trough_color='white', font=(None, 10),
      text_color=None, disabled=True, background_color="#e5dfcf",
      border_width=2, pad=((0, 4), (0, 4)), key='-PSID_OFST_SLDR-'),
    sg.Sizer(h_pixels=150)
   ],
   [sg.Sizer(v_pixels=6)]

]

bmr_pd_layout = [
   [sg.Multiline("BMR and User PD prefixes", size=(83, 7),
      pad=((4, 4), (4, 0)), font=('Courier', 12, 'bold'), background_color='#f1eee7',
      expand_x=True, disabled=True, border_width=2, # horizontal_scroll = True,
      no_scrollbar=True, key='MLINE_BINOPS')
   ],
   [sg.Sizer(v_pixels=4)],
   [sg.Sizer(h_pixels=63),
    sg.Text('IPv6 User PD:', font=(None, 11, 'bold'), pad=((4, 0), (2, 4))),
    sg.Input('', size=(30, 1), font=('Courier', 12), justification='centered',
      disabled=True, disabled_readonly_background_color='#fdfdfc',
      pad=((0, 4), (4, 4)), key="-USER_PD-"),
    sg.Button('First', font='None 8 bold', pad=((4, 0), (4, 4))),
    sg.Button('Next', font='None 8 bold', pad=((3, 0), (4, 4)), key='-NXT_USER_PD-'),
    sg.Button('Last', font='None 8 bold', pad=((3, 4), (4, 4))),
    sg.Text('(Changes PSID)', font=(None, 11, 'italic'),
      pad=((3, 3), (0, 4))),
    sg.Push()
   ],
   [sg.Text('CE MAP-T WAN Address:', font=(None, 11, 'bold'),
      pad=((4, 0), (2, 4))),
    sg.Input('', size=(30, 1), font=('Courier', 12), justification='centered',
      disabled=True, disabled_readonly_background_color='#fdfdfc',
      pad=((0, 4), (4, 4)), key="CE_V6_WAN"),
    sg.Push()
   ],
   [sg.Sizer(v_pixels=4)],
]

ipv4_section = [
   [sg.Multiline('IPv4 Prefix and Host Bits', size=(None, 2), # size=(83, 13), # auto_size_text=True,...Needed?
      p=4, font=('Courier', 12, 'bold'), background_color='#fdfdfc',
      expand_x=True, disabled=True, border_width=2, # horizontal_scroll = True,
      no_scrollbar=True, key='MLINE_IPV4')
   ],
   [sg.Push(),
    sg.Text('IPv4 Host:', font=(None, 11, 'bold'), pad=((4, 0), (10, 0))),
    sg.Slider(range=(0, 0), default_value=0, orientation='h',
    disable_number_display=False, enable_events=True, border_width=2,
    size=(42, 10), trough_color='white', font=(None, 11, 'bold'),
    pad=((0, 2), (0, 6)), key='-V4HOST_SLIDER-'),
    sg.Button(' + 1', font='None 8 bold', pad=((2, 5), (12, 0)), key='-NEXT_HOST-'),
    sg.Push()
   ],
   [sg.Sizer(v_pixels=4)],
]

portidx_multiline = [
   [sg.Multiline("Port Set ID and Port Selection", size=(None, 3), # size=(83, 13), # auto_size_text=True,...Needed?
      p=4, font=('Courier', 12, 'bold'), background_color='#fdfdfc',
      expand_x=True, disabled=True, border_width=2, # horizontal_scroll = True,
      no_scrollbar=True, key='MLINE_PORTIDX')
   ],
   [sg.Sizer(v_pixels=3)],
   [sg.Text('Source Port Index:', font=(None, 11, 'bold'),
      pad=((6, 0), (1, 4))),
    sg.Input('', size=(16, 1), font=('Courier', 12, 'bold'),
      justification='centered', disabled=True,
      disabled_readonly_background_color='#fdfdfc', pad=((1, 4), (4, 4)),
      key="-SP_INDEX-"),
    sg.Text(f'= Port', font=(None, 11, 'bold'), pad=((0, 0), (1, 4))),
    sg.Input('', size=(16, 1), font=('Courier', 12, 'bold'),
      justification='centered', disabled=True,
      disabled_readonly_background_color='#fdfdfc', pad=((1, 4), (4, 4)),
      key="-SP_INT-"),
    sg.Sizer(h_pixels=16),
    sg.Button(' <<', font='none 8 bold', pad=((4, 2), (4, 4)), key='-P_IDX_FIRST-'),
    sg.Button(' + 1', font='none 8 bold', pad=((2, 2), (4, 4)), key='-P_IDX_UP_1-'),
    sg.Button(' + 10', font='none 8 bold', pad=((2, 2), (4, 4)), key='-P_IDX_UP_10-'),
    sg.Button(' + 100', font='none 8 bold', pad=((2, 2), (4, 4)), key='-P_IDX_UP_100-'),
    sg.Button(' >>', font='none 8 bold', pad=((2, 0), (4, 4)), key='-P_IDX_LAST-')],
   [sg.Sizer(v_pixels=4)]
]

bmr_binops_tab_layout = [
   [sg.Frame("", [
      [sg.Sizer(v_pixels=3)],
      [sg.Text(('Bit analysis performed by CE, to determine its allocated '
                'IPv4 host addresses and ports'),
       font='None 12 bold', text_color='black', background_color="#8399C4",
       justification='centered', 
       border_width=0, relief='raised', pad=0, expand_x=True)],],
       expand_x=True, background_color='#8399C4', border_width=0)
   ],
   [sg.Sizer(v_pixels=4)],
   [sg.Frame("", bmr_pd_layout, font='None 11 bold italic',
      title_location=sg.TITLE_LOCATION_TOP_LEFT, expand_x=True, border_width=2, relief='raised',
      pad=((4, 4), (0, 4)))],
   [sg.Frame("", ipv4_section, font='None 11 bold italic',
      title_location=sg.TITLE_LOCATION_TOP_LEFT, expand_x=True, border_width=2,
      relief="raised", pad=((4, 4), (0, 4)))
   ],
   [sg.Frame("", portidx_multiline,
      font='None 11 bold italic', title_location=sg.TITLE_LOCATION_TOP_LEFT,
      expand_x=True, border_width=2, relief='raised', pad=((4, 4), (0, 4)))
   ],
]

user_ports_multiline = [
      [sg.Multiline(
         'All user ports list',
         size=(None, 11), # size=(83,
         border_width=2,
         pad=4,
         auto_size_text=True,
         font=('Courier', 12),
         background_color='#fdfdfc',
         expand_x=True,
         horizontal_scroll = False,
         disabled=True,
         no_scrollbar=False,
         key='MLINE_PORTS')]
]

user_ports_tab_layout = [
   [sg.Sizer(v_pixels=3)],
   [sg.Text("All ports for current PSID ",
      font=(None, 12, 'bold'), text_color='black', expand_x=True, justification='centered', background_color='#8399C4',)],
   [sg.Sizer(v_pixels=3)],
   [sg.Frame("", user_ports_multiline, expand_x=True, border_width=2, relief='raised')],
   [sg.Sizer(v_pixels=6)],
   [sg.Sizer(v_pixels=4)],
]

dhcp_fields = [
   [sg.Sizer(0, 6),],
   [sg.Text('DMR', font=(None, 11, 'bold'), pad=((4, 0), (3, 0)) ),
    sg.Input('Ex. 2001:db8:ffff::/64', size=(25, 1), font=('Courier', 12),
      justification='centered', background_color='#fdfdfc', 
      disabled_readonly_background_color='#fdfdfc', pad=((0, 0), (4, 0)),
      disabled=True, key='DMR_INPUT'),
    sg.Button('Enter', font='None 8 bold', key='DMR_ENTER')],
   [sg.Text('S46 MAP-T Container Option 95:', font=(None, 11, 'bold')),
    sg.Checkbox('Make FMR String', font=(None, 11, 'bold'), #tooltip=fmr_tooltip,
      enable_events=True, tooltip=fmr_tooltip, key='FMR_FLAG'),
    sg.Text('', text_color='red', font='None 11 bold', key='-DHCP_MESSAGES-')],
   [sg.Sizer(0, 0),
    sg.Input('', size=(93, 1), font=('Courier', 11), justification='centered',
      disabled=True, use_readonly_for_disable=True,
      disabled_readonly_background_color='#fdfdfc', key='OPT_95')],
   [sg.Text(f'Option 89', font=(None, 11, 'bold')),
    sg.Input('', size=(55, 1), font=('Courier', 12), justification='centered',
      disabled=True, use_readonly_for_disable=True,
      disabled_readonly_background_color='#fdfdfc', key='OPT_89')], # OPTION_S46_RULE (89)
   [sg.Text('Option 93', justification='centered', font=(None, 11, 'bold')),
    sg.Input('', font=('Courier', 12), justification='centered',
      disabled=True, use_readonly_for_disable=True,
      disabled_readonly_background_color='#fdfdfc', key='OPT_93')], # OPTION_S46_PORTPARAMS (93)
   [sg.Text(f'Option 91', justification='centered', font=(None, 11, 'bold')),
    sg.Input('', font=('Courier', 12), justification='centered',
      disabled=True, use_readonly_for_disable=True,
      disabled_readonly_background_color='#fdfdfc', key='OPT_91')], # OPTION_S46_DMR (91)
   [sg.Sizer(v_pixels=6)],
]

dhcp_tab_layout = [
   [sg.Sizer(v_pixels=3)],
   [sg.Text("Softwire 46 MAP-T Options for DHCPv6", font=(None, 12, 'bold'),
      text_color='black', background_color='#8399C4', expand_x=True,
      justification='centered')],
   [sg.Frame("", dhcp_fields, expand_x=True, border_width=2, relief='raised')]
]

saved_rules_multiline =[
   [sg.Multiline(
      default_text='IP MAP Calculator BMR strings', 
      size=(None, 11),
      border_width=2,
      pad=3,
      font=('Courier', 12), 
      background_color='#fdfdfc', 
      expand_x=True, 
      disabled=True, 
      autoscroll=True,
      horizontal_scroll=True,
      key='-MLINE_SAVED-'
      )
   ]
]

saved_rules_tab_layout = [
   [sg.Sizer(v_pixels=3)],
   [sg.Push( background_color='#8399C4'),
    sg.Text("Saved BMR Strings", font=(None, 12, 'bold'),
       text_color='black', background_color='#8399C4', justification='centered'),
    sg.Text("(To enter in 'BMR String' field)", font=(None, 12, 'italic'),
       text_color='black', background_color='#8399C4', justification='centered'),
    sg.Push( background_color='#8399C4')],
   [sg.Frame("", saved_rules_multiline, p=4, expand_x=True, border_width=2, relief='raised')],
   [sg.Sizer(v_pixels=6)],
]

tab_group_layout = [
   [sg.Tab('Binary Operations', bmr_binops_tab_layout, background_color='#8399C4',
      key='TAB_BINARY'),
    # image_source=binops_tab_label, key='TAB_BINARY'),
    # sg.Tab('User PD', user_pd_tab_layout, key='TAB_UPD'),
    sg.Tab('User Ports', user_ports_tab_layout,  background_color='#8399C4', key='TAB_PORTS'),
    sg.Tab('DHCP Options', dhcp_tab_layout, background_color='#8399C4', key='TAB_DHCP'),
    sg.Tab('Saved Rules', saved_rules_tab_layout, background_color='#8399C4', key='TAB_SAVED')]
]

# Error messages
bin_display_col3 = [
   [sg.Push(),
    sg.Text('', text_color='red', font='None 14 bold',
            pad=((5, 5), (0, 0)), key='-PARAM_MESSAGES-'),
    sg.Push()],
   [sg.Sizer(h_pixels=0, v_pixels=1)]
]

# Binary Display (5th frame)
#-------------------------------------#
button_col1 = [
   [sg.Button('Example', font='Helvetica 11', key='-EXAMPLE-'),
    sg.Button('Clear', font='Helvetica 11', key='-CLEAR-'),
    sg.Text('', text_color='red', font='None 14 bold', key='-PARAM_MESSAGES-'),
    sg.Push(),
#    sg.Button('Save', font='Helvetica 11', key=('-SAVE_MAIN-')),
    sg.Button('About', font=('Helvetica', 12)),
    sg.Button(' Exit ', font=('Helvetica', 12, 'bold'))]
]

button_layout = [
   [sg.Column(button_col1, expand_x=True)]
]

layout = [
   [sg.Sizer(v_pixels=4)],
   [sg.Frame("", display_layout, element_justification='centered',
      expand_x=True, border_width=4)],
   [sg.Frame("Enter or Edit BMR Parameters", editor_layout,
      font=(None, 12, 'bold'), title_location=sg.TITLE_LOCATION_TOP,
      border_width=4, expand_x=True,)],
   [sg.TabGroup(tab_group_layout, enable_events=True, border_width=1,
      tab_background_color='#C8D1E5', selected_background_color='#8399C4',
      title_color='black', selected_title_color='black', tab_border_width=2,
      key="TABGROUP")],
   [sg.Sizer(v_pixels=5)],
   [sg.Sizer(h_pixels=8),
    sg.Button('Example Values', font='None 8 bold', focus=True, key="EXAMPLE"), 
    sg.Button('Clear', font='None 8 bold', pad=(4, 0)),
    sg.Push(),
    sg.Button('About', font='None 8 bold', pad=(4, 0)),
    # sg.Push(),
    sg.Exit(pad=(4, 0), font='None 8 bold'),
    sg.Sizer(h_pixels=8)],
   [sg.Sizer(v_pixels=5)],
]

#-------------------------------------------------------------------------#
# Create Main Window
#-------------------------------------------------------------------------#
# Window uses last screen location for next start
# Location is set upon Exit or WINDOW_CLOSE... event
window = sg.Window('IP MAP Calculator', layout, font=windowfont,
   enable_close_attempted_event=True,
   location=sg.user_settings_get_entry('-location-', (None, None)),
   keep_on_top=False, resizable=True, finalize=True)

# Bind tkinter events to text fields
window['-STRING_IN-'].bind('<Return>', '_Enter')
window['DMR_INPUT'].bind('<FocusIn>', '_FOCUS')
window['DMR_INPUT'].bind('<Return>', '_Enter')

'''
██████  ██    ██ ██      ███████      ██████  █████  ██       ██████ 
██   ██ ██    ██ ██      ██          ██      ██   ██ ██      ██      
██████  ██    ██ ██      █████       ██      ███████ ██      ██      
██   ██ ██    ██ ██      ██          ██      ██   ██ ██      ██      
██   ██  ██████  ███████ ███████      ██████ ██   ██ ███████  ██████ 
'''

#----------------------------------------------------------------------------#
# Calculate Results
#----------------------------------------------------------------------------#
# param_ls contains BMR parameters
# param_ls = [name, v6pfx, v6pfx len, v4pfx, v4pfx len, ealen, psid offset]
# user_pd_obj is "User delegated prefix" received from DHCP
def rule_calc(param_ls, user_pd_obj, v4host = None, portidx = None):
   '''The rule_calc function accepts a BMR paramater list, an IPv6
   user PD (ipaddress object), and an optional port index integer from
   a user input or editing option. It calculates the network address results,
   formats them for the UI, and enters them into a dictionary for the
   UI display function displays_update().
   '''

   # initial values
   #----------------------------------#
   psidlen = (param_ls[5] - (32 - param_ls[4])) # ea_len - host_len
   bmrpfx_len = param_ls[2]
   upd_len = user_pd_obj.prefixlen
   psid_ofst = param_ls[6]

   # ppusr = 2^(16 - k) - 2^m (per rfc7597) (2^m is # of excluded ports)
   # 16 is the number of IP port bits (constant)
   # Used for d_dic and other calculations
   if param_ls[6] > 0: # Because PSID Offset > 0 excludes some ports
      ppusr = (2 ** (16 - psidlen)) - (2 ** (16 - psidlen - param_ls[6]))
   else:
      ppusr = (2 ** (16 - psidlen))

   # If call is from the host slider, update the upd with host bits
   # and update v4pfx value in param_ls
   if v4host != None:
      pdbin = f'{user_pd_obj.network_address:b}'
      pdbin_l = pdbin[:param_ls[2]]
      pdbin_r = pdbin[param_ls[2] + (32 - last_params[4]) : ]
      v4hostbin = bin(v4host)[2:].zfill(32 - param_ls[4])
      newpdbin = pdbin_l + v4hostbin + pdbin_r
      newpdint = int(newpdbin, 2)
      new_upd_add_str = \
         ip.IPv6Address(newpdint).compressed + '/' + str(user_pd_obj.prefixlen)
      user_pd_obj = ip.IPv6Network(new_upd_add_str)
      v4pfxbin = f'{ip.IPv4Address(param_ls[3]):b}'[: int(param_ls[4])]
      newv4bin = v4pfxbin + v4hostbin
      newv4int = int(newv4bin, 2)
      newv4add = ip.IPv4Address(newv4int)
      v4str = newv4add.compressed
   else:
      v4pfxbin = f'{ip.IPv4Address(param_ls[3]):b}'
      v4hostbin = f'{user_pd_obj.network_address:b}]'[bmrpfx_len : bmrpfx_len + (32 - param_ls[4])]
      v4hostint = int(v4hostbin, 2)
      newv4bin = v4pfxbin[:param_ls[4]] + v4hostbin
      # window['-V4HOST_SLIDER-'].update(value=0)
      newv4add = ip.IPv4Address(int(newv4bin, 2))
      v4str = newv4add.compressed
      window['-V4HOST_SLIDER-'].update(v4hostint)

   #-------------------------------------------------------------------------#
   # Binary display strings
   #-------------------------------------------------------------------------#
   # Sec 1, BMR PD, User PD, and EA Bits data
   #--------------------------------------------------#
   v6p_hex_exp = ip.IPv6Address(param_ls[1]).exploded # Hex style: 0000:0000:...
   v6p_hex_seglst = v6p_hex_exp.split(':')[:4] # ['0000', '0000', ...]
   upd_hex_exp = ip.IPv6Address(user_pd_obj.network_address).exploded # 0000:0000:...
   upd_hex_seglst = upd_hex_exp.split(':')[:4] # ['0000', '0000', ...]
   v6p_bin = f'{ip.IPv6Address(param_ls[1]):b}'[:64] # first 64 bits of pfx
   v6p_bin_seglst = [v6p_bin[i:i+16] for i in range(0, 64, 16)]
   v6p_bin_fmt = ':'.join(v6p_bin_seglst) + f'::/{bmrpfx_len}'
   upd_bin = f'{ip.IPv6Address(user_pd_obj.network_address):b}'[:64]
   upd_bin_seglst = [upd_bin[i:i+16] for i in range(0, 64, 16)]
   upd_bin_fmt = ':'.join(upd_bin_seglst) + f'::/{upd_len}'
   ea_bin_idxl = V6Indices(param_ls[2]) # V6Indices adds # of ":"separators
   ea_bin_idxr = V6Indices(upd_len)
   ea_bin_fmt = upd_bin_fmt[ea_bin_idxl : ea_bin_idxr]

   # Sec 1, User PD (upd) string data
   #-----------------------------------#
   v4hostbin_len = 32 - param_ls[4]
   psid_idxl = param_ls[2] + v4hostbin_len
   psid_idxr = param_ls[2] + param_ls[5]
   psid = upd_bin[psid_idxl : psid_idxr]
   # Generate 16 bit string for Port number
   # is PSID > 0?
   if param_ls[6] > 0:
      psid_ofst_bin = bin(1)[2:].zfill(param_ls[6]) # binary 1 with len = offset
   else:
      psid_ofst_bin = ''
   portrpad_bin = '0' * (16 - param_ls[6] - psidlen) # MAY NEED TO ACCEPT EDITOR VALUES !!!
   port_bin = psid_ofst_bin + \
              psid + \
              portrpad_bin
   port_int = str(int(port_bin, 2))
   pidx_bin = psid_ofst_bin + portrpad_bin # Port index number binary string

   # Sec 1, IPv4 string data
   #-----------------------------------#
   v4_seglst = v4str.split('.')
   v4mask = param_ls[4]
   # make segments equal length for display
   v4_bin_seglst = [newv4bin[i:i+8] for i in range(0, 32, 8)]
   v4_bin_fmt = '.'.join(v4_bin_seglst) + f'/{v4mask}'
   for i, seg in enumerate(v4_seglst):
      if len(seg) == 3:
         pass
      elif len(seg) == 2:
         v4_seglst[i] = f' {seg}'
      elif len(seg) == 1:
         v4_seglst[i] = f' {seg} '

   # Sec 1, Modify Port string if Port Index (portidx) has been changed
   #--------------------------------------------------------------------#
   if portidx:
      # Initial value of port index
      pidx_bin_base = int(pidx_bin, 2)
      if portidx == 0:
         pass
      # Increment val can't exceed max value of idx binary - index initial value
      elif portidx < (2 ** len(pidx_bin)) - pidx_bin_base:
         pidx_int = int(pidx_bin, 2)
         pidx_int = pidx_int + portidx
         pidx_bin = bin(pidx_int)[2:].zfill(len(pidx_bin)) # for d_dic
         psid_ofst_bin = pidx_bin[: psid_ofst]
         portrpad_bin = pidx_bin[psid_ofst:]
         port_bin = psid_ofst_bin + psid + portrpad_bin
         port_int = int(port_bin, 2) # for d_dic
      else:
         window['-PARAM_MESSAGES-'].update('Port index maximum reached')
         pidx_bin = "1" * len(pidx_bin)
         pidx_int = int(pidx_bin, 2)
         psid_ofst_bin = pidx_bin[: psid_ofst]
         portrpad_bin = pidx_bin[psid_ofst:]
         port_bin = psid_ofst_bin + psid + portrpad_bin
         port_int = int(port_bin, 2) # for d_dic

   # BMR PD, User PD, and EA Bits dictionary entries
   #--------------------------------------------------#
   bin_str_dic = {
      'blank1': '',
      'v6p_hexstr': (f" BMR PD:{' ' * 8}"
                     f"{'      :      '.join(v6p_hex_seglst)}"
                     f"      ::/{bmrpfx_len}"),
      'upd_hexstr': (f" User PD:{' ' * 7}"
                     f"{'      :      '.join(upd_hex_seglst)}"
                     f"      ::/{upd_len}"),
      'bmr_binstr': f' BMR PD:  {v6p_bin_fmt}',
      'upd_binstr': f' User PD: {upd_bin_fmt}',
      'ea_binstr': f' EA Bits: {"." * V6Indices(param_ls[2])}{ea_bin_fmt}',
   }

   ipv4_str_dic = {
      # 'blank2': '',
      'v4_intstr': (f" IPv4 Addr:     "
                    f"{'  .   '.join(v4_seglst)}"
                    f"  /{v4mask}"),
      'v4_binstr': f" IPv4 Addr:  {v4_bin_fmt}",
   }

   portidx_str_dic = {
      # 'blank3': '',
      'portidx': (f' Port Index: '
                  f' {psid_ofst_bin}-{portrpad_bin}'
                  f' (psid-offset/padding or "a bits/m bits")'),
      'port_bin': (f' Port binary: {psid_ofst_bin}-{psid}-{portrpad_bin} '
                   f'(psid offset/psid/padding or "a bits/psid/m bits")'),
      'port_dec': (f' Port integer: {port_int}')
   }

   if psid != '':
      # Number of user contiguous port sequences (omits sequence 0)
      # sequences = range(1, 2 ** psid_ofst)
      if psid_ofst > 0:
         sequences = range(1, 2 ** psid_ofst)

         # Interval between *initial port numbers* of contiguous port sequences
         seq_rng_intvl = 2 ** (16 - psid_ofst)

         # Number of ports in contiguous port sequences
         seq_len = (16 - psid_ofst - psidlen) # 'm' bits
         prt_seq_len = 2 ** seq_len

         # List of port sequences with format "start-end"
         psid_int = int(psid, 2) # PSID value as an integer
         seq_mod = psid_int * prt_seq_len
         seq_list = [
            (f"{x * seq_rng_intvl + seq_mod}"
             f"-{(x * seq_rng_intvl + seq_mod) + prt_seq_len - 1}")
            for x in sequences
         ]
      else:
         seq_list = [
            (f"{int(psid + '0' * (16 - len(psid)), 2)}"
             f"-{int(psid + '1' * (16 - len(psid)), 2)}")
         ]
   else:
      seq_list = [
         f"{int(psid_ofst_bin + '0' * (16 - psid_ofst), 2)}-{int('1' * 16, 2)}"
      ]

   # PSID and PSID Offset Warnings flags
   no_psid = False
   no_offset = False
   high_offset = False
   if psid == '':
      no_psid = True
   elif psid_ofst == 0:
      no_offset = True
   elif psid_ofst > 6:
      high_offset = True
   
   # Binary displays highlight index data
   #---------------------------------------------------------------------#
   # # return index of first character after " BMR PD: "
   # bmr_pfx_l = next(i for (i, e) in enumerate(bin_str_dic["bmr_binstr"])
   #    if e not in "BMR PD: ") #................................Can this be hardcoded to 10?
   bmr_pfx_l = 10
   bmr_pfx_r = bmr_pfx_l + V6Indices(param_ls[2])
   v6_pfxlen_l = 79
   v6_pfxlen_r = 82
   upd_pfx_l = bmr_pfx_r
   upd_pfx_r = bmr_pfx_l + V6Indices(upd_len)
   upd_binstr_sbnt_l = upd_pfx_r
   upd_binstr_sbnt_r = bin_str_dic['upd_binstr'].index('::')
   ea_binstr_l = next(i for (i, e) in enumerate(bin_str_dic["ea_binstr"])
      if e not in "EA Bits:.")
   ea_binstr_r = ea_binstr_l + len(ea_bin_fmt)
   # ea_binstr_div is v4host_r and psid_l
   ea_binstr_div = bmr_pfx_l + V6Indices(param_ls[2] + v4hostbin_len)
   v4ip_hl_l = 13 + V4Indices(param_ls[4])
   v4ip_hl_r = 13 + V4Indices(32)
   prtidx_ofst_l = 14
   prtidx_ofst_r = prtidx_ofst_l + param_ls[6]
   prtidx_pad_l = prtidx_ofst_r + 1
   prtidx_pad_r = prtidx_pad_l + (16 - param_ls[6] - psidlen)
   portbin_ofst_hl_l = 14
   portbin_ofst_hl_r = portbin_ofst_hl_l + param_ls[6]
   portbin_psid_hl_l = 14 + psid_ofst + 1
   portbin_psid_hl_r = portbin_psid_hl_l + psidlen
   portbin_pad_hl_l = portbin_psid_hl_r + 1
   portbin_pad_hl_r = portbin_pad_hl_l + (16 - param_ls[6] - psidlen)

   # Binary display 1 highlight index dictionary
   #---------------------------------------------#
   # Prepend line number for each highlight index
   hl_dic1 = {
      'bmr_hl': [f'4.{bmr_pfx_l}', f'4.{bmr_pfx_r}'],
      'bmr_len_hl': [f'4.{v6_pfxlen_l}', f'4.{v6_pfxlen_r}'],
      'upd_hl': [f'5.{upd_pfx_l}', f'5.{upd_pfx_r}'],
      'upd_len_hl': [f'5.{v6_pfxlen_l}', f'5.{v6_pfxlen_r}'],
      'sbnt_hl': [f'5.{upd_binstr_sbnt_l}', f'5.{upd_binstr_sbnt_r}'],
      'ea_v4_hl': [f'6.{ea_binstr_l}', f'6.{ea_binstr_div}'],
      'ea_psid_hl': [f'6.{ea_binstr_div}', f'6.{ea_binstr_r}'],
      'v4ip_hl': [f'8.{v4ip_hl_l}', f'8.{v4ip_hl_r}'],
      'v4ipbin_hl': [f'9.{v4ip_hl_l}', f'9.{v4ip_hl_r}'],
   }

   # Binary IPv4 display highlight index dictionary
   #------------------------------------------------#
   hl_dic_v4 = {
      'v4ip_hl': [f'2.{v4ip_hl_l}', f'2.{v4ip_hl_r}'],
      'v4ipbin_hl': [f'3.{v4ip_hl_l}', f'3.{v4ip_hl_r}'],
   }

   # Binary Port Index display highlight index dictionary
   #------------------------------------------------------#
   hl_dic_port = {
      'prtidx_ofst_hl': [f'1.{prtidx_ofst_l}', f'1.{prtidx_ofst_r}'],
      'prtidx_pad_hl': [f'1.{prtidx_pad_l}', f'1.{prtidx_pad_r}'],
      'portbin_ofst_hl': [f'2.{portbin_ofst_hl_l}', f'2.{portbin_ofst_hl_r}'],
      'portbin_psid_hl': [f'2.{portbin_psid_hl_l}', f'2.{portbin_psid_hl_r}'],
      'portbin_pad_hl': [f'2.{portbin_pad_hl_l}', f'2.{portbin_pad_hl_r}']
   }

   #-------------------------------------------------------------------------#
   # Results = Display values dictionary
   #-------------------------------------------------------------------------#
   d_dic = {
      'paramlist': param_ls,
      'v4ips': 2 ** v4hostbin_len, # 2^host_bits
      'sratio': 2 ** psidlen, # num of unique psids per v4-host address
      'users': (2 ** v4hostbin_len) * (2 ** psidlen),
      'ppusr': ppusr,
      'excl_ports': 65536 - ((2 ** psidlen) * (ppusr)),
      'bmr_str': '|'.join([str(x) for x in param_ls]),
      'upd_str': user_pd_obj.compressed, # upd_str = User Delegated Prefix (PD)
      'ce_ip': v4str,
      'port_int': port_int,
      'pidx_bin': pidx_bin,
      'bin_str_dic': bin_str_dic,
      'ipv4_str_dic': ipv4_str_dic,
      'portidx_str_dic': portidx_str_dic,
      # 'bin_ipstr_dic': bin_ipstr_dic,
      'hl_dic1': hl_dic1,
      'hl_dic_v4': hl_dic_v4,
      'hl_dic_port': hl_dic_port,
      # 'hl_dic2': hl_dic2,
      'num_excl_ports': 2 ** (16 - param_ls[6]),
      'seq_list': seq_list,
      'no_psid': no_psid,
      'no_offset': no_offset,
      'high_offset': high_offset
   }

   if v4host == None:
      clear_dhcp_fields()

   displays_update(d_dic, user_pd_obj)

   return

'''
██████  ██ ███████ ██████  ██       █████  ██    ██ ███████ 
██   ██ ██ ██      ██   ██ ██      ██   ██  ██  ██  ██      
██   ██ ██ ███████ ██████  ██      ███████   ████   ███████ 
██   ██ ██      ██ ██      ██      ██   ██    ██         ██ 
██████  ██ ███████ ██      ███████ ██   ██    ██    ███████ 
'''

def displays_update(dic, pd_obj):
   '''The displays_update function accepts a display values dictionary
   and an IPv6 user PD (ipaddress object) from the rule_calc function.
   It then updates all affected display fields.
   '''

   # Initial field updates
   #----------------------------------#
   # Output BMR results to display
   window['-IPS_DSPLY-'].update(dic['v4ips'])
   window['-RATIO_DSPLY-'].update(dic['sratio'])
   window['-USERS_DSPLY-'].update(dic['users'])
   window['-PORTS_DSPLY-'].update(dic['ppusr'])
   window['-EXCL_PORTS_DSPLY-'].update(dic['excl_ports'])
   # window['-BMR_STRING_DSPLY-'].update(dic['bmr_str'])

   # Output values to Edit String and Values fields
   window['-STRING_IN-'].update(dic['bmr_str'])
   for i, element in enumerate(pframe_ls):
      window[element].update(dic['paramlist'][i])

   # Output User PD, CE IP, and Port to binary string editor
   window['-USER_PD-'].update(dic['upd_str'])
   # window['-USER_IP4-'].update(dic['ce_ip'])
   # window['-USER_PORT-'].update(dic['port_int'])
   window['-SP_INT-'].update(dic['port_int'])
   window['-SP_INDEX-'].update(dic['pidx_bin'])

   # Binary displays update values and highlights
   multiline1: sg.Multiline = window['MLINE_BINOPS']
   multiline2: sg.Multiline = window['MLINE_IPV4']
   multiline3: sg.Multiline = window['MLINE_PORTIDX']
   # multiline5: sg.Multiline = window['MLINE_BIN_2']

   multiline1.update('')
   for num, bstr in enumerate(dic['bin_str_dic']):
      multiline1.update(dic['bin_str_dic'][bstr]
       + ('\n' if num < len(dic['bin_str_dic']) -1 else ''), append=True)

   multiline2.update('')
   for num, bstr in enumerate(dic['ipv4_str_dic']):
      multiline2.update(dic['ipv4_str_dic'][bstr]
       + ('\n' if num < len(dic['ipv4_str_dic']) -1 else ''), append=True)

   multiline3.update('')
   for num, bstr in enumerate(dic['portidx_str_dic']):
      multiline3.update(dic['portidx_str_dic'][bstr]
       + ('\n' if num < len(dic['portidx_str_dic']) -1 else ''), append=True)

   # Apply highlighting
   highlights(multiline1, dic)
   highlights(multiline2, dic)
   highlights(multiline3, dic)
   # highlights(multiline5, dic)

   # Format port list and output to Source Port List field
   #-------------------------------------------------------#
   # "x" row result array will be transposed into "x" columns, to fit in the output field
   rows = 6
   port_seqs = dic['seq_list']
   width = max(len(item) for item in port_seqs)  # Find max item width

   # Pad list items to keep columns aligned
   for i, item in enumerate(port_seqs):
      port_seqs[i] = port_seqs[i].ljust(width)
   
   # Make list fit evenly into number of rows (will be transposed to columns)
   columns, remainder = divmod(len(port_seqs), rows)

   if remainder:
      add = range(rows - remainder)
      for x in add:
         port_seqs.append('')
      columns += 1

   # Generator for port_seqs list indices
   idx = (x for x in range(len(port_seqs)))
   array = [[port_seqs[next(idx)] for _ in range(columns)] for _ in range(rows)]

   # Transpose n rows into n columns.
   newarray = []
   newarray = transpose(array, newarray)

   # Output port sequences list to User Ports multiline field
   array_list = []
   window['MLINE_PORTS'].update('') # Clear field
   for ls in enumerate(newarray):
      # Don't append "\n" to last line
      if ls[0] + 1 < len(newarray):
         line = '  '.join(ls[1]) + '\n'
      else:
         line = '  '.join(ls[1])
      array_list.append(line)
      array_string = ''.join(array_list)
   window['MLINE_PORTS'].update(array_string)

   # Warnings for 'no psid = well known ports may be included'
   if dic['no_psid'] == True:
      alert_line = ('No PSID!\n'
              'Sharing Ratio = 1.\n\n')
      window['MLINE_PORTS'].update(alert_line)
      window['MLINE_PORTS'].update(array_string, append=True)
      window['-PARAM_MESSAGES-'].update('No PSID. Sharing Ratio = 1.')

   # Warnings for no psid offset'
   if dic['no_offset'] == True:
      alert_line = ('No PSID Offset!\nNo Ports Excluded!\n'
              'To exclude ports, lower bound on allowed set of PSID values is required.\n'
              'See RFC 7597, Appendix B.1.\n'
              'https://datatracker.ietf.org/doc/html/rfc7597#appendix-B.1\n\n')
      window['MLINE_PORTS'].update(alert_line)
      window['MLINE_PORTS'].update(array_string, append=True)
      window['-PARAM_MESSAGES-'].update('No PSID Offset. See "User Ports" tab for details.')

   # Warnings for 'high psid offset = well-known ports may be included'
   if dic['high_offset'] == True:
      alert_line = ('PSID Offset > 6!\nWell-known ports may be included!\n'
              'Ports included by the first User PDs may be < 1024.\n\n')
      window['MLINE_PORTS'].update(alert_line)
      window['MLINE_PORTS'].update(array_string, append=True)
      window['-PARAM_MESSAGES-'].update('High PSID Offset. See "User Ports" tab for details.')

   # Output values to binary editor sliders and input fields
   window['-V6PFX_LEN_SLDR-'].update(disabled=False)
   window['-EA_LEN_SLDR-'].update(disabled=False)
   window['-V4PFX_LEN_SLDR-'].update(disabled=False)
   window['-PSID_OFST_SLDR-'].update(disabled=False)
   window['-V6PFX_LEN_SLDR-'].update(dic['paramlist'][2])
   window['-EA_LEN_SLDR-'].update(dic['paramlist'][5])
   window['-V4PFX_LEN_SLDR-'].update(dic['paramlist'][4])
   window['-PSID_OFST_SLDR-'].update(dic['paramlist'][6])
   window['-V4HOST_SLIDER-'].update(range=(0, dic['v4ips'] - 1))
#   window['-PORT_SLIDER-'].update(range=(0, (dic['ppusr'] - 1) ))
#   window['-PORT_INDEX-'].update('0') #### <<<<--- UPDATE WITH ACTUAL VALUE !!! !!!

   return

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

def highlights(display, dic):
   """ Highlighting for binary displays. Called from displays_update() """
   widget = display.Widget
 
   # Highlight color option definitions
   #-------------------------------------#
   widget.tag_config('white', foreground='black', background='#FFFFFF')
   widget.tag_config('yellow', foreground='black', background='#FFFF21') #FFFF00
   widget.tag_config('new_yellow', foreground='black', background='#F8FF00')
   widget.tag_config('burley', foreground='black', background='#FFD39B') # burlywood
   widget.tag_config('burley3', foreground='black', background='#CDAA7D') # burlywood3
   widget.tag_config('grey49', foreground='black', background='#7D7D7D')
   widget.tag_config('sage', foreground='black', background='#C2C9A6')
   widget.tag_config('peri', foreground='black', background='#B2CAFA') # periwinkle
   widget.tag_config('pink', foreground='black', background='#ff90c7')
   widget.tag_config('new_teal', foreground='black', background='#7cdff3') # moonstone
   widget.tag_config('Turquoise', foreground='black', background='#46E1D1')
   widget.tag_config('lt_purple', foreground='black', background='#D7C1D5')
   widget.tag_config('lt_blue1', foreground='black', background='#B3C3D1') # lt blue grey
   widget.tag_config('lt_blue2', foreground='black', background='#CCD7E0') # ltr blue grey
   widget.tag_config('lt_blue', foreground='black', background='#B2CAFA') # lt blue
   widget.tag_config('tan', foreground='black', background='tan')
   widget.tag_config('lt_tan', foreground='black', background='#dbcdbd')
   widget.tag_config('lt_orange', foreground='black', background='#ffcc99')
   widget.tag_config('new_lt_green', foreground='black', background='#c2ebc2')
   widget.tag_config('light_green', foreground='black', background='#00ff19')
   widget.tag_config('grey_blue', foreground='black', background='#a4b5c1')
   widget.tag_config('Sunshade', foreground='black', background='#fdaf46')
   widget.tag_config('Malibu', foreground='black', background='#FFFF21')

   if display.Key == 'MLINE_BINOPS':
      widget.tag_add('light_green', *dic['hl_dic1']['bmr_hl'])
      widget.tag_add('light_green', *dic['hl_dic1']['bmr_len_hl'])
      widget.tag_add('light_green', *dic['hl_dic1']['upd_hl'])
      widget.tag_add('light_green', *dic['hl_dic1']['upd_len_hl'])
      widget.tag_add('grey_blue', *dic['hl_dic1']['sbnt_hl'])
      widget.tag_add('pink', *dic['hl_dic1']['ea_v4_hl'])
      widget.tag_add('yellow', *dic['hl_dic1']['ea_psid_hl'])

   elif display.Key == 'MLINE_IPV4':
      widget.tag_add('pink', *dic['hl_dic_v4']['v4ip_hl'])
      widget.tag_add('pink', *dic['hl_dic_v4']['v4ipbin_hl'])

   elif display.key == 'MLINE_PORTIDX':
      widget.tag_add('Sunshade', *dic['hl_dic_port']['prtidx_ofst_hl'])
      widget.tag_add('Turquoise', *dic['hl_dic_port']['prtidx_pad_hl'])
      widget.tag_add('Sunshade', *dic['hl_dic_port']['portbin_ofst_hl'])
      widget.tag_add('yellow', *dic['hl_dic_port']['portbin_psid_hl'])
      widget.tag_add('Turquoise', *dic['hl_dic_port']['portbin_pad_hl'])

   return

# Example BMR prefix lists and parameters
#-----------------------------------------#
# param_ls = [name, v6pfx, v6pfx mask, v4pfx, v4pfx mask, ealen, psid offset]
class ExampleParams:
   '''Returns a list of example BMR parameters. The Python ipaddress module and
   self.rv6blk is used to create an IPv6 class (.subnets) object. New IPv6 BMR
   prefixes are pulled from this object until ExampleParams() is called and
   last_plist (created in global space by a global function) has been changed.
   At this time, a new class instance is created and saved.
   '''
   def __init__(self):
      self.ex_cnt = None
      self.last_plist = []
      self.rv6plen = 46
      self.rv4plen = 24
      self.ealen = 14
      self.psid_ofst = 6
      self.rv6blk = '2001:db8::/32'
      self.rv4blk = '192.168.0.0/16'
      self.rv6pfx_obj = None
      self.rv4pfx_obj = None

   def new_params(self):
      if self.last_plist:
         plist = self.last_plist
         plist[0] = 'example_' + str(next(self.ex_cnt) + 1)
         plist[1] = next(self.rv6pfx_obj).network_address.compressed
         plist[3] = next(self.rv4pfx_obj).network_address.compressed
         return(plist)
      else:
         self.ex_cnt = (i for i in range(16384))
         self.rv6pfx_obj = ip.ip_network(self.rv6blk).subnets(
            new_prefix = self.rv6plen)
         self.rv4pfx_obj = ip.ip_network(self.rv4blk).subnets(
            new_prefix = self.rv4plen)
         plist = ['example_' + str(next(self.ex_cnt) + 1),
                  next(self.rv6pfx_obj).network_address.compressed,
                  self.rv6plen,
                  next(self.rv4pfx_obj).network_address.compressed,
                  self.rv4plen,
                  self.ealen,
                  self.psid_ofst
                 ]
         self.last_plist = plist
         return(plist)

class UserPd:
   '''Return a User Delegated Prefix (PD|upd) object.
   If BMR parameters (last_plist) remains the same, it returns
   PD object from current object. If the parameters change,
   a new PD object is created.
   syntax: x = UserPd(param_ls)
   print(x.new_pd())'''
   def __init__(self, plist):
      self.plist = plist
      self.last_plist = []
      self.pd_obj = None
      self.lastpd = ''

   def new_pd(self):
      if self.plist == self.last_plist:  # Next PD from current PD object
         nextpd = next(self.pd_obj)
         self.lastpd = nextpd
         return nextpd
      else:                              # New PD object & new PD
         self.last_plist = self.plist
         bmr_v6p = ip.ip_network('/'.join((self.plist[1], str(self.plist[2]))))
         pd_len = int(self.plist[2]) + int(self.plist[5])
         self.pd_obj = bmr_v6p.subnets(new_prefix = pd_len)
         nextpd = next(self.pd_obj)
         self.lastpd = nextpd
         return nextpd

# "Pad right" when IPv6 prefix not divisible by 8
def find_next_divisible(num):
    """Finds the next higher number evenly divisible by the divisor."""
    while True:
        if num % 8 == 0:
            return num
        num += 1

#-------------------------------------------------------------------------#
# DHCPv6 Option String Calculations = Based on RFC7597
#-------------------------------------------------------------------------#
def dhcp_calc(dmr, fmr=False):
   rulv6_obj = ip.ip_network(f"{param_ls[1]}/{param_ls[2]}")
   rulv6_len = rulv6_obj.prefixlen
   rulv4_obj = ip.ip_network(f"{param_ls[3]}/{param_ls[4]}")
   rulv4_len = rulv4_obj.prefixlen
   # rulv4_host_len = 32 - rulv4_len
   ea_bits = int(param_ls[5])
   ps_ofst = int(param_ls[6]) # "a bits" from RFC 7597
   # psid_len = ea_bits - (32 - rulv4_len) # "k bits" from RFC 7597
   # m_bits = 16 - ps_ofst - psid_len      # "m bits" from RFC 7597
   dmr_obj = ip.ip_network(dmr)
   dmr_len = dmr_obj.prefixlen

   # sharing_ratio = 2**psid_len
   # ports_per_user = 2 ** (16 - psid_len) - 2 ** m_bits
   # ports_per_user = ppusr
   # v4_host_ips = 2 ** (32 - rulv4_len)
   # max_users = v4_host_ips * sharing_ratio
   # user_pd_len = rulv6_len + ea_bits
   # user_pd_1 = f"{rulv6_obj.network_address.compressed}/{user_pd_len}"

   opt_95_lbl_hex = "005f"
   opt_89_lbl_hex = "0059"
   opt_93_lbl_hex = "005d"
   opt_91_lbl_hex = "005b"
   opt_93_len_hx = "0004" # hard coded per RFC 7598

   rulv6_len_hx = hex(rulv6_len).lstrip("0x").zfill(2)
   rulv6_opt_len = find_next_divisible(rulv6_len)
   rulv6_opt_hx = rulv6_obj.network_address.exploded.replace(":", "")[:rulv6_opt_len//4]

   dmr_len_hx = hex(dmr_len).lstrip("0x").zfill(2)
   dmr_opt_len = find_next_divisible(dmr_len)
   dmr_opt_hx = dmr_obj.network_address.exploded.replace(":", "")[:dmr_opt_len//4]

   v4_len_hx = hex(rulv4_len).lstrip("0x").zfill(2)
   v4_segs = rulv4_obj.network_address.exploded.split(".")
   v4_segs_hx = [hex(int(seg)).lstrip("0x").zfill(2) for seg in v4_segs]
   v4_opt_hx = "".join(v4_segs_hx)

   ea_bits_hx = hex(ea_bits).lstrip("0x").zfill(2)
   ps_ofst_hx = hex(ps_ofst).lstrip("0x").zfill(2)
   # rule_flags_hx = "00"
   if fmr == True:
      rule_flags_hx = "01" # Option for FMR
   else:
      rule_flags_hx = "00" # Option for BMR, not FMR

   # S46 Port Parameters
   opt_93_val = ps_ofst_hx + "000000" # Hard coding PSID Length & PSID to all 0's per this design
   opt_93_str = opt_93_lbl_hex + opt_93_len_hx + opt_93_val

   # S46 Rule Option
   opt_89_val = rule_flags_hx + ea_bits_hx + v4_len_hx + v4_opt_hx + rulv6_len_hx + rulv6_opt_hx
   opt_89_len = ( len(opt_89_val) + len(opt_93_str) ) // 2
   opt_89_len_hx = hex(opt_89_len).lstrip("0x").zfill(4)
   opt_89_str = opt_89_lbl_hex + opt_89_len_hx + opt_89_val + opt_93_str

   # S46 DMR Option
   opt_91_val = dmr_len_hx + dmr_opt_hx
   opt_91_len_hx = hex((dmr_len // 4) // 2 + 1).lstrip("0x").zfill(4)
   opt_91_str = opt_91_lbl_hex + opt_91_len_hx + opt_91_val

   # S46 MAP-T Container Option
   opt_95_len = ( len(opt_89_str) + len(opt_91_str) ) // 2
   opt_95_len_hx = hex(opt_95_len).lstrip("0x").zfill(4)
#   opt_95_str = opt_95_lbl_hex + opt_95_len_hx + opt_89_str + opt_91_str # moved to opt_95_w_head

   opt_95_payload = opt_89_str + opt_91_str
   opt_95_w_head = f"({opt_95_lbl_hex}{opt_95_len_hx}){opt_95_payload}"

   # window['OPT_95'].update(opt_95_payload)
   window['OPT_95'].update(opt_95_w_head)
   window['OPT_89'].update(opt_89_str)
   window['OPT_93'].update(opt_93_str)
   window['OPT_91'].update(opt_91_str)

   opt89_str_len = len(opt_89_str)
   opt93_str_len = 15
   opt91_str_len = len(opt_91_str)





# Account for IP address separators (: & .) in binary strings
def V6Indices(bin_right):
   '''For creation of highlight indices for IPv6 binary strings.
   For a given string length, it returns that length increased
   by the number of separators ":" that will be inserted.
   '''
   if bin_right > 112:
      bin_right += 7
   elif bin_right > 96:
      bin_right += 6
   elif bin_right > 80:
      bin_right += 5
   elif bin_right > 64:
      bin_right += 4
   elif bin_right > 48:
      bin_right += 3
   elif bin_right > 32:
      bin_right += 2
   elif bin_right > 16:
      bin_right += 1
   return bin_right

def V4Indices(bin_right):
   '''For creation of highlight indices for IPv4 binary strings.
   For a given string length, it returns that length increased
   by the number of separators "." that will be inserted.
   '''

   if bin_right >= 24:
      bin_right += 3
   elif bin_right >= 16:
      bin_right += 2
   elif bin_right >= 8:
      bin_right += 1
   return bin_right

def advance(element):
   '''Move focus to input field, select all, move cursor to end'''
   focus = '''
element_in = window[element]
element_in.set_focus()
element_in.Widget.icursor('end')
'''
   exec(focus)
   return

# Input validation and create IP prefix objects
#-----------------------------------------------#
def validate(param_ls):
   '''Validates input parameters using ipaddress module to create
   required IP prefix object variables. Then tests results for
   compatibility with MAP-T.
   '''
   # param_ls = [name, v6p, v6len, v4p, v4len, eal, psol]
   validflag = 'fail'
   v6p = param_ls[1]
   v6pl = param_ls[2]
   v4p = param_ls[3]
   v4pl = int(param_ls[4])
   eal = int(param_ls[5])
   psofst_len = int(param_ls[6])
   psid_len = eal - (32 - v4pl)

   # test IPv6 prefix/mask
   try:
      v6p_out = ip.ip_network('/'.join((v6p, str(v6pl))))
      validflag = 'pass'
   except:
      advance('-R6PRE-')
      window['-PARAM_MESSAGES-'].update(
         f'IPv6 {v6p}/{v6pl} not valid. Host bits set?')
      window['-PARAM_MESSAGES-'].update(
         f'IPv6 {v6p}/{v6pl} not valid. Host bits set?')
      return(validflag)

   # test IPv4 prefix/mask
   try:
      v4pfx_val = ip.ip_network('/'.join((v4p, str(v4pl))))
      v4pfx_bits = f'{ip.IPv4Address(v4p):b}'[:v4pl]
      v4pfx_bin = f'{v4pfx_bits:<032s}'
      v4pfx_int = int(v4pfx_bin, 2)
      v4pfx = ip.ip_address(v4pfx_int)
   except ValueError:
      validflag = 'fail'
      window['-PARAM_MESSAGES-'].update(
         f'IPv4 {v4p}/{v4pl} not valid. Host bits set?')
      window['-PARAM_MESSAGES-'].update(
         f'IPv4 {v4p}/{v4pl} not valid. Host bits set?')
      return(validflag)
 
   # Validate host bits exist
   if v4pfx_val.prefixlen > 31: # Valid for ip.ip_network test, but invalid for MAP-T
      validflag = 'fail'
      window['-PARAM_MESSAGES-'].update('IPv4 Host Length = 0, Invalid')
      window['-PARAM_MESSAGES-'].update('IPv4 Host Length = 0, Invalid')
      return(validflag)

   # Validate Rule prefix masks are in acceptable MAP-T Rule ranges
   if int(v6pl) + eal > 64: # v6 prefix length + EA length > 64 not valid for MAP-T
      validflag = 'fail'
      window['-PARAM_MESSAGES-'].update(
         f"IPv6 prefix mask + EA Bits can't exceed 64 bits")
      window['-PARAM_MESSAGES-'].update(
         f"IPv6 prefix mask + EA Bits can't exceed 64 bits")
      return(validflag)

   if eal < (32 - v4pl):  # EA length < v4 host bits (Check RFC)
      validflag = 'fail'
      window['-PARAM_MESSAGES-'].update(
         f"EA Bits can't be less than IPv4 host bits")
      window['-PARAM_MESSAGES-'].update(
         f"EA Bits can't be less than IPv4 host bits")
      return(validflag)

   # validate EA Bits and PSID Offset values are in valid MAP-T Rule range
   # (values not tested with actual BMR!)
   if eal > 48:     # EA length > 48 is invalid, rfc7597 5.2
      validflag = 'fail'
      advance('-EABITS-')
      window['-PARAM_MESSAGES-'].update('EA bits out of range')
      window['-PARAM_MESSAGES-'].update('EA bits out of range')
      return(validflag)
   elif psofst_len > 15:   # PSID offset > 15 = no available ports
      validflag = 'fail'
      window['-PARAM_MESSAGES-'].update('PSID Offset must not exceed 15')
      window['-PARAM_MESSAGES-'].update('PSID Offset must not exceed 15')
      advance('-OFFSET-')
      return(validflag)
      ##### >>>> Check RFC to see if offset > 15 is possible <<<<<
   elif psofst_len + psid_len > 16:
      validflag = 'fail'
      window['-PARAM_MESSAGES-'].update('PSID Offset + PSID Length > 16 bits')
      window['-PARAM_MESSAGES-'].update('PSID Offset + PSID Length > 16 bits')
      return(validflag)

   return validflag # ('pass')

# Path to additional data files
#-------------------------------#
def resource_path(relative_path):
   """ Get absolute path to resource, works for dev and for PyInstaller """
   try:
      # PyInstaller creates a temp folder and stores path in _MEIPASS
      base_path = sys._MEIPASS
   except Exception:
      base_path = os.path.abspath(".")
   return os.path.join(base_path, relative_path)

def transpose(array, array_new):
   """
   Transposes a 2d array (rows to columns).

   Args:
     array: Original 2d array (list of lists).
     array_new: Transposed array.
   """
   # iterate over list array to the length of an item 
   for i in range(len(array[0])):
      row =[]
      for item in array:
         # appending to new list with values and index positions
         # i contains index position and item contains values
         row.append(item[i])
      array_new.append(row)
   return array_new

# Clear DHCPv6 results fields, but not DMR entry field
#------------------------------------------------------#
def clear_dhcp_fields(reset_prompt=True):
   window['OPT_95'].update('')
   window['OPT_89'].update('')
   window['OPT_93'].update('')
   window['OPT_91'].update('')
   if reset_prompt == True:
      window['DMR_INPUT'].update('Ex. 2001:db8:ffff::/64', disabled=True)

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
dframe_ls = ['-USERS_DSPLY-', # '-BMR_STRING_DSPLY-'
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

# Output Fields
#---------------------------------#
outfields_ls = ['MLINE_BINOPS', 'MLINE_PORTS', 'MLINE_IPV4', 'MLINE_PORTIDX',
                'CE_V6_WAN', 'USER_PD', '-SP_INDEX-', # 'BMR_STRING', '-BMR_STRING_DSPLY-'
                '-SP_INT-']

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
last_dmr_entry = None

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
   if event in ('Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
      # Save screen location when closing window
      sg.user_settings_set_entry('-location-', window.current_location())
      break

   # Workaround for tab contents not appearing until cursor is moved off of selected tab
   if event == "TABGROUP":
      window[event].get_previous_focus().set_focus()
      window.refresh()
      # window[event].get_next_focus().set_focus()

   if event == 'About':
      if os.path.isfile('files/about_txt'):
         about_txt_file = resource_path('files/about_txt')
         with open(about_txt_file) as lt:
            abouttxt = lt.read()
         about = sg.popup_scrolled(abouttxt, title='About',
            size=(70, 33), font=('Arial', 14))
      else:
         abouttxt = 'File "files/about_txt" not found.'
         about = sg.popup(abouttxt, title='About', font=('Arial', 14))

   # Clear error message fields on next event
   window['-PARAM_MESSAGES-'].update('')
   window['-PARAM_MESSAGES-'].update('')
   window['-PARAM_MESSAGES-'].update('')
   window['-DHCP_MESSAGES-'].update('')

   # Clear all fields except Save Frame
   if event == 'Clear':
      for i in [*dframe_ls, *pframe_ls]: #, *sframe_ls]:
         window[i].update('')
      window['-V4HOST_SLIDER-'].update(value=0)
      window['-V4HOST_SLIDER-'].update(range=(0, 0))
      window['-V6PFX_LEN_SLDR-'].update(disabled=True)
      window['-EA_LEN_SLDR-'].update(disabled=True)
      window['-V4PFX_LEN_SLDR-'].update(disabled=True)
      window['-PSID_OFST_SLDR-'].update(disabled=True)
      window['-USER_PD-'].update('')
      # window['-USER_IP4-'].update('')
      # window['-USER_PORT-'].update('')
      window['-STRING_IN-'].update('')
      window['-SP_INDEX-'].update('')
      window['-SP_INT-'].update('')
      window['MLINE_BINOPS'].update('')
      window['MLINE_PORTS'].update('')
      window['MLINE_IPV4'].update('')
      window['MLINE_PORTIDX'].update('')
      clear_dhcp_fields()
      window['FMR_FLAG'].update(False)
      last_dmr_entry = None
      userpds = None # delete UserPd() class instance
      examples = None # delete ExampleParams() class instance
      last_params = None
      portidx = 0

   # Load example values in main display and editors
   #-------------------------------------------------#
   if event == 'EXAMPLE':
      portidxadd = 0      # reset port index value
      v4hostint = 0       # reset v4 host integer
      clear_dhcp_fields()
      
      if examples:
         param_ls = examples.new_params()
      else:
         examples = ExampleParams()
         param_ls = examples.new_params()

      last_params = param_ls
      userpds = UserPd(param_ls)
      user_pd = userpds.new_pd()
      rule_calc(param_ls, user_pd, v4hostint)
      window['-V4HOST_SLIDER-'].update(value=0)
      window['DMR_INPUT'].update('Ex. 2001:db8:ffff::/64')

   # BMR parameter entry - validate input as it is typed
   #-----------------------------------------------------#
   if event == '-RULENAME-' and values[event]:
      if values[event][-1] not in chars:
         window[event].update(values[event][:-1])
         window['-PARAM_MESSAGES-'].update('Invalid character')
      elif len(str(values['-RULENAME-'])) > 20:
         window[event].update(values[event][:-1])
         window['-PARAM_MESSAGES-'].update('Max Name length')

   if event == '-R6PRE-' and values['-R6PRE-']:
      if values['-R6PRE-'][-1] not in v6chars \
         or len(values['-R6PRE-']) > 21:
         # Delete last character entered
         window[event].update(values[event][:-1])
         window['-PARAM_MESSAGES-'].update('Bad character or too long')

   if event == '-R4PRE-' and values['-R4PRE-']:
      if values['-R4PRE-'][-1] not in v4chars \
         or len(values['-R4PRE-']) > 15:
         window[event].update(values[event][:-1])
         window['-PARAM_MESSAGES-'].update('Bad character or too long')

   # Enter new BMR
   #---------------#
   if event == '-ENTER_PARAMS-':
      portidxadd = 0      # reset port index value
      valid = 'not set'
      for p in pframe_ls:
         if p == '-OFFSET-' and values[p] == 0:
            allow = 'yes'
         elif not values[p]:
               window['-PARAM_MESSAGES-'].update(f'Missing Parameter')
               # advance(p)
               allow = 'no'
               break
         else:
            allow = 'yes'
      if allow == 'yes':
         param_ls = [values[p] for p in pframe_ls]
         for i, element in enumerate(param_ls):
            if i in [2, 4, 5, 6]:
               param_ls[i] = int(param_ls[i])
         if param_ls == last_params:
            window['-PARAM_MESSAGES-'].update('No change') # ->> Add "only name changed" scenario???
         else:
            valid = validate(param_ls)
            if valid == 'pass':
               last_params = param_ls # Used for UserPd() to decide next PD vs. new PD
               userpds = UserPd(param_ls)
               user_pd = userpds.new_pd()
               rule_calc(param_ls, user_pd)
            else:
               print('PARAMETER ENTRY ERROR')

   # Validate Enter/Edit String
   # Values in allowable ranges. But not tested that they work in BMR!
   #-------------------------------------------------------------------#
   # Rule String Enter button pressed or Return key pressed in Rule String Field
   if event == '-ENTER_STRING-' or event == '-STRING_IN-' + '_Enter':
      portidxadd = 0      # reset port index setting
      valid = 'not set'
      goodstring = True
      if not values['-STRING_IN-']:
         window['-STRING_IN-'].update('Enter rule string')
         window['-PARAM_MESSAGES-'].update('Missing Rule String')
         advance('-STRING_IN-')
      # Remove extra information (space and everything following)
      elif ' (' in values['-STRING_IN-']:
         space_idx = values['-STRING_IN-'].index(' ')
         values['-STRING_IN-'] = values['-STRING_IN-'][:space_idx]
         window['-STRING_IN-'].update(values['-STRING_IN-'])
         window['-ENTER_STRING-'].click() # "Re-click" String Enter button
      elif len(values['-STRING_IN-']) > 69: # or delete characters >69 during entry (above)
         window['-STRING_IN-'].update('Rule string too long')
      else:
         input_str = values['-STRING_IN-']
         # New param list values. Validate strings and numeric entries.
         param_ls = input_str.split('|')
         if len(param_ls) != 7:
            window['-PARAM_MESSAGES-'].update('Enter valid rule string'),
            advance('-STRING_IN-')
         else:
            for i, element in enumerate(param_ls):
               if i in [2, 4, 5, 6]:
                  try:
                     param_ls[i] = int(param_ls[i])
                  except ValueError:
                     window['-PARAM_MESSAGES-'].update('Incorrect digit entry. View example.')
                     advance('-STRING_IN-')
                     goodstring = False
            if goodstring:
               if param_ls == last_params:
                  window['-PARAM_MESSAGES-'].update('No change') # ---->> Add "only name changed" scenario???
               else:
                  valid = validate(param_ls)
                  if valid == 'pass':
                     last_params = param_ls # Used for UserPd() to decide next PD vs. new PD
                     userpds = UserPd(param_ls)
                     user_pd = userpds.new_pd()

                     rule_calc(param_ls, user_pd)

                  else:
                     print('RULE STRING ERROR')
            else:
               pass

   # Update binary editor values and highlights
   #--------------------------------------------#
   if event.endswith('SLDR-') and last_params: # rule to edit must exist
      portidxadd = 0
      print(f'last_params is {last_params}')
      param_ls = [
         param_ls[0],
         param_ls[1],
         int(values['-V6PFX_LEN_SLDR-']),
         param_ls[3],
         int(values['-V4PFX_LEN_SLDR-']),
         int(values['-EA_LEN_SLDR-']),
         int(values['-PSID_OFST_SLDR-'])
      ]

      valid = validate(param_ls)

      if valid == 'pass':
         last_params = param_ls # Used by UserPd() to decide next PD vs. new PD
         userpds = UserPd(param_ls)
         user_pd = userpds.new_pd()
         rule_calc(param_ls, user_pd)
      else:
         param_ls = last_params
         # print('SLIDER ERROR')

   # Display next User Delegated Prefix (PD)
   #-----------------------------------------#
   if event == '-NXT_USER_PD-' and last_params:
      # If last_params=None (initial state or Clear was used) ignore button
      portidxadd = 0
      user_pd = userpds.new_pd()
#     v4hostint = int(values['-V4HOST_SLIDER-']) # slider values are floats
      rule_calc(last_params, user_pd, v4hostint)
      if last_dmr_entry:
         window['DMR_INPUT'].update(last_dmr_entry)
         dhcp_calc(last_dmr_entry, values['FMR_FLAG'])

   # Increment IPv4 host address
   #-----------------------------------------#
   # Host slider initialized with range=0,0. It can't be incremented when range=0
   # Range is updated when valid BMR parameters are Entered
   # Range is reset to 0,0 when "Clear" is used
   if event == '-V4HOST_SLIDER-': # ---- May be able to use ip.addr + v4host_slider ----
      portidxadd = 0
      v4hostint = int(values['-V4HOST_SLIDER-']) # slider values are floats
      rule_calc(last_params, user_pd, v4hostint)
   # If last_params=None (initial state or Clear was used) ignore button
   elif event == '-NEXT_HOST-' and last_params: # +1 button
      maxhost = (2 ** (32 - values["-R4LEN-"])) -1
      if last_params and values['-V4HOST_SLIDER-'] < maxhost:
         v4hostint = int(values['-V4HOST_SLIDER-']) + 1 # slider values are floats
         window['-V4HOST_SLIDER-'].update(value=v4hostint)
         rule_calc(last_params, user_pd, v4hostint)

   # Display user source port numbers
   #-----------------------------------------#
   if 'IDX' in event and last_params:
      match event:
         case '-P_IDX_FIRST-':
            portidxadd = 0
            idx = 0
         case '-P_IDX_UP_1-':
            idx = 1
         case '-P_IDX_UP_10-':
            idx = 10
         case '-P_IDX_UP_100-':
            idx = 100
         case '-P_IDX_LAST-':
            idx = 65535
      idx = idx + portidxadd
      portidxadd = idx
      if portidxadd > 65535: # 16 bit port field max value is 65535
         portidxadd = 65535 # Prevent possibility of infinite growth
      v4hostint = int(values['-V4HOST_SLIDER-'])
      rule_calc(last_params, user_pd, v4hostint, portidx = idx)

   # Save Current BMR in bottom Multiline field for user to copy
   # Only BMR parameter list section needs to be entered
   #-------------------------------------------------------------#
   if event == 'SAVE' and last_params:
      rule = values["-STRING_IN-"]
      name = rule.split('|')
      name = name[0]

      if name in values["-MLINE_SAVED-"]:
         window['-PARAM_MESSAGES-'].update('Duplicate Rule Name')
      elif rule[rule.index('|'):] in values["-MLINE_SAVED-"]:
         window['-PARAM_MESSAGES-'].update('Duplicate Rule')
      else:
         savstr = f'{values["-STRING_IN-"]} ' \
                  f'(IPs-{window["-IPS_DSPLY-"].get()}, ' \
                  f'SHR-{window["-RATIO_DSPLY-"].get()}, ' \
                  f'USRS-{window["-USERS_DSPLY-"].get()}, ' \
                  f'PTS-{window["-PORTS_DSPLY-"].get()}, ' \
                  f'XPTS-{window["-EXCL_PORTS_DSPLY-"].get()})\n'

         if savctr == True:
            window['-MLINE_SAVED-'].update(savstr, append=True)
         else:
            window['-MLINE_SAVED-'].update(savstr)
            savctr = True

   elif event == '-SAVE-':
      window['-PARAM_MESSAGES-'].update('Enter Rule')

   # DHCPv6 operations
   #-------------------------------------------------------------#
   # Disable section until valid BMR is entered
   if last_params:
      if event == 'DMR_INPUT_FOCUS':
         window['DMR_INPUT'].update(disabled=False)
         if not values['OPT_95']:
            if values['DMR_INPUT'] == 'Ex. 2001:db8:ffff::/64':
               window['DMR_INPUT'].update('')
            # else:
            #    window['DMR_INPUT'].update(bad_value) # No bad_value yet

      if event == 'DMR_ENTER' or event == 'DMR_INPUT' + '_Enter':
         try:
            dmr_obj = ip.ip_network(values['DMR_INPUT'])
         except ValueError as ve:
            window['-DHCP_MESSAGES-'].update(f"'{values['DMR_INPUT']}' is not a valid IPv6 network")
            bad_value = values['DMR_INPUT']
            clear_dhcp_fields(reset_prompt=False)
         except Exception as e:
            errname = type(e).__name__
            window['-DHCP_MESSAGES-'].update(f'{errname}: {e}')
            bad_value = values['DMR_INPUT']
            clear_dhcp_fields(reset_prompt=False)
         else:
            bad_value = None
            if values['FMR_FLAG'] == True:
               dhcp_calc(values['DMR_INPUT'], fmr=True)
               last_dmr_entry = values['DMR_INPUT']
               last_fmr_flag = values['FMR_FLAG']
            else:
               dhcp_calc(values['DMR_INPUT'], fmr=False)
               last_dmr_entry = values['DMR_INPUT']
               last_fmr_flag = values['FMR_FLAG']

      # Move focus out of DMR_INPUT to reset for next DMR_INPUT_FOCUS event
      if event == 'DMR_INPUT' + '_Enter':
         window['DMR_ENTER'].set_focus()

      # FMR checkbox changes option string to FMR without re-clicking DMR Enter Button
      if event == 'FMR_FLAG' and values['OPT_95']:
         if values['FMR_FLAG'] != last_fmr_flag:
            window['OPT_95'].update('')
            window['OPT_89'].update('')
            window.read(timeout=50)
            last_fmr_flag = values['FMR_FLAG']
            window['DMR_INPUT'].update(last_dmr_entry)
            dhcp_calc(last_dmr_entry, values['FMR_FLAG'])

   foc_elmt = window.find_element_with_focus()


   print(f'#------- End Event {cntr - 1} -------#')

   print(window.size)



   '''
   TODO:
    - Add example text to all input fields at start (One is DMR in DHCP Options)
    - Add Name input if Enter clicked with no name
    - Look at moving parameter sliders out of tabbed frame - DONE 12/6/24
    - Change eabits var to ealen (also related keys)
    - Change all multiline fields with highlighted text to white background

   # Utilities:
   #----------------------------------------#

   # This prints all available element keys:
   #----------------------------------------#
   print('\n ---- VALUES KEYS ----')
   for x in values.keys():
      print(x)

   # This prints all variables:
   #----------------------------------------#
   print(dir())
   '''

window.close()