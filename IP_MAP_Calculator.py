#!/usr/bin/env python3
import PySimpleGUI as sg
import ipaddress as ip
import os
import sys

'''
██    ██ ██     ██       █████  ██    ██  ██████  ██    ██ ████████ ███████ 
██    ██ ██     ██      ██   ██  ██  ██  ██    ██ ██    ██    ██    ██      
██    ██ ██     ██      ███████   ████   ██    ██ ██    ██    ██    ███████ 
██    ██ ██     ██      ██   ██    ██    ██    ██ ██    ██    ██         ██ 
 ██████  ██     ███████ ██   ██    ██     ██████   ██████     ██    ███████ 
'''

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

# Combo control values for BMR Rule enter and edit
v4mask = [n for n in range(16, 33)]
v6mask = [n for n in range(32, 65)]
psidoff = [n for n in range(16)]
eabits = [n for n in range(33)]

# Main Display - Domain Results Fields
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

# Main Display - Domain Results Frame
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

# Main Display - BMR Parameters Entry Frame
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
   [sg.Sizer(v_pixels=2)],
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


# Tabbed Frames Layouts
#===========================================================================#

# BMR Binary Operations Tab
#---------------------------------------------------------------------------#
bmr_binops_section = [
    [sg.Multiline("BMR and User PD prefixes", size=(83, 7),
        pad=((4, 4), (4, 0)), font=('Courier', 12, 'bold'),
        background_color='#f1eee7', expand_x=True, disabled=True, # horizontal_scroll = True,
        border_width=2, no_scrollbar=True, key='MLINE_BINOPS') 
    ],
    [sg.Sizer(v_pixels=4)],
    [sg.Sizer(h_pixels=63),
    sg.Text('IPv6 User PD:', font=(None, 11, 'bold'), pad=((4, 0), (2, 4))),
    sg.Input('', size=(30, 1), font=('Courier', 12), justification='centered',
        disabled=True, disabled_readonly_background_color='#fdfdfc',
        pad=((0, 4), (4, 4)), key="-USER_PD-"),
    sg.Button('First', font='None 8 bold', pad=((4, 0), (4, 4)), key='FIRST_USER_PD'),
    sg.Button('Next', font='None 8 bold', pad=((3, 0), (4, 4)),
        key='NEXT_USER_PD'),
    sg.Button('Last', font='None 8 bold', pad=((3, 4), (4, 4)), key='LAST_USER_PD'),
    sg.Text('', text_color='red', font='None 12 bold', key='PD_MESSAGES'),
    # sg.Text('(Changes PSID)', font=(None, 11, 'italic'),
    #   pad=((3, 3), (0, 4))),
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
    sg.Button(' + 1', font='None 8 bold', pad=((2, 5), (12, 0)),
      key='-NEXT_HOST-'),
    sg.Push()
   ],
   [sg.Sizer(v_pixels=4)],
]

