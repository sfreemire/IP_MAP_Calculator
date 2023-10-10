#!/usr/bin/env python
import PySimpleGUI as sg
import ipaddress as ip

'''IP_MAP_Calculator.py: Calculates the results of IP MAP Rule parameters'''

# IP_MAP_ADDRESS_CALCULATOR v0.5.2 - 09/28/2023 - Scott Freemire

# Window theme and frame variables
#-------------------------------------#
sg.theme('TanBlue')
windowfont=('Helvetica', 14)
name_tooltip = 'Enter unique rule name'
v6_tooltip = 'Format similar to 2008:8cd:0::/xx'
v6m_tooltip = 'Enter IPv6 mask bits'
v4_tooltip = 'Format similar to 192.168.2.0/24'
v4m_tooltip = 'Enter IPv4 mask bits'
ea_tooltip = 'Max 2 digits'
#psid_tooltip = 'Max 1 digit'
saved_tooltip = 'Similar to example below'
v4mask = [n for n in range(16, 33)] # for edit rule Combo
v6mask = [n for n in range(32, 65)] # for edit rule Combo
psidoff = [n for n in range(17)]    # for edit rule Combo
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
# expand_x=True causes container element to expand to widest element contained
# expand_y=True causes container element to expand vertically as needed

# Main Display (top frame) - Calculated Values
#----------------------------------------------#
display_col1 = [
   [sg.Text('Users', font=('Arial', 14, 'bold'))],
   [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
    size=(7, 1), background_color='white smoke', border_width=4, relief='ridge',
    key='-USERS_DSPLY-')]
]
display_col2 = [
   [sg.Text('Ports/User', font=('Arial', 14, 'bold'))],
   [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
    size=(7, 1), background_color='white smoke', border_width=4, relief='ridge',
    key='-PORTS_DSPLY-')]
]
display_col3 = [
   [sg.Text('Uniq v4 IPs', font=('Arial', 14, 'bold'))],
   [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
    size=(7, 1), background_color='white smoke', border_width=4, relief='ridge',
    key='-IPS_DSPLY-')]
]
display_col4 = [
   [sg.Text('Sharing', font=('Arial', 14, 'bold'))],
   [sg.Text('', font=('Arial', 16, 'bold'), justification='centered',
    size=(7, 1), background_color='white smoke', border_width=4,
    relief='ridge', key='-RATIO_DSPLY-')]
]

# Top frame with results fields
display_layout = [
   [sg.Column(display_col3, element_justification='centered'),
    sg.Text('x', pad=((0, 0), (20, 0))),
    sg.Column(display_col4, element_justification='centered'),
    sg.Text('=', pad=((0, 0), (20, 0))),
    sg.Column(display_col1, element_justification='centered'),
    sg.Text(':', font=('Arial', 16, 'bold'), pad=((0, 0), (20, 0))),
    sg.Column(display_col2, element_justification='centered')],
   [sg.Text('BMR', font=('Arial', 14, 'bold')),
    sg.Input('', font=('Courier', 15, 'bold'),
   # use_readonly... with disabled creates display field that can be
   # selected and copied with cursor but not edited
    justification='centered', size=(60, 1), use_readonly_for_disable=True,
    disabled=True, pad=((0, 8), (0, 0)),
    key='-BMR_STRING_DSPLY-'),
#    sg.Push(),
    sg.Button('Save', font=('Helvetica', 11), key='-SAVE-')],
   [sg.Push(),
    sg.Text('Select and copy, or click Save', font=('Helvetica', 13, 'italic'),
    justification='centered', pad=((5, 5), (0, 5))),
    sg.Push()],
]

# Parameter Editing Display (2nd frame)
#---------------------------------------#
param_edit_col1 = [
   [sg.Text('Enter or Edit BMR Parameters',
      font=('Helvetica', 14, 'underline', 'bold')),
      sg.Push(),
    sg.Text('', text_color='red', key='-PARAM_MESSAGES-'),
#    sg.Text('', text_color='red', key='-MESSAGES-'),
    sg.Push()],
   [sg.Text('Name:', font=('Arial', 14, 'bold')),
    sg.Input('', font=('Arial', 14, 'bold'), size=(20, 1),
    enable_events=True, tooltip=name_tooltip, border_width=2,
    pad=((89, 5), (5, 5)), key='-RULENAME-'),
    sg.Push()],
    [sg.Text('IPv6 Prefix/Length:', font=('Arial', 14, 'bold')),
    sg.Input('', font=('Arial', 14, 'bold'), size=(20, 1), enable_events=True,
    tooltip=v6_tooltip, border_width=2, key='-R6PRE-'),
    sg.Text('/'),
    sg.Combo(v6mask, readonly=True, font=('Helvetica', 14, 'bold'),
    enable_events=True, key='-R6LEN-')],
   [sg.Text('IPv4 Prefix/Length:', font=('Arial', 14, 'bold')),
    sg.Input('', font=('Arial', 14, 'bold'), size=(20, 1), enable_events=True,
    tooltip=v4_tooltip,  border_width=2, key='-R4PRE-'),
    sg.Text('/'),
    sg.Combo(v4mask, readonly=True, font=('Helvetica', 14, 'bold'),
    enable_events=True, key='-R4LEN-')],
   [sg.Text('EA Bits Length', font=('Arial', 14, 'bold')),
    sg.Sizer(h_pixels=25, v_pixels=0),
    sg.Combo(eabits, readonly=True, font=('Helvetica', 14, 'bold'),
    enable_events=True, key='-EABITS-'),
    sg.Sizer(h_pixels=20, v_pixels=0),
    sg.Text('PSID Offset Bits', font=('Arial', 14, 'bold')),
    sg.Combo(psidoff, readonly=True, font=('Helvetica', 14, 'bold'),
    enable_events=True, key='-OFFSET-'),
    sg.Sizer(h_pixels=202, v_pixels=0),
    sg.Button('Enter', font=('Helvetica', 11), key='-ENTER_PARAMS-')],
   [sg.Sizer(h_pixels=0, v_pixels=5)],
   [sg.HorizontalSeparator()],
   [sg.Sizer(h_pixels=0, v_pixels=5)],
   [sg.Text('Rule String:', font=(None, 14, 'italic', 'bold'),
    pad=((5, 5), (5, 0))),
    sg.Input('', font=('Courier', 14, 'bold'), size=(60, 1),
    justification='centered', pad=((5, 5), (5, 0)), enable_events=True,
    tooltip=saved_tooltip, key='-STRING_IN-'),
    sg.Button('Enter', font='Helvetica 11', pad=((5, 5), (5, 0)),
    key='-ENTER_STRING-')],
   [sg.Push(),
    sg.Text('Edit or paste saved string and Enter', font=('Helvetica', 13, 'italic'),
    justification='centered', pad=((5, 5), (0, 5))),
    sg.Push()]
]

editor_layout = [
   [sg.Column(param_edit_col1, expand_x=True)],
]

# Binary Display (3rd frame)
#-------------------------------------#
# '#faf9f2' is a nice white, similar to default background '#e3dbcf'
bin_display_col1 = [
#   [sg.HorizontalSeparator()],
   [sg.Sizer(h_pixels=0, v_pixels=8)],
   [sg.Push(),
    sg.Text('User PD', font=('Arial', 14, 'bold'), pad=((5, 0), (5, 5))),
    sg.Input('', size=(24, 1), pad=((4, 5), (5, 5)),
    font=('Arial', 14, 'bold'), justification='centered',
    use_readonly_for_disable=True, disabled=True, key='-USER_PD-'),
    sg.Push(),
    sg.Text('CE IP', font=('Arial', 14, 'bold'), pad=((0, 0), (5, 5))),
    sg.Input('', size=(16, 1), font=('Arial', 14, 'bold'),
    pad=((5, 0), (5, 5)), justification='centered',
    use_readonly_for_disable=True, disabled=True, key='-USER_IP4-'),
    sg.Push(),
    sg.Text('Port', font=('Arial', 14, 'bold'), pad=((4, 0), (5, 5))),
    sg.Input('', size=((9), 1), font=('Arial', 14, 'bold'),
    justification='centered', use_readonly_for_disable=True,
    disabled=True, key='-USER_PORT-'),
    sg.Push()],
   [sg.Sizer(h_pixels=0, v_pixels=8)],
   [sg.Multiline(size=(83, 20), auto_size_text=True,
    font=('Courier', 14, 'bold'), background_color='#e3dbcf',
#   enable_events=True,
    expand_x=True, disabled=True, horizontal_scroll = True,
    no_scrollbar=True, key='MLINE_BIN_EDIT')],
   ]

bin_display_col2 = [
   [sg.Text('IPv6\nPrefix Length:', font=('Helvetica', 14, 'bold'),
    pad=((5, 1), (5, 0))),
    sg.Slider(range=(32, 64), default_value=32, orientation='h', 
    disable_number_display=False, enable_events=True,
    size=(16, 8), trough_color='white', font=('Helvetica', 14, 'bold'),
    text_color=None, key='-V6PFX_LEN_SLDR-'),
    sg.VerticalSeparator(),
    sg.Text('EA Length:', font=('Helvetica', 14, 'bold'),
      pad=((5, 0), (5, 0))),
    sg.Sizer(h_pixels=5, v_pixels=0),
    sg.Slider(range=(0, 32), default_value=0, orientation='h',
    disable_number_display=False, enable_events=True,
    size=(16, 8), trough_color='white', font=('Helvetica', 14, 'bold'),
    text_color=None, key='-EA_LEN_SLDR-'),
    sg.Push(),],
   [sg.Text('IPv4\nPrefix Length:', font=('Helvetica', 14, 'bold'),
      pad=((5, 0), (5, 0))),
    sg.Slider(range=(16, 32), default_value=16, orientation='h',
    disable_number_display=False, enable_events=True,
    size=(16, 8), trough_color='white', font=('Helvetica', 14, 'bold'),
    pad=((5, 4), (0, 0)), text_color=None, key='-V4PFX_LEN_SLDR-'),
    sg.Sizer(h_pixels=1),
    sg.VerticalSeparator(),
    sg.Sizer(h_pixels=2),
    sg.Text('PSID\nOffset:', font=('Helvetica', 14, 'bold'),
    pad=((0, 5), (0, 5))),
    sg.Slider(range=(0, 16), default_value=0, orientation='h',
    disable_number_display=False, enable_events=True,
    size=(19, 8), trough_color='white', font=('Helvetica', 14, 'bold'),
    pad=((5, 5), (0, 10)), key='-PSID_OFST_SLDR-'),
    sg.Push()],
   [sg.Text('IPv4 Host:', font=('Helvetica', 14, 'bold')),
    sg.Sizer(h_pixels=20),
    sg.Slider(range=(0, 0), default_value=0, orientation='h',
    disable_number_display=False, enable_events=True,
    size=(42, 8), trough_color='white', font=('Helvetica', 14, 'bold'),
    pad=((5, 10), (0, 10)), key='-V4HOST_SLIDER-'),
    sg.Button(' + 1', font='Helvetica 11', key='-NEXT_HOST-'),
    sg.Push()],
   [sg.Sizer(h_pixels=0, v_pixels=8)],   
   [sg.HorizontalSeparator()],
   [sg.Sizer(h_pixels=0, v_pixels=10)],
   [sg.Text('Source Port Index:', font=('Helvetica', 14, 'bold')),
    sg.Text('', font=('Arial', 14, 'bold'), justification='centered',
    size=(16, 1), background_color='white smoke', border_width=4, relief='ridge',
    key='-SP_INDEX-'),
#    sg.Input('', size=(16, 1), justification='centered',
#    use_readonly_for_disable=True,disabled=True, key='-SP_INDEX-'),
    sg.Button(' <<', font='Helvetica 11', key='-P_IDX_FIRST-'),
    sg.Button(' + 1', font='Helvetica 11', key='-P_IDX_UP1-'),
    sg.Button(' + 10', font='Helvetica 11', key='-P_IDX_UP10-'),
    sg.Button(' + 100', font='Helvetica 11', key='-P_IDX_UP100-'),
    sg.Button(' >>', font='Helvetica 11', key='-P_IDX_LAST-'),
    sg.Text(f'= Port', font=('Helvetica', 14, 'bold')),
    sg.Text('', font=('Arial', 14, 'bold'), justification='centered',
    size=(7, 1), background_color='white smoke', border_width=4, relief='ridge',
    key='-SP_INT-'),
#    sg.Input('', size=(7, 1), justification='centered',
#    use_readonly_for_disable=True, disabled=True, key='-SP_INT-'),
    sg.Push()]
]

bin_display_col3 = [
   [sg.Push(),
    sg.Text('', text_color='red', key='-PD_MESSAGES-'), # for error messages
    sg.Push()]
]

bin_display_layout = [
   [sg.Column(bin_display_col1, element_justification='centered',
    expand_x=True)],
   [sg.Column(bin_display_col2, element_justification='centered',
    expand_x=True)],
   [sg.Column(bin_display_col3, expand_x=True)],
]