port_idx_section = [
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

bmr_binops_tab = [
    [sg.Frame("", [
        [sg.Sizer(v_pixels=3)],
        [sg.Text(('Bit analysis performed by CE, to determine its allocated '
                'IPv4 host addresses and ports'),
       font='None 12 bold', text_color='white', background_color="#8399C4",
       justification='centered', 
       border_width=0, relief='raised', pad=0, expand_x=True)],],
       expand_x=True, background_color='#8399C4', border_width=0)
    ],
    [sg.Sizer(v_pixels=4)],
    [sg.Frame("", bmr_binops_section, font='None 11 bold italic',
        title_location=sg.TITLE_LOCATION_TOP_LEFT, expand_x=True, border_width=2,
        relief='raised', pad=((4, 4), (0, 4)))],
    [sg.Frame("", ipv4_section, font='None 11 bold italic',
        title_location=sg.TITLE_LOCATION_TOP_LEFT, expand_x=True, border_width=2,
        relief="raised", pad=((4, 4), (0, 4)))
    ],
    [sg.Frame("", port_idx_section,
        font='None 11 bold italic', title_location=sg.TITLE_LOCATION_TOP_LEFT,
        expand_x=True, border_width=2, relief='raised', pad=((4, 4), (0, 4)))
    ],
]

# User Ports Tab
#---------------------------------------------------------------------------#
user_ports = [
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

user_ports_tab = [
   [sg.Sizer(v_pixels=3)],
   [sg.Text("All ports for current PSID ",
      font=(None, 12, 'bold'), text_color='white', expand_x=True,
      justification='centered', background_color='#8399C4',)],
   [sg.Sizer(v_pixels=3)],
   [sg.Frame("", user_ports, expand_x=True, border_width=2,
      relief='raised')],
   [sg.Sizer(v_pixels=6)],
   [sg.Sizer(v_pixels=4)],
]

# DHCP Tab
#---------------------------------------------------------------------------#
dhcp_fields = [
   [sg.Sizer(0, 6),],
   [sg.Text('DMR', font=(None, 11, 'bold'), pad=((4, 0), (3, 0)) ),
    sg.Input('Ex. 2001:db8:ffff::/64', size=(25, 1), font=('Courier', 12),
      justification='centered', background_color='#fdfdfc', 
      disabled_readonly_background_color='#fdfdfc', pad=((0, 0), (4, 0)),
      disabled=True, key='DMR_INPUT'),
    sg.Button('Enter', font='None 8 bold', key='DMR_ENTER')],
   # OPTION_S46_CONT_MAPT (95)
   [sg.Text('S46 MAP-T Container Option 95:', font=(None, 11, 'bold')),
    sg.Checkbox('Make FMR String', font=(None, 11, 'bold'), #tooltip=fmr_tooltip,
      enable_events=True, tooltip=fmr_tooltip, key='FMR_FLAG'),
    sg.Text('', text_color='red', font='None 11 bold', key='-DHCP_MESSAGES-')],
   # [sg.Sizer(0, 0),

    # sg.Input('', size=(93, 1), font=('Courier', 11), justification='left',
    #   disabled=True, use_readonly_for_disable=True,
    #   disabled_readonly_background_color='#fdfdfc', key='OPT_95')],

   [sg.Multiline( # ...Using Multiline to get disabled copy/paste - review need for this
         '',
         size=(93, 1), # size=(83,
         # border_width=2,
         pad=((3, 4), (0, 4)),
         # auto_size_text=True,
         font=('Courier', 12),
         justification='left',
         background_color='#fdfdfc',
         # expand_x=True,
         horizontal_scroll = False,
         disabled=True,
         no_scrollbar=True,
         key='OPT_95')],

   # OPTION_S46_RULE (89)
   [sg.Text(f'Option 89', font=(None, 11, 'bold')),
    # sg.Input('', size=(55, 1), font=('Courier', 12), justification='centered',
    #   disabled=True, use_readonly_for_disable=True,
    #   disabled_readonly_background_color='#fdfdfc', key='OPT_89')], # OPTION_S46_RULE (89)
    sg.Multiline(
         '',
         size=(55, 1), # size=(83,
         # border_width=2,
         # pad=4,
         # auto_size_text=True,
         font=('Courier', 12),
         justification='left',
         background_color='#fdfdfc',
         # expand_x=True,
         horizontal_scroll = False,
         disabled=True,
         no_scrollbar=True,
         key='OPT_89'),
    sg.Text('S46 Rule Option', font=(None, 11))],

   # OPTION_S46_PORTPARAMS (93)
   [sg.Text('Option 93', justification='centered', font=(None, 11, 'bold')),
    sg.Multiline(
         '',
         size=(45, 1), # size=(83,
         # border_width=2,
         # pad=4,
         # auto_size_text=True,
         font=('Courier', 12),
         justification='left',
         background_color='#fdfdfc',
         # expand_x=True,
         horizontal_scroll = False,
         disabled=True,
         no_scrollbar=True,
         key='OPT_93'),
    sg.Text('S46 Port Parameters Option (no PSID data)', font=(None, 11))],

   # OPTION_S46_DMR (91)
   [sg.Text('Option 91', justification='centered', font=(None, 11, 'bold')),
    sg.Multiline(
         '',
         size=(45, 1), # size=(83,
         # border_width=2,
         pad=((7, 4), (4, 4)),
         # auto_size_text=True,
         font=('Courier', 12),
         justification='left',
         background_color='#fdfdfc',
         # expand_x=True,
         horizontal_scroll = False,
         disabled=True,
         no_scrollbar=True,
         key='OPT_91'),
    sg.Text('S46 DMR Option', font=(None, 11))],

   [sg.Sizer(v_pixels=6)],
]

dhcp_tab_layout = [
   [sg.Sizer(v_pixels=3)],
   [sg.Text("Softwire 46 MAP-T Options for DHCPv6", font=(None, 12, 'bold'),
      text_color='white', background_color='#8399C4', expand_x=True,
      justification='centered')],
   [sg.Frame("", dhcp_fields, expand_x=True, border_width=2, relief='raised')]
]

# Saved BMR Rules Tab
#---------------------------------------------------------------------------#
saved_rules =[
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
    sg.Text("Saved BMR Strings", font=(None, 12, 'bold'), text_color='white',
      background_color='#8399C4', justification='centered'),
    sg.Text("(To enter in 'BMR String' field)", font=(None, 12, 'italic'),
       text_color='white', background_color='#8399C4', justification='centered'),
    sg.Push( background_color='#8399C4')],
   [sg.Frame("", saved_rules, p=4, expand_x=True, border_width=2,
      relief='raised')],
   [sg.Sizer(v_pixels=6)],
]

# Tab Group Main Layout
#---------------------------------------------------------------------------#
tab_group_layout = [
    [sg.Tab('Binary Operations', bmr_binops_tab, background_color='#8399C4',
        key='TAB_BINARY'),
     # # image_source=binops_tab_label, key='TAB_BINARY'),
     # # sg.Tab('User PD', user_pd_tab_layout, key='TAB_UPD'),
     sg.Tab('User Ports', user_ports_tab,  background_color='#8399C4',
        key='TAB_PORTS'),
     sg.Tab('DHCP Options', dhcp_tab_layout, background_color='#8399C4',
        key='TAB_DHCP'),
     sg.Tab('Saved Rules', saved_rules_tab_layout, background_color='#8399C4',
        key='TAB_SAVED')]
]

# Main Layout
layout = [
   [sg.Sizer(v_pixels=4)],
   [sg.Frame("", display_layout, element_justification='centered',
      expand_x=True, border_width=4)],
   [sg.Frame("Enter or Edit BMR Parameters", editor_layout,
      font=(None, 12, 'bold'), title_location=sg.TITLE_LOCATION_TOP,
      border_width=4, expand_x=True,)],
   [sg.TabGroup(tab_group_layout, enable_events=True, border_width=1,
      tab_background_color='#C8D1E5', selected_background_color='#8399C4',
      title_color='black', selected_title_color='white', tab_border_width=2,
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

# Create Main Window
#------------------------------------------------------------------#
# Window uses last screen location for next start
# Location is set upon Exit or WINDOW_CLOSE... event
window = sg.Window('IP MAP Calculator', layout, font=windowfont,
   enable_close_attempted_event=True,
   location=sg.user_settings_get_entry('-location-', (None, None)),
   keep_on_top=False, resizable=True, finalize=True)

'''
██████  ███    ███ ██████       ██████  █████  ██       ██████ 
██   ██ ████  ████ ██   ██     ██      ██   ██ ██      ██      
██████  ██ ████ ██ ██████      ██      ███████ ██      ██      
██   ██ ██  ██  ██ ██   ██     ██      ██   ██ ██      ██      
██████  ██      ██ ██   ██      ██████ ██   ██ ███████  ██████ 
'''                                                               

class Calc:
    '''
    Display basic MAP-T domain results
    '''
    def __init__(self, param_ls): #, user_pd_obj):
        self.params = param_ls
        # self.last_params = None
        # self.user_pd_obj = None
        self.hostnum = 0
        self.last_pd_obj = None
        self.v4hostbin_len: int = None
        self.bmrpfx_len: int = self.params[2]

    # def base_values(self):
    def display_values(self):
        # self.last_params = self.params
        self.v4hostbin_len: int = 32 - self.params[4]
        self.psidlen: int = (self.params[5] - self.v4hostbin_len) # ea_len - host_len
        # self.upd_len: int = self.params[2] + self.params[5]

        v4_ips: int = 2 ** self.v4hostbin_len # 2 ^ number of host_bits
        sharing: int = 2 ** self.psidlen # num of unique psids per v4-host address
        # users = (2 ** self.[v4hostbin_len]) * (2 ** psidlen)
        users: int = v4_ips * sharing

        # Ports per user = 2^(16 - k) - 2^m (per rfc7597)
        # 2^m is # of excluded ports. 16 is the number of IP port bits (constant)
        if self.params[6] > 0: # Because PSID Offset > 0 excludes some ports
            ppusr: int = ((2 ** (16 - self.psidlen))
                - (2 ** (16 - self.psidlen - self.params[6])))
        else:
            ppusr: int = (2 ** (16 - self.psidlen))

        excl_ports: int = 65536 - ((2 ** self.psidlen) * (ppusr))
        bmr_str: str = '|'.join([str(x) for x in self.params])

        result_vals = (
            v4_ips,
            sharing,
            users,
            ppusr,
            excl_ports,
            bmr_str,
            # upd_str
        )

        return result_vals

    # def binary_ops(self, v4host=None):
    #     # User Delegated IPv6 Prefix .........Maybe move
    #     upd_obj = self.user_pd()
    #     upd_str: str = upd_obj



    #-------------------------------------------------------------------------#
    # Binary display strings
    #-------------------------------------------------------------------------#
    # BMR PD, User PD, IPv4, and IP Port binary data
    # BMR PD, User PD, and EA Bits
    #--------------------------------------------------#
    # def binary_ops(self, v4host=None):
    def binary_ops(self):
        v6p_hex_exp = ip.IPv6Address(self.params[1]).exploded # Hex style: 0000:0000:...
        v6p_hex_seglst = v6p_hex_exp.split(':')[:4] # ['0000', '0000', ...]
        # print(v6p_hex_seglst)
        upd_hex_exp = ip.IPv6Address(user_pd_obj.network_address).exploded # 0000:0000:...
        upd_hex_seglst = upd_hex_exp.split(':')[:4] # ['0000', '0000', ...]

        # print(f"upd_hex_seglst is {upd_hex_seglst}") #.................PRINT

        v6p_bin = f'{ip.IPv6Address(self.params[1]):b}'[:64] # first 64 bits of pfx
        v6p_bin_seglst = [v6p_bin[i:i+16] for i in range(0, 64, 16)]
        v6p_bin_fmt = ':'.join(v6p_bin_seglst) + f'::/{self.bmrpfx_len}'
        upd_bin = f'{ip.IPv6Address(user_pd_obj.network_address):b}'[:64]
        upd_bin_seglst = [upd_bin[i:i+16] for i in range(0, 64, 16)]
        upd_bin_fmt = ':'.join(upd_bin_seglst) + f'::/{upd_len}'
        ea_bin_idxl = V6Indices(self.params[2]) # V6Indices adds # of ":"separators
        ea_bin_idxr = V6Indices(upd_len)
        ea_bin_fmt = upd_bin_fmt[ea_bin_idxl : ea_bin_idxr]

        # User PD (upd) string data
        #-----------------------------------#
        psid_idxl = self.params[2] + self.v4hostbin_len
        psid_idxr = self.params[2] + self.params[5]
        psid = upd_bin[psid_idxl : psid_idxr]

        # print(f"psid is {psid}") #.............................PRINT

        # Generate 16 bit string for Port number
        # is PSID Offset > 0?
        if self.params[6] > 0:
            psid_ofst_bin = bin(1)[2:].zfill(self.params[6]) # binary 1 with len = offset
        else:
            psid_ofst_bin = ''
        portrpad_bin = '0' * (16 - self.params[6] - psidlen) # MAY NEED TO ACCEPT EDITOR VALUES !!!
        port_bin = psid_ofst_bin + \
                   psid + \
                   portrpad_bin
        port_int = str(int(port_bin, 2))
        pidx_bin = psid_ofst_bin + portrpad_bin # Port index number binary string

        # IPv4 string data
        #-----------------------------------#
        v4_seglst = v4str.split('.')
        v4mask = self.params[4]
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

        # Modify Port string if Port Index (portidx) has been changed
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
                           f"      ::/{self.bmrpfx_len}"),
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







######### v4 host slider ##########

        # If call is from the host slider, update the upd with host bits
        # and update v4pfx value in param_ls
        if v4host != None:
            pdbin = f'{user_pd_obj.network_address:b}'
            # User PD bits up to BMR prefix length
            pdbin_l = pdbin[:param_ls[2]]
            # User PD bits from after IPv4 host bits to end
            pdbin_r = pdbin[param_ls[2] + (32 - last_params[4]) : ]
            v4hostbin = bin(v4host)[2:].zfill(self.v4hostbin_len)
            newpdbin = pdbin_l + v4hostbin + pdbin_r
            newpdint = int(newpdbin, 2)
            new_upd_pfx_str = \
               ip.IPv6Address(newpdint).compressed + '/' + str(user_pd_obj.prefixlen)
            user_pd_obj = ip.IPv6Network(new_upd_pfx_str)
            # BMR IPv4 bits to prefix len
            v4pfxbin = f'{ip.IPv4Address(param_ls[3]):b}'[: int(param_ls[4])]
            newv4bin = v4pfxbin + v4hostbin
            newv4int = int(newv4bin, 2)
            newv4add = ip.IPv4Address(newv4int)
            # print(f"ipv4 newv4add is {newv4add}, type is {type(newv4add)}")
            v4str = newv4add.compressed
            # print(f"v4str is {v4str}, type is {type(v4str)}")
        else:
            v4pfxbin = f'{ip.IPv4Address(param_ls[3]):b}'
            v4hostbin = f'{user_pd_obj.network_address:b}]'[self.bmrpfx_len : self.bmrpfx_len + (self.v4hostbin_len)]
        #    v4hostint = int(v4hostbin, 2)
            newv4bin = v4pfxbin[:param_ls[4]] + v4hostbin
        #    # window['-V4HOST_SLIDER-'].update(value=0)
            newv4add = ip.IPv4Address(int(newv4bin, 2))
            v4str = newv4add.compressed
        #    window['-V4HOST_SLIDER-'].update(v4hostint)
            # print(f">>>>>in 'else', v4str is {v4str}")

###################################



        # result_vals = [
        #    upd_str
        # ]




    def user_pd(self):
        if self.last_pd_obj:
            pd = next(last_pd_obj)
            self.last_pd_obj = pd
            return pd
        else:
            bmr_v6p = ip.ip_network('/'.join((self.params[1], str(self.params[2]))))
            upd_len: int = self.params[2] + self.params[5]
            pd_obj = bmr_v6p.subnets(new_prefix = upd_len)
            pd = next(pd_obj)
            self.last_pd_obj = pd
            return pd

    def v4_host(self):
        ...

'''
██████  ██ ███████ ██████  ██       █████  ██    ██ ███████ 
██   ██ ██ ██      ██   ██ ██      ██   ██  ██  ██  ██      
██   ██ ██ ███████ ██████  ██      ███████   ████   ███████ 
██   ██ ██      ██ ██      ██      ██   ██    ██         ██ 
██████  ██ ███████ ██      ███████ ██   ██    ██    ███████ 
'''

# MAP-T Domain Result fields
domain_fields = (
    '-IPS_DSPLY-',
    '-RATIO_DSPLY-',
    '-USERS_DSPLY-',
    '-PORTS_DSPLY-',
    '-EXCL_PORTS_DSPLY-',
    '-STRING_IN-'
)

# BMR Parameter Entry Fields
bmr_fields = (
    '-RULENAME-',
    '-R6PRE-',
    '-R6LEN-',
    '-R4PRE-',
    '-R4LEN-',
    '-EABITS-',
    '-OFFSET-'
)

# BMR Parameter Entry Sliders
slider_keys = (
    '-V6PFX_LEN_SLDR-',
    '-EA_LEN_SLDR-',
    '-V4PFX_LEN_SLDR-',
    '-PSID_OFST_SLDR-'
)

def domain_display(params, bmr_results): #......................Handle '-STRING_IN-' separately?
    # Display MAP-T Domain parameter results
    for x, y in zip(domain_fields, bmr_results):
        window[x].update(y)

    # Enable binary editor sliders
    window['-V6PFX_LEN_SLDR-'].update(disabled=False)
    window['-EA_LEN_SLDR-'].update(disabled=False)
    window['-V4PFX_LEN_SLDR-'].update(disabled=False)
    window['-PSID_OFST_SLDR-'].update(disabled=False)

    # Update binary editor sliders with new values
    slider_vals = (params[2], params[5], params[4], params[6])
    for x, y in zip(slider_keys, slider_vals):
        window[x].update(y)

    # Display new BMR parameters in entry fields
    for x, y in zip(bmr_fields, params):
        window[x].update(y)


# Example BMR prefix lists and parameters ......Incorporate into Calc()?
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
# (Moved to DISPLAYS section)

# Event Loop Variables
#----------------------------------#
chars = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789().'
v6chars = '0123456789abcdefABCDEF:'
v4chars = '0123456789.'
examples = None
userpds = None
savctr = False
portidxadd = 0 # used with 'Source Port Index n = Port' section
last_params = None
last_dmr_entry = None
param_ls = []

##-------Event Loop-------##
cntr = 1  # Event counter
while True:
    event, values = window.read()    # type: (str, dict)
    print(f'\n#--------- Event {str(cntr)} ----------#')
    # print(event, values)
    print(event)
    cntr += 1
    if event in ('Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
        # Save screen location when closing window
        sg.user_settings_set_entry('-location-', window.current_location())
        break

    # Clear error message fields on next event
    window['-PARAM_MESSAGES-'].update('')
    # window['-DHCP_MESSAGES-'].update('')

    # BMR parameter input validation
    #-----------------------------------------------------#
    if event == '-RULENAME-' and values[event]: #.............review validation
        if values[event][-1] not in chars:
            window[event].update(values[event][:-1])
            window['-PARAM_MESSAGES-'].update('Invalid character')
        elif len(str(values['-RULENAME-'])) > 20:
            window[event].update(values[event][:-1])
            window['-PARAM_MESSAGES-'].update('Max Name length')
    
    if event == '-R6PRE-' and values['-R6PRE-']: #............improve validation
        if values['-R6PRE-'][-1] not in v6chars \
            or len(values['-R6PRE-']) > 21:
            # Delete last character entered
            window[event].update(values[event][:-1])
            window['-PARAM_MESSAGES-'].update('Invalid character or too long')
    
    if event == '-R4PRE-' and values['-R4PRE-']: #............improve validation
        if values['-R4PRE-'][-1] not in v4chars \
            or len(values['-R4PRE-']) > 15:
            window[event].update(values[event][:-1])
            window['-PARAM_MESSAGES-'].update('Bad character or too long')

    # Enter new BMR
    #---------------#
    if event == '-ENTER_PARAMS-':
        portidxadd = 0      # reset port index value
        valid = 'not set'
        for p in bmr_fields:
            if p == '-OFFSET-' and values[p] == 0:
                allow = 'yes'
            elif not values[p]:
                window['-PARAM_MESSAGES-'].update(f'Missing Parameter')
                # advance(p)
                allow = 'no'
                break
            else:
                allow = 'yes'

        if allow == 'yes': # ....................Consider moving to "else" above
            param_ls = [values[p] for p in bmr_fields]
            if param_ls == last_params:
                window['-PARAM_MESSAGES-'].update('No change') # ->> Add "only name changed" scenario???
            else:
                valid = validate(param_ls)
                if valid == 'pass':
                    last_params = param_ls
                    # userpds = UserPd(param_ls)
                    # user_pd = userpds.new_pd()
                    # rule_calc(param_ls, user_pd)
                    results = Calc(param_ls)
                    domain_display(param_ls, results.display_values())
                else:
                    param_ls = last_params # Restore param_ls
                    # print('PARAMETER ENTRY ERROR') # or raise error and pop up

   # Update binary editor values and highlights
   #--------------------------------------------#
    if event.endswith('SLDR-') and last_params: # rule to edit must exist
        portidxadd = 0
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
            # userpds = UserPd(param_ls)
            # user_pd = userpds.new_pd()
            # rule_calc(param_ls, user_pd)
            results = Calc(param_ls)
            domain_display(param_ls, results.display_values())
        else:
            param_ls = last_params
            # print('SLIDER ERROR')

    # Load example values in main display and editors
    #-------------------------------------------------#
    if event == 'EXAMPLE':
        portidxadd = 0      # reset port index value
        v4hostint = 0       # reset v4 host integer
        # clear_dhcp_fields()
       
        if examples:
            param_ls = examples.new_params()
        else:
            examples = ExampleParams()
            param_ls = examples.new_params()

        last_params = param_ls
        # userpds = UserPd(param_ls)
        # user_pd = userpds.new_pd()
        # rule_calc(param_ls, user_pd, v4hostint)
        results = Calc(param_ls)
        domain_display(param_ls, results.display_values())
        # print(f"results is {results}, type {(type(results))}")
        # result_vals = results.display_values()
        # print(f"\nresult_vals is {result_vals}\nresult_vals")
        # window['-V4HOST_SLIDER-'].update(value=0)
        # window['DMR_INPUT'].update('Ex. 2001:db8:ffff::/64')

    # Clear all fields except Save Frame
    #-------------------------------------------------#
    if event == 'Clear':
        for i in [*domain_fields, *bmr_fields]:
            window[i].update('')
        # window['-V4HOST_SLIDER-'].update(value=0)
        # window['-V4HOST_SLIDER-'].update(range=(0, 0))
        window['-V6PFX_LEN_SLDR-'].update(disabled=True)
        window['-EA_LEN_SLDR-'].update(disabled=True)
        window['-V4PFX_LEN_SLDR-'].update(disabled=True)
        window['-PSID_OFST_SLDR-'].update(disabled=True)
        window['-USER_PD-'].update('')
        window['CE_V6_WAN'].update("")
        window['-SP_INDEX-'].update("")
        window['-SP_INT-'].update("")
        window['-STRING_IN-'].update('')
        window['MLINE_BINOPS'].update('')
        window['MLINE_PORTS'].update('')
        window['MLINE_IPV4'].update('')
        window['MLINE_PORTIDX'].update('')

        # clear_dhcp_fields()
        window['OPT_95'].update('')
        window['OPT_89'].update('')
        window['OPT_93'].update('')
        window['OPT_91'].update('')
        # window['FMR_FLAG'].update(False)
        # last_dmr_entry = None
        # userpds = None # delete UserPd() class instance
        examples = None # delete ExampleParams() class instance
        last_params = None
        # portidx = 0

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


    # TESTING
    #---------------------------------------------------#
    # if event == 'About':
    #     print(f"results is {results.display_values()}")


    #---------------------------------------------------#


    print(f'#------- End Event {cntr - 1} -------#')


window.close()


'''
TO DO:
 - Change "param_ls" to params
 - Fix selected tab blank until cursor is moved out of tab


'''