# Binary Display (4th frame)
#-------------------------------------#
button_col1 = [
   [sg.Button('Example', font='Helvetica 11', key='-EXAMPLE-'),
    sg.Button('Next User PD', font='Helvetica 11', key='-NXT_USER_PD-'),
    sg.Button('Clear', font='Helvetica 11', key='-CLEAR-'),
    sg.Text('', text_color='red', key='-BTN_MESSAGES-'),
    sg.Push(),
#    sg.Button('Save', font='Helvetica 11', key=('-SAVE_MAIN-')),
#    sg.Button('About', font=('Helvetica', 12)),
    sg.Button(' Exit ', font=('Helvetica', 12, 'bold'))]
]

button_layout = [
   [sg.Column(button_col1, expand_x=True)]
]

# Saved rule string frame (5th frame)
#-------------------------------------#
MLINE_SAVED = '-MLINE_SAVED-'+sg.WRITE_ONLY_KEY
saved_layout = [
#      [sg.Text('Saved Rule Strings:')],
      [sg.Push(),
       sg.Multiline(size=(77, 7), font=('Courier', 14, 'bold'),
       disabled=True, autoscroll=True, expand_x=True, expand_y=True,
       pad=(2, 10), horizontal_scroll=True, key=MLINE_SAVED),
       sg.Push()]
]

# Master Window Layout
#-------------------------------------#
layout = [
#   [sg.Text('MAP Calculator', font=('Helvetica', 20), size=(49, 1),
#      pad=((0, 0),(11, 0)), justification=('l'))],
   [sg.Frame('', display_layout, expand_x=True, border_width=6,
      relief='ridge', element_justification='centered')],
   [sg.Frame('', editor_layout, expand_x=True, border_width=6, 
    relief='ridge')],
   [sg.Frame('', bin_display_layout, expand_x=True, border_width=6, 
    relief='ridge')],
   [sg.Frame('', button_layout, expand_x=True, border_width=6, 
    relief='ridge')],
   [sg.Frame('', saved_layout, expand_x=True, border_width=6, 
    relief='ridge')]
   ]

#-------------------------------------------------------------------------#
# Create Main Window
#-------------------------------------------------------------------------#
# Window uses last screen location for next start
# Location is set upon Exit or WINDOW_CLOSE... event
window = sg.Window('IP MAP Calculator', layout, font=windowfont,
   enable_close_attempted_event=True,
   location=sg.user_settings_get_entry('-location-', (None, None)),
   keep_on_top=False, finalize=True)

# Display formatting for strings - applied immediately
#------------------------------------------------------#
window['-BMR_STRING_DSPLY-'].Widget.config(readonlybackground='white smoke',
   borderwidth=3, relief='ridge')

multiline: sg.Multiline = window['MLINE_BIN_EDIT']
widget = multiline.Widget
# Optional string formats
#-------------------------------------#
widget.tag_config('white', foreground='black', background='#FFFFFF')
widget.tag_config('yellow', foreground='black', background='#FFFF00')
widget.tag_config('burley', foreground='black', background='#FFD39B') # burlywood
widget.tag_config('burley3', foreground='black', background='#CDAA7D') # burlywood3
widget.tag_config('grey49', foreground='black', background='#7D7D7D')
widget.tag_config('sage', foreground='black', background='#C2C9A6')
widget.tag_config('peri', foreground='black', background='#B2CAFA') # periwinkle
widget.tag_config('pink', foreground='black', background='#EDABBF') # cherry blossom pink
widget.tag_config('teal', foreground='black', background='#96cdd9') # moonstone
widget.tag_config('lt_purple', foreground='black', background='#D7C1D5')
widget.tag_config('lt_blue1', foreground='black', background='#B3C3D1') # lt blue grey
widget.tag_config('lt_blue2', foreground='black', background='#CCD7E0') # ltr blue grey
widget.tag_config('lt_blue', foreground='black', background='#B2CAFA') # lt blue

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
# upd_obj is "User delegated prefix" received from DHCP
# 'obj' indicates a class object created with the imported ipaddress module
def rule_calc(param_ls, upd_obj, v4host = 0, portidx_b = None):
   print('\n********** START rule_calc **************')
   '''The rule_calc function accepts a BMR paramater list, an IPv6
   user PD (ipaddress object), and an optional port index integer from
   a user input or editing option. It calculates the network address results,
   formats them for the UI, and enters them into a dictionary for the
   UI display function displays_update.
   '''

   # initial values
   #----------------------------------#
   psidlen = (param_ls[5] - (32 - param_ls[4])) # ea_len - host_len
   bmrpd_len = param_ls[2]
   upd_len = upd_obj.prefixlen

   # ppusr = 2^(16 - k) - 2^m (per rfc7597) (2^m is # of excluded ports)
   # 16 is the number of IP port bits (constant)
   # Used for d_dic and other calculations
   if param_ls[6] > 0: # Because PSID Offset > 0 excludes some ports
      ppusr = (2 ** (16 - psidlen)) - (2 ** (16 - psidlen - param_ls[6]))
   else:
      ppusr = (2 ** (16 - psidlen))

   # If call is from the host slider, update the upd with host bits
   # and update v4pfx value in param_ls
   if v4host != 0:
      print(f'>>> v4host is {v4host}')
      pdbin = f'{ip.IPv6Address(upd_obj.network_address):b}'
#      pdint = int(pdbin, 2)
#      pd_add = ip.IPv6Address(pdint)
      pdbin_l = pdbin[:param_ls[2]]
      pdbin_r = pdbin[param_ls[2] + (32 - last_params[4]) : ]
      v4hostbin = bin(v4host)[2:].zfill(32 - param_ls[4])
      print(f'>>> v4hostbin is {v4hostbin}')
      newpdbin = pdbin_l + v4hostbin + pdbin_r
      newpdint = int(newpdbin, 2)
      new_upd_add_str = \
         ip.IPv6Address(newpdint).compressed + '/' + str(upd_obj.prefixlen)
      upd_obj = ip.IPv6Network(new_upd_add_str)
      v4pfxbin = f'{ip.IPv4Address(param_ls[3]):b}'[: int(param_ls[4])]
      print(f'>>> v4pfxbin is {v4pfxbin}')
      v4addbin = v4pfxbin + v4hostbin
      print(f'>>> v4addbin is {v4addbin}')
      newv4int = int(v4addbin, 2)
      newv4add = ip.IPv4Address(newv4int)
      print(f'>>> newv4add is {newv4add}, type is {type(newv4add)}')
      param_ls[3] = newv4add.compressed
      print(f'>>> param_ls[3] is {param_ls[3]}, type {type(param_ls[3])}')
   else:
      window['-V4HOST_SLIDER-'].update(value=0)

   #-------------------------------------------------------------------------#
   # Binary display strings
   #-------------------------------------------------------------------------#

   # BMR PD, User PD, and EA Bits strings data
   #--------------------------------------------------#
   v6p_hex_exp = ip.IPv6Address(param_ls[1]).exploded # 0000:0000:...
   v6p_hex_seglst = v6p_hex_exp.split(':')[:4] # ['0000', '0000', ...]
   upd_hex_exp = ip.IPv6Address(upd_obj.network_address).exploded # 0000:0000:...
   upd_hex_seglst = upd_hex_exp.split(':')[:4] # ['0000', '0000', ...]
   v6p_bin = f'{ip.IPv6Address(param_ls[1]):b}'[:64] # first 64 bits of pfx
   v6p_bin_seglst = [v6p_bin[i:i+16] for i in range(0, 64, 16)]
   v6p_bin_fmt = ':'.join(v6p_bin_seglst) + f'::/{bmrpd_len}'
   upd_bin = f'{ip.IPv6Address(upd_obj.network_address):b}'[:64]
   upd_bin_seglst = [upd_bin[i:i+16] for i in range(0, 64, 16)]
   upd_bin_fmt = ':'.join(upd_bin_seglst) + f'::/{upd_len}'
   ea_bin_idxl = V6Indices(param_ls[2]) # V6Indices adds # of separators
   ea_bin_idxr = V6Indices(upd_len)
   ea_bin_fmt = upd_bin_fmt[ea_bin_idxl : ea_bin_idxr]

   # User PD (upd) strings data
   #--------------------------------------------------#
   v4hostbin_len = 32 - param_ls[4]
   psid_idxl = param_ls[2] + v4hostbin_len
   psid_idxr = param_ls[2] + param_ls[5]
   v4str = param_ls[3]
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

   # IPv4 string data
   #--------------------------------------------------#
   v4ip_str = param_ls[3]
   v4_seglst = v4ip_str.split('.')
   v4mask = param_ls[4]
   v4_obj = ip.ip_network(v4ip_str + '/' + str(v4mask), strict=False)
   v4_bin = f'{ip.IPv4Address(v4ip_str):b}'
   # make segments equal length for display
   v4_bin_seglst = [v4_bin[i:i+8] for i in range(0, 32, 8)]
   v4_bin_fmt = '.'.join(v4_bin_seglst) + f'/{v4mask}'
   for i, seg in enumerate(v4_seglst):
      if len(seg) == 3:
         pass
      elif len(seg) == 2:
         v4_seglst[i] = f' {seg}'
      elif len(seg) == 1:
         v4_seglst[i] = f' {seg} '

   # Modify Port string if Port Index (portidx) has been changed
   #--------------------------------------------------------------#
   if portidx_b:
      if portidx_b == 0:
         pass
      elif portidx_b < 1000:
         pidx_int = int(pidx_bin, 2) 
         if pidx_int + portidx_b <= 2 ** (16 - psidlen) - 1:
            pidx_int = pidx_int + portidx_b
         else:
            pidx_int = 2 ** (16 - psidlen) - 1
            window['-PD_MESSAGES-'].update('Port index maximum reached')
         pidx_bin = bin(pidx_int)[2:].zfill(len(pidx_bin)) # for d_dic
         psid_ofst_bin = pidx_bin[: len(psid_ofst_bin)]
         portrpad_bin = pidx_bin[len(psid_ofst_bin) :]
         port_bin = psid_ofst_bin + \
                    psid + \
                    portrpad_bin
         port_int = int(port_bin, 2) # for d_dic
      else:
         window['-PD_MESSAGES-'].update('Port index maximum reached')
         pidx_int = 2 ** (16 - psidlen) - 1
         pidx_bin = bin(pidx_int)[2:] # for d_dic
         psid_ofst_bin = pidx_bin[: len(psid_ofst_bin)]
         portrpad_bin = pidx_bin[len(psid_ofst_bin) :]
         port_bin = psid_ofst_bin + \
                    psid + \
                    portrpad_bin
         port_int = int(port_bin, 2) # for d_dic

   # BMR PD, User PD, and EA Bits dictionary entries
   #--------------------------------------------------#
   bin_str_dic = {}
   bin_str_dic['params_str'] = f'          User PD Len /{upd_len},' \
                              f' with BMR PD Len /{param_ls[2]}' \
                              f' = EA Bits Len {param_ls[5]}'
   bin_str_dic['blank1'] = ''
   bin_str_dic['v6p_hexstr'] = f" BMR PD:{' ' * 8}" \
                              f"{'      :      '.join(v6p_hex_seglst)}" \
                              f"      ::/{bmrpd_len}"
   bin_str_dic['upd_hexstr'] = f" User PD:{' ' * 7}" \
                              f"{'      :      '.join(upd_hex_seglst)}" \
                              f"      ::/{upd_len}"
   bin_str_dic['bmr_binstr'] = ' BMR PD:  ' + v6p_bin_fmt
   bin_str_dic['upd_binstr'] = ' User PD: ' + upd_bin_fmt
   bin_str_dic['ea_binstr'] = ' EA Bits: ' + '.' * V6Indices(param_ls[2]) + ea_bin_fmt

   # IPv4 dictionary entries
   #--------------------------------------------------#
   bin_str_dic['blank2'] = ''
   bin_str_dic['v4_intstr'] = f" IPv4 Addr:     " \
                            f"{'  .   '.join(v4_seglst)}" \
                            f"  /{v4mask}"
   bin_str_dic['v4_binstr'] = f" IPv4 Addr:  {v4_bin_fmt}"

   # Port and Port Index dictionary entries
   #--------------------------------------------------#
   bin_str_dic['blank3'] = ''
   bin_str_dic['portidx_b'] = f' The "PORT INDEX" is PSID-Offset/Right-Padding:' \
                            f' {psid_ofst_bin}-{portrpad_bin}'
   bin_str_dic['port_bin'] = f' The PORT is PSID-Offset/PSID/Right-Padding: ' \
                           f'{psid_ofst_bin}-{psid}-{portrpad_bin}' \
                           f' = Port {port_int}'

   #-------------------------------------------------------------------------#
   # Binary display highlight indices
   #-------------------------------------------------------------------------#
   # highlight index data
   #----------------------------------#
   bmr_binstr_l = next(i for (i, e) in enumerate(bin_str_dic["bmr_binstr"])
      if e not in "BMR PD: ")
   bmr_binstr_r = bmr_binstr_l + V6Indices(param_ls[2])
   upd_binstr_l = bmr_binstr_l + V6Indices(param_ls[2])
   upd_binstr_r = bmr_binstr_l + V6Indices(upd_len)
   upd_binstr_sbnt_l = upd_binstr_r
   upd_binstr_sbnt_r = bin_str_dic['upd_binstr'].index('::')
   ea_binstr_l = next(i for (i, e) in enumerate(bin_str_dic["ea_binstr"])
      if e not in "EA Bits:.")
   ea_binstr_r = ea_binstr_l + len(ea_bin_fmt)
   # ea_binstr_div is v4host_r and psid_l
   ea_binstr_div = bmr_binstr_l + V6Indices(param_ls[2] + v4hostbin_len)
   prtidx_ofst_l = 48
   prtidx_ofst_r = prtidx_ofst_l + param_ls[6]
   prtidx_pad_l = prtidx_ofst_r + 1
   prtidx_pad_r = prtidx_pad_l + (16 - param_ls[6] - psidlen)
   portbin_ofst_hl_l = 45
   portbin_ofst_hl_r = portbin_ofst_hl_l + param_ls[6]
   portbin_psid_hl_l = 45 + len(psid_ofst_bin) + 1
   portbin_psid_hl_r = portbin_psid_hl_l + psidlen
   portbin_pad_hl_l = portbin_psid_hl_r + 1
   portbin_pad_hl_r = portbin_pad_hl_l + (16 - param_ls[6] - psidlen)
   v4ip_hl_l = 13 + V4Indices(param_ls[4])
   v4ip_hl_r = 13 + V4Indices(32)

   # highlight index dictionary
   #----------------------------------#
   # Prepend line number for each highlight index
   hl_dic = {}
   hl_dic['bmr_hl'] = ['5.' + str(bmr_binstr_l), '5.' + str(bmr_binstr_r)]
   hl_dic['upd_hl'] = ['6.' + str(upd_binstr_l), '6.' + str(upd_binstr_r)]
   hl_dic['sbnt_hl'] = ['6.' + str(upd_binstr_sbnt_l), '6.' + str(upd_binstr_sbnt_r)]
   hl_dic['ea_v4_hl'] = ['7.' + str(ea_binstr_l), '7.' + str(ea_binstr_div)]
   hl_dic['ea_psid_hl'] = ['7.' + str(ea_binstr_div), '7.' + str(ea_binstr_r)]
   hl_dic['v4ip_hl'] = ['9.' + str(v4ip_hl_l), '9.' + str(v4ip_hl_r)]
   hl_dic['v4ipbin_hl'] = ['10.' + str(v4ip_hl_l), '10.' + str(v4ip_hl_r)]
   hl_dic['prtidx_ofst_hl'] = ['12.' + str(prtidx_ofst_l), '12.' + str(prtidx_ofst_r)]
   hl_dic['prtidx_pad_hl'] = ['12.' + str(prtidx_pad_l), '12.' + str(prtidx_pad_r)]
   hl_dic['portbin_ofst_hl'] = ['13.' + str(portbin_ofst_hl_l), '13.' + str(portbin_ofst_hl_r)]
   hl_dic['portbin_psid_hl'] = ['13.' + str(portbin_psid_hl_l), '13.' + str(portbin_psid_hl_r)]
   hl_dic['portbin_pad_hl'] = ['13.' + str(portbin_pad_hl_l), '13.' + str(portbin_pad_hl_r)]

   #-------------------------------------------------------------------------#
   # Results = Display values dictionary
   #-------------------------------------------------------------------------#
   d_dic = {}
   d_dic['paramlist'] = param_ls
   d_dic['v4ips'] = 2 ** (32 - param_ls[4]) # 2^host_bits
   d_dic['sratio'] = 2 ** psidlen # num of unique psids/v4-host
   d_dic['users'] = d_dic['v4ips'] * d_dic['sratio']
   d_dic['ppusr'] = ppusr
   d_dic['bmr_str'] = '|'.join([str(x) for x in param_ls])
   d_dic['upd_str'] = upd_obj.compressed  # upd = User Delegated Prefix (PD)
   d_dic['ce_ip'] = v4str
   d_dic['port_int'] = port_int
   d_dic['pidx_bin'] = pidx_bin
   d_dic['bin_str_dic'] = bin_str_dic
   d_dic['hl_dic'] = hl_dic
   d_dic['num_excl_ports'] = 2 ** (16 - param_ls[6])

   displays_update(d_dic, upd_obj)

   return d_dic

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
   It then updates all affected UI fields.
   '''

   # Initial field updates
   #----------------------------------#
   # Output BMR results to display
   window['-IPS_DSPLY-'].update(dic['v4ips'])
   window['-RATIO_DSPLY-'].update(dic['sratio'])
   window['-USERS_DSPLY-'].update(dic['users'])
   window['-PORTS_DSPLY-'].update(dic['ppusr'])
   window['-BMR_STRING_DSPLY-'].update(dic['bmr_str'])

   # Output values to Edit String and Values fields
   window['-STRING_IN-'].update(dic['bmr_str'])
   for i, element in enumerate(pframe_ls):
      window[element].update(dic['paramlist'][i])

   # Output User PD, CE IP, and Port to binary string editor
   window['-USER_PD-'].update(dic['upd_str'])
   window['-USER_IP4-'].update(dic['ce_ip'])
   window['-USER_PORT-'].update(dic['port_int'])
   window['-SP_INT-'].update(dic['port_int'])
   window['-SP_INDEX-'].update(dic['pidx_bin'])

   # Output binary strings to binary string editor
   for num, bstr in enumerate(dic['bin_str_dic']):
      if num == 0:   # No append on line 0 causes initial "clear field"
         multiline.update(''.join((dic['bin_str_dic'][bstr], '\n')))
      else:
         multiline.update(''.join((dic['bin_str_dic'][bstr], '\n')), append=True)
#
#   for num, bstr in enumerate(dic['pd_bs_dic']):
#      multiline.update(''.join((dic['pd_bs_dic'][bstr], '\n')), append=True)
#
#   for num, bstr in enumerate(dic['v4_bs_dic']):
#      multiline.update(''.join((dic['v4_bs_dic'][bstr], '\n')), append=True)

   # Output values to binary editor sliders and input fields
   window['-V6PFX_LEN_SLDR-'].update(dic['paramlist'][2])
   window['-EA_LEN_SLDR-'].update(dic['paramlist'][5])
   window['-V4PFX_LEN_SLDR-'].update(dic['paramlist'][4])
   window['-PSID_OFST_SLDR-'].update(dic['paramlist'][6])
   window['-V4HOST_SLIDER-'].update(range=(0, dic['v4ips'] - 1))
#   window['-PORT_SLIDER-'].update(range=(0, (dic['ppusr'] - 1) ))
#   window['-PORT_INDEX-'].update('0') #### <<<<------ UPDATE WITH ACTUAL VALUE !!! !!!

   #-------------------------------------------------------------------------#
   # Binary string highlights
   #-------------------------------------------------------------------------#
   # Update received hl indices w/required line numbers
   #----------------------------------------------------#
   # BMR binary string
#   for i, x in enumerate(dic["hl_dic"]["bmr_hl"]):
#      dic["hl_dic"]["bmr_hl"][i] = '5.' + str(x)   # User PD is on line 4
#
#   # User PD binary string
#   for i, x in enumerate(dic["hl_dic"]["upd_hl"]):
#      dic["hl_dic"]["upd_hl"][i] = '6.' + str(x)
#
#   # IPv6 subnet bits in User PD binary string
#   for i, x in enumerate(dic["hl_dic"]["sbnt_hl"]):
#      dic["hl_dic"]["sbnt_hl"][i] = '6.' + str(x)
#
#   # IPv4 host bits in MAP EA binary string
#   for i, x in enumerate(dic["hl_dic"]["ea_v4_hl"]):
#      dic["hl_dic"]["ea_v4_hl"][i] = '7.' + str(x)
#
#   # PSID bits in MAP EA binary string
#   for i, x in enumerate(dic["hl_dic"]["ea_psid_hl"]):
#      dic["hl_dic"]["ea_psid_hl"][i] = '7.' + str(x)
#
#   # Port Index
#   for i, x in enumerate(dic['hl_dic']['prtidx_ofst_hl']):
#      dic['hl_dic']['prtidx_ofst_hl'][i] = '9.' + str(x)
#   for i, x in enumerate(dic['hl_dic']['prtidx_pad_hl']):
#      dic['hl_dic']['prtidx_pad_hl'][i] = '9.' + str(x)
#
#   # Port Index & PSID bits in port binary string
#   for i, x in enumerate(dic['hl_dic']['portbin_ofst_hl']):
#      dic['hl_dic']['portbin_ofst_hl'][i] = '10.' + str(x)
#
#   for i, x in enumerate(dic['hl_dic']['portbin_psid_hl']):
#      dic['hl_dic']['portbin_psid_hl'][i] = '10.' + str(x)
#
#   for i, x in enumerate(dic['hl_dic']['portbin_pad_hl']):
#      dic['hl_dic']['portbin_pad_hl'][i] = '10.' + str(x)
#
#   # IPv4 strings
#   for i, x in enumerate(dic['hl_dic']['v4ip_hl']):
#      dic['hl_dic']['v4ip_hl'][i] = '12.' + str(x)
#
#   for i, x in enumerate(dic['hl_dic']['v4ipbin_hl']):
#      dic['hl_dic']['v4ipbin_hl'][i] = '13.' + str(x)

   # Apply highlights
   #----------------------------------#
   widget.tag_add('white', *dic['hl_dic']['bmr_hl'])
   widget.tag_add('white', *dic['hl_dic']['upd_hl'])
   widget.tag_add('grey49', *dic['hl_dic']['sbnt_hl'])
   widget.tag_add('pink', *dic['hl_dic']['ea_v4_hl'])
   widget.tag_add('teal', *dic['hl_dic']['ea_psid_hl'])

   widget.tag_add('burley', *dic['hl_dic']['prtidx_ofst_hl'])
   widget.tag_add('yellow', *dic['hl_dic']['prtidx_pad_hl'])

   widget.tag_add('burley', *dic['hl_dic']['portbin_ofst_hl'])

   widget.tag_add('teal', *dic['hl_dic']['portbin_psid_hl'])

   widget.tag_add('yellow', *dic['hl_dic']['portbin_pad_hl'])

   widget.tag_add('pink', *dic['hl_dic']['v4ip_hl'])
   widget.tag_add('pink', *dic['hl_dic']['v4ipbin_hl'])


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

# Example BMR prefix lists and parameters
#-----------------------------------------#
# param_ls = [name, v6pfx, v6pfx mask, v4pfx, v4pfx mask, ealen, psid offset]
class ExampleParams:
   '''Returns a list of example BMR parameters. The Python ipaddress module and
   self.rv6blk is used to create an IPv6 class (.subnets) object. New IPv6 BMR
   prefixes are pulled from this object until ExampleParams() is called and
   last_plist (created in global space by a global function) has been changed.
   At this time, a new class object is created and saved.
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
      self.rv6pfxs_obj = None
      self.rv4pfxs_obj = None

   def new_params(self):
      if self.last_plist:
         plist = self.last_plist
         plist[0] = 'example_' + str(next(self.ex_cnt))
         plist[1] = next(self.rv6pfxs_obj).network_address.compressed
         plist[3] = next(self.rv4pfxs_obj).network_address.compressed
         return(plist)
      else:
         self.ex_cnt = (i for i in range(16384))
         self.rv6pfxs_obj = ip.ip_network(self.rv6blk).subnets(
            new_prefix = self.rv6plen)
         self.rv4pfxs_obj = ip.ip_network(self.rv4blk).subnets(
            new_prefix = self.rv4plen)
         plist = ['example_' + str(next(self.ex_cnt)),
                  next(self.rv6pfxs_obj).network_address.compressed,
                  self.rv6plen,
                  next(self.rv4pfxs_obj).network_address.compressed,
                  self.rv4plen,
                  self.ealen,
                  self.psid_ofst
                 ]
         self.last_plist = plist
         return(plist)

class UserPd:
   '''Return a User Delegated Prefix (PD|upd) object.
   If BMR parameters (last_plist) remains the same, it returns
   PD objects from this object. If the parameters change,
   a new PD object is created.
   syntax: x = UserPd(param_ls)
   print(x.new_pd())'''
   def __init__(self, plist):
      self.plist = plist
      self.last_plist = []
      self.pd_obj = None
      self.lastpd = ''

   def new_pd(self):
      if self.plist == self.last_plist:  # New PD
         nextpd = next(self.pd_obj)
         self.lastpd = nextpd
         return nextpd
      else:                              # Next PD
         self.last_plist = self.plist
         bmr_v6p = ip.ip_network('/'.join((self.plist[1], str(self.plist[2]))))
         pd_len = int(self.plist[2]) + int(self.plist[5])
         self.pd_obj = bmr_v6p.subnets(new_prefix = pd_len)
         nextpd = next(self.pd_obj)
         self.lastpd = nextpd
         return nextpd

# Account for IP address separators (: & .) in binary strings
def V6Indices(bin_right):
   '''For creation of highlight indices for IPv6 binary strings.
   For a given string length, it returns that length increased
   by the number of separators ":" that will be inserted.
   '''
   if bin_right > 48:
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
#   if bin_right > 32:
#      bin_right += 3
#   elif bin_right > 24:
#      bin_right += 3
#   elif bin_right > 16:
#      bin_right += 2
#   elif bin_right > 8:
#      bin_right += 1
#   return bin_right

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
   '''Validates input parameters by using "try" to create
   required IP prefix object variables. Sets flag on failures.
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
      validflag = 'fail'
      advance('-R6PRE-')
      window['-PARAM_MESSAGES-'].update(
         f'IPv6 {v6p}/{v6pl} not valid. Host bits set?')

   # test IPv4 prefix/mask
   if validflag == 'pass':
      try:
         v4pfx_bits = f'{ip.IPv4Address(v4p):b}'[:v4pl]
      except ValueError:
         valdflag = 'fail'
      
      if validflag == 'pass':
         v4pfx_bin = f'{v4pfx_bits:<032s}'
         v4pfx_int = int(v4pfx_bin, 2)
         v4pfx = ip.ip_address(v4pfx_int)
         
         try:
            ip.ip_network(v4pfx, v4pl)
         except:
            validflag = 'fail'

   # validate Rule prefix masks are in acceptable MAP-T Rule ranges
   if validflag == 'pass':
      if int(v6pl) + eal > 64: # (v6 prefix + EA length) > 64 not allowed
         validflag = 'fail'
         window['-PD_MESSAGES-'].update(
            f"IPv6 prefix mask + EA Bits can't exceed 64 bits")
      if eal < (32 - v4pl):  # EA length < v4 host bits (RFC?)
         validflag = 'fail'
         window['-PD_MESSAGES-'].update(
            f"EA Bits can't be less than IPv4 host bits")

   # validate EA Bits and PSID Offset values are in valid MAP-T Rule range
   # (values not tested with actual BMR!)
   if validflag == 'pass':
      if eal > 48:     # EA length > 48 is invalid, rfc7597 5.2
         validflag = 'fail'
         advance('-EABITS-')
         window['-PARAM_MESSAGES-'].update('EA bits out of range')
      elif psofst_len > 15:   # PSID offset > 15 = no available ports
         validflag = 'fail'
         window['-PARAM_MESSAGES-'].update('PSID Offset must not exceed 15')
##         advance('-OFFSET-')
##### >>>> CHECK TO SEE IF OFFSET > 15 IS ACTUALLY POSSIBLE <<<< ##### <----- REVIEW
      elif psofst_len + psid_len > 16:
         # psid length + psid offset > 16 bit port length not valid
         validflag = 'fail'
         window['-PARAM_MESSAGES-'].update('PSID Offset + PSID length > 16 bits')
         window['-PD_MESSAGES-'].update('PSID Offset + PSID length > 16 bits')
   return validflag

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
dframe_ls = ['-BMR_STRING_DSPLY-', '-USERS_DSPLY-', '-PORTS_DSPLY-',
             '-IPS_DSPLY-', '-RATIO_DSPLY-']   # Display Frame fields

# Parameter Editor frame fields
#----------------------------------#
pframe_ls = ['-RULENAME-', '-R6PRE-', '-R6LEN-', '-R4PRE-', '-R4LEN-',
   '-EABITS-', '-OFFSET-']
#stringin = ['-STRING_IN-']  # Rule String field
#bframe_ls = ['-USER_PD-', '-USER_IP4-', '-V6PFX_LEN_SLDR-', '-EA_LEN_SLDR-',
#   '-V4PFX_LEN_SLDR-', '-PSID_OFST_SLDR-', '-V4HOST_SLIDER-',
#   '-PORT_INDEX-', 'MLINE_BIN_EDIT']       # Binary Editor fields
#sframe_ls = ['MLINE_SAVED']                # Don't clear Save frame

# Event Loop Variables
#----------------------------------#
toggle_visible = True # Show hidden elements
chars = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789().'
v6chars = '0123456789abcdefABCDEF:'
intchars = '0123456789'
v4chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
integer_inputs = ['-R6LEN-', '-R4LEN-', '-EABITS-', '-OFFSET-',
   '-CE_IDX-', '-CE_PRT_IDX-']
example_obj = None
userpd_cls_obj = None
savctr = False
portidxadd = 0 # used with 'Source Port Index n = Port' section
last_params = None

#-------------------------------------------------------------------------#
# Main Event Loop - runs once for each 'event'
#-------------------------------------------------------------------------#
cntr = 1  # debugging
while True:
   event, values = window.read()    # type: (str, dict)
   print(f'\n#--------- Event {str(cntr)} ----------#')
   print(event, values)
   cntr += 1
   if event in (' Exit ', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
      # Save screen location when closing window
      sg.user_settings_set_entry('-location-', window.current_location())
      break

## Prints all available element keys
#   print('\n ---- VALUES KEYS ----')
#   for x in values.keys():
#      print(x)

   # Clear message fields on next event
   window['-PARAM_MESSAGES-'].update('')
   window['-PD_MESSAGES-'].update('')
   window['-BTN_MESSAGES-'].update('')

   # Clear all fields except Save Frame
   if event == '-CLEAR-':
      for i in [*dframe_ls, *pframe_ls]: #, *sframe_ls]:
         window[i].update('')
      window['MLINE_BIN_EDIT'].update('')
      window['-V4HOST_SLIDER-'].update(value=0)
      window['-USER_PD-'].update('')
      window['-USER_IP4-'].update('')
      window['-USER_PORT-'].update('')
      window['-V4HOST_SLIDER-'].update(range=(0, 0))
      window['-STRING_IN-'].update('')
      window['-SP_INDEX-'].update('')
      window['-SP_INT-'].update('')
      userpd_cls_obj = None # delete UserPd class object
#      last_params = None
      example_obj = None # delete NewParams class object
      last_params = None

#   if event == '-SAVE_MAIN-':

   # Load example values in main display and editors
   #-------------------------------------------------#
   if event == '-EXAMPLE-' and last_params:
      window['-BTN_MESSAGES-'].update('"Clear" or "Next User PD" for new example')
   elif event == '-EXAMPLE-':
      portidxadd = 0      # reset port index setting
      if example_obj:
         param_ls = example_obj.new_params()
      else:
         example_obj = ExampleParams()
         param_ls = example_obj.new_params()
      last_params = param_ls
   
      if userpd_cls_obj:
         userpd_obj = userpd_cls_obj.new_pd()
      else:
         userpd_cls_obj = UserPd(param_ls)
         userpd_obj = userpd_cls_obj.new_pd()
         last_userpd_obj = userpd_obj
      rule_calc(param_ls, userpd_obj)
      

   # BMR parameter entry - validate input as it is typed
   #-----------------------------------------------------#
   if event == '-RULENAME-' and values[event][-1] not in chars:
      window[event].update(values[event][:-1])
      window['-PARAM_MESSAGES-'].update('Invalid character')
   elif event == '-RULENAME-' and len(str(values['-RULENAME-'])) > 20:
         window[event].update(values[event][:-1])
         window['-PARAM_MESSAGES-'].update('Too long')
   if event == '-STRING_IN-' and values['-STRING_IN-']:
      if len(str(values['-STRING_IN-'])) > 59:
         window[event].update(values[event][:-1])
         # Find a place to send error message ------------<<<<<<<<<<<< REVIEW
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

   if event == '-ENTER_PARAMS-':
      portidxadd = 0      # reset port index setting
      valid = 'not set'
      for p in pframe_ls:
         if p == '-OFFSET-' and values[p] == 0:
            allow = 'yes'
         else:
            if not values[p]:
               window['-PARAM_MESSAGES-'].update(f'Missing Parameter: {p}')
               advance(p)
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
               last_params = param_ls # Used for UserPd() to decide next vs. new PD
               userpd_cls_obj = UserPd(param_ls)
               new_userpd_obj = userpd_cls_obj.new_pd()
               last_userpd_obj = new_userpd_obj
               rule_calc(param_ls, new_userpd_obj)
            else:
               window['-PARAM_MESSAGES-'].update('Values out of MAP-T range') # Review if this is possible after pre-checks

   # Validate Enter/Edit String
   # Values in allowable ranges. But not tested that they work in BMR!
   #-------------------------------------------------------------------#
   if event == '-ENTER_STRING-':
      portidxadd = 0      # reset port index setting
      valid = 'not set'
      if not values['-STRING_IN-']:
         window['-STRING_IN-'].update('Enter rule string')
         window['-PARAM_MESSAGES-'].update('Missing String')
         advance('-STRING_IN-')
      elif len(values['-STRING_IN-']) > 69: # ----------------->> NEEDED???
         window['-STRING_IN-'].update('Rule string too long')
      else:
         input_str = values['-STRING_IN-']
         # Values for further processing
         param_ls = input_str.split('|')
         if len(param_ls) != 7:
            window['-PARAM_MESSAGES-'].update('Enter valid rule string'),
            advance('-STRING_IN-')
         else:
            for i, element in enumerate(param_ls):
               if i in [2, 4, 5, 6]:
                  param_ls[i] = int(param_ls[i])
            if param_ls == last_params:
               window['-PARAM_MESSAGES-'].update('No change') # -------->> Add "only name changed" scenario???
            else:
               valid = validate(param_ls)
#               print('>>> "Enter String" validation complete\n valid flag is {valid}')
               if valid == 'pass':
                  last_params = param_ls # Used for UserPd() to decide next vs. new PD
                  userpd_cls_obj = UserPd(param_ls)
                  new_userpd_obj = userpd_cls_obj.new_pd()
                  last_userpd_obj = new_userpd_obj
                  rule_calc(param_ls, new_userpd_obj)
               else:
                  window['-PARAM_MESSAGES-'].update('Values out of MAP-T range') # Review if this is possible after pre-checks

   # Update binary editor values and highlights
   #--------------------------------------------#
   if event.endswith('SLDR-') and values['-STRING_IN-']: # rule to edit must exist
      portidxadd = 0
      param_ls = last_params
      param_ls[2] = int(values['-V6PFX_LEN_SLDR-'])
      param_ls[5] = int(values['-EA_LEN_SLDR-'])
      param_ls[4] = int(values['-V4PFX_LEN_SLDR-'])
      param_ls[6] = int(values['-PSID_OFST_SLDR-'])
      valid = validate(param_ls)
      if valid == 'pass':
         last_params = param_ls # Used for UserPd() to decide next vs. new PD
         userpd_cls_obj = UserPd(param_ls)
         new_userpd_obj = userpd_cls_obj.new_pd()
         last_userpd_obj = new_userpd_obj
         rule_calc(param_ls, new_userpd_obj)
      # Need "else:" statement??

   # Display next User Delegated Prefix (PD)
   #-----------------------------------------#
   if event == '-NXT_USER_PD-' and last_params:
      portidxadd = 0
      next_userpd_obj = userpd_cls_obj.new_pd()
      last_userpd_obj = next_userpd_obj
      next_pd_bin = f'{ip.IPv6Address(next_userpd_obj.network_address):b}'
      next_pd_bin_type = type(f'{ip.IPv6Address(next_userpd_obj.network_address):b}')
      v4hostint = int(values['-V4HOST_SLIDER-']) # slider values are floats
      rule_calc(last_params, next_userpd_obj, v4hostint, portidx_b = 0)

   # Increment IPv4 host address
   #-----------------------------------------#
   # Host slider initialized with range=0. It can't be incremented when range=0
   # Range is updated when BMR parameters are Entered
   # Range is reset to 0 when "Clear" is used
   if event == '-V4HOST_SLIDER-': # ---- May be able to use ip.addr + v4host_slider ----
      portidxadd = 0
      v4hostint = int(values['-V4HOST_SLIDER-']) # slider values are floats
      print(f'\n>>> v4host slider v4hostint is {v4hostint}')
      rule_calc(last_params, last_userpd_obj, v4hostint)
   elif event == '-NEXT_HOST-':
      # If last_params=None (initial state or Clear used) disable button
      if last_params:
         v4hostint = int(values['-V4HOST_SLIDER-']) + 1 # slider values are floats
         print(f'>>> v4host button v4hostint is {v4hostint}')
         window['-V4HOST_SLIDER-'].update(value=v4hostint)
         rule_calc(last_params, last_userpd_obj, v4hostint)

   # Display user source port numbers
   #-----------------------------------------#
   if last_params and 'IDX' in event:
      match event:
         case '-P_IDX_FIRST-':
            portidxadd = 0
            idx = 0
         case '-P_IDX_UP1-':
            idx = 1
         case '-P_IDX_UP10-':
            idx = 10
         case '-P_IDX_UP100-':
            idx = 100
         case '-P_IDX_LAST-':
            idx = 100000
      idx = idx + portidxadd
      portidxadd = idx
      if portidxadd > 100000: # avoiding allowing infinite growth
         portidxadd = 100000  # ----------------------------- do this better!!!

      v4hostint = int(values['-V4HOST_SLIDER-'])
   #   userpd_curr = ip.ip_network(values['-USER_PD-'])
   #   print(f'>>> IDX Change - last_userpd_obj is {last_userpd_obj}')
      rule_calc(last_params, last_userpd_obj, v4host = v4hostint, portidx_b = idx)

   print(f'#------- End Event {cntr - 1} -------#')

#   prints all variables
#   print(dir())

   # Save Current BMR in bottom Multiline field for user to copy
   # Only BMR parameter list section needs to be entered
   #-------------------------------------------------------------#
   if event == '-SAVE-':
      savstr = f'{values["-BMR_STRING_DSPLY-"]} ' \
               f'(IPs-{window["-IPS_DSPLY-"].get()}, ' \
               f'S-{window["-RATIO_DSPLY-"].get()}, ' \
               f'U-{window["-USERS_DSPLY-"].get()}, ' \
               f'P-{window["-PORTS_DSPLY-"].get()})\n'
      if savctr == True:
         window[MLINE_SAVED].update(savstr, append=True)
      else:
         window[MLINE_SAVED].update(savstr)
         savctr = True

window.close()
