#!/usr/bin/env python
import PySimpleGUI as sg
import ipaddress as ip
import os
import sys

'''IP_MAP_Calculator.py: Calculates the results of IP MAP Rule parameters'''

# IP_MAP_ADDRESS_CALCULATOR v0.12.0 - 11/12/2024 - D. Scott Freemire

# Window theme, variables, and functions
#----------------------------------------------------------------------------#
sg.theme('TanBlue') # Tan is #E5DECE, Blue is #063289, Text backgrounds are #FDFDFC
# windowfont=('Helvetica', 10) # = sg.DEFAULT_FONT




def result_val_col(label, key):
    """Create Column layout for displaying one result parameter"""
    layout = [
        [sg.Text(label, font=(None, 10, "bold"), p=0)],
        [
            sg.Text(
                "",
                justification="centered",
                size=(7, 1),
                background_color="#fdfdfc",
                border_width=2,
                relief="sunken",
                key=key,
            )
        ],
    ]

    col = sg.Column(layout, element_justification="centered", p=0)

    return col


def collapse(title, layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Frame(title, layout, visible=False, border_width=2, key=key))


# Main Results Display (top frame) - Calculated Values
# ----------------------------------------------------------------------------#
result_layout_dat = [
    ("Uniq v4 IPs", "-IPS_DSPLY-"),
    ("Sharing", "-RATIO_DSPLY-"),
    ("Users", "-USERS_DSPLY-"),
    ("Ports/User", "-PORTS_DSPLY-"),
]

result_cols_layout = [
    result_val_col(result_layout_dat[i][0], result_layout_dat[i][1])
    for i in range(len(result_layout_dat))
]

results_layout = [
    [
        result_cols_layout[0],
        sg.Text("x", font=(None, 10, "bold"), pad=((0, 0), (12, 0))),
        result_cols_layout[1],
        sg.Text("=", font=(None, 10, "bold"), pad=((0, 0), (12, 0))),
        result_cols_layout[2],
        sg.Text(":", font=(None, 12, "bold"), pad=((0, 0), (10, 0))),
        result_cols_layout[3],
    ],
    [
        sg.Text("First User IPv6 PD:", font=(None, 10, "bold"), pad=((4, 0), (4, 6))),
        sg.Input(
            "",
            font=(None, 10, "bold"),
            size=(28, 1),
            disabled=True,
            justification="centered",
            key="USER_IPV6PD",
        ),
    ],
    # Set Frame width
    # [sg.Sizer(400)]
]

# Collapsing frame layouts
# ----------------------------------------------------------------------------#
# Frame visibility controls
frame_visibility_buttons = [
    [
        sg.Button("BINARY", key="OPEN_BIN_BTN"),
        sg.Button("DHCPv6", key="OPEN_DHCP_BTN"),
        sg.Button("SAVED", key="OPEN_SAVED_BTN"),
    ]
    # [
    #     sg.Checkbox("Blank checkbox"),
    #     sg.Checkbox("Hide Saved Section", enable_events=True, key="-OPEN_SAVED-CHECKBOX"),
    # ],
]

# Binary Display frame layout - collapsible
binary_editor = [
    [
        sg.Multiline(
            default_text="Binary Display",
            size=(81, 8), # Coordinate width with main layout Sizer width
            font=("Courier", 14),
            disabled=True,
            autoscroll=True,
            expand_x=True,
            # expand_y=True,
            pad=(0, 0),
            horizontal_scroll=False,
            background_color="#fdfdfc",
            key="-MLINE_SAVED-",
        )
    ],
    # [sg.Input('Input sec 1', key='-IN1-')],
    # [sg.Input(key='-IN11-')],
    [
        sg.Button("Button section 1", button_color="yellow on green"),
        sg.Button("Button2 section 1", button_color="yellow on green"),
        sg.Button("Button3 section 1", button_color="yellow on green"),
    ],
]

# DHCPv6 Options frame layout - collapsible
dhcp_options = [
    [
        sg.Multiline(
            default_text="DHCP Strings",
            size=(81, 8), # Coordinate width with main layout Sizer width
            font=("Courier", 14),
            disabled=True,
            autoscroll=True,
            expand_x=True,
            # expand_y=True,
            pad=(0, 0),
            horizontal_scroll=False,
            background_color="#fdfdfc",
            key="-MLINE_SAVED-",
        )
    ],
    # [sg.Input('Input sec 1', key='-IN1-')],
    # [sg.Input(key='-IN11-')],
    [
        sg.Button("Button section 1", button_color="yellow on green"),
        sg.Button("Button2 section 1", button_color="yellow on green"),
        sg.Button("Button3 section 1", button_color="yellow on green"),
    ],
]

# Section 2 collapsing frame layout
# ----------------------------------------------------------------------------#
saved_strings = [
    # [sg.Text("Saved BMR Strings")],
    # [sg.Sizer(h_pixels=3, v_pixels=0)],
    [
        sg.Multiline(
            default_text="Saved BMR Strings",
            size=(81, 8), # Multiline width sets Frame width
            font=("Courier", 14),
            disabled=True,
            autoscroll=True,
            expand_x=True,
            # expand_y=True,
            pad=(0, 0),
            horizontal_scroll=False,
            background_color="#fdfdfc",
            key="-MLINE_SAVED-",
        )
    ],
    # sg.Push(),
    # [sg.I('Input sec 2', k='-IN2-')],
    # [sg.I(k='-IN21-')],
    [
        sg.B("Button section 2", button_color=("yellow", "purple")),
        sg.B("Button2 section 2", button_color=("yellow", "purple")),
        sg.B("Button3 section 2", button_color=("yellow", "purple")),
    ],
]

# Master Layout
# ----------------------------------------------------------------------------#
layout = [
    [sg.Frame("Results", results_layout, element_justification='centered', border_width=2, expand_x=True)],
    [sg.Sizer(681)], # Sets overall window size
    [frame_visibility_buttons],

    # Binary Editor Frame
    [
        # sg.T(sg.SYMBOL_RIGHT, enable_events=True, k="OPEN_BIN_SYMBL", text_color="white"),
        sg.T(sg.SYMBOL_RIGHT, enable_events=True, k="OPEN_BIN_SYMBL"),
        sg.T(
            "Binary Editor",
            enable_events=True,
            font="None 10 bold",
            # text_color="white",
            k="OPEN_BIN_TEXT",
        ),
    ],
    [collapse("Binary Editor", binary_editor, "BIN_EDIT")],

    # DHCP Options Frame
    [
        # sg.T(sg.SYMBOL_RIGHT, enable_events=True, k="OPEN_DHCP_SYMBL", text_color="white"),
        sg.T(sg.SYMBOL_RIGHT, enable_events=True, k="OPEN_DHCP_SYMBL"),
        sg.T(
            "DHCP Options",
            enable_events=True,
            font="None 10 bold",
            # text_color="white",
            k="OPEN_DHCP_TEXT",
        ),
    ],
    [collapse("DHCP Strings", dhcp_options, "DHCP_OPTIONS")],

    #### Saved Strings Frame####
    [
        # sg.T(sg.SYMBOL_RIGHT, enable_events=True, k="OPEN_SAVED_SYMBL", text_color="white"),
        sg.T(sg.SYMBOL_RIGHT, enable_events=True, k="OPEN_SAVED_SYMBL"),
        sg.T(
            "Saved BMR Strings",
            enable_events=True,
            font="None 10 bold",
            # text_color="white",
            k="OPEN_SAVED_TEXT",
        ),
    ],
    [collapse("Saved Rule Strings", saved_strings, "SAVED_STRINGS")],

    #### Buttons at bottom ####
    [sg.Button("Button1"), sg.Button("Button2"), sg.Button("Exit")],
]

# window = sg.Window('IP MAP Calculator', layout, font=windowfont,
#    enable_close_attempted_event=True,
#    location=sg.user_settings_get_entry('-location-', (None, None)),
#    keep_on_top=False, resizable=True, size=(755, 1130), finalize=True) #(755, 1070)

window = sg.Window(
    "Visible / Invisible Element Demo",
    layout,
    enable_close_attempted_event=True,
    location=sg.user_settings_get_entry("-location-", (None, None)),
    finalize=True
)

# window["-OPEN_SAVED-CHECKBOX"].update(True) # Set checkbox to "checked" if frame starts invisible

# Intial collapsible frame visibility
# To change, edit this line, "visible" in collapse(), and sg.SYMBOL in layout
open_binary, open_dhcp, open_saved = False, False, False

while True:  # Event Loop
    event, values = window.read()
    print(event, values)

    if event in ("Exit", sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
        # Save screen location when closing window
        sg.user_settings_set_entry("-location-", window.current_location())
        break

    # if event == sg.WIN_CLOSED or event == 'Exit':
    #     break

# Frame visibility controls
# ----------------------------------------------------------------------------#
    if event.startswith("OPEN_BIN_"):
        open_binary = not open_binary
        window["OPEN_BIN_SYMBL"].update(sg.SYMBOL_DOWN if open_binary else sg.SYMBOL_RIGHT)
        window["BIN_EDIT"].update(visible=open_binary)
        if open_binary:
            window["OPEN_BIN_BTN"].update(button_color="black on yellow")
        else:
            window["OPEN_BIN_BTN"].update(button_color="white on #283b5b")

    if event.startswith("OPEN_DHCP_"):
        print("********* IN OPEN_DHCP *********")
        open_dhcp = not open_dhcp
        window["OPEN_DHCP_SYMBL"].update(sg.SYMBOL_DOWN if open_dhcp else sg.SYMBOL_RIGHT)
        window["DHCP_OPTIONS"].update(visible=open_dhcp)
        if open_dhcp:
            window["OPEN_DHCP_BTN"].update(button_color="black on yellow")
        else:
            window["OPEN_DHCP_BTN"].update(button_color="white on #283b5b")

    if event.startswith("OPEN_SAVED_"):
        open_saved = not open_saved
        window["OPEN_SAVED_SYMBL"].update(sg.SYMBOL_DOWN if open_saved else sg.SYMBOL_RIGHT)
        window["SAVED_STRINGS"].update(visible=open_saved)
        if open_saved:
            window["OPEN_SAVED_BTN"].update(button_color="black on yellow")
            window.refresh()
        else:
            window["OPEN_SAVED_BTN"].update(button_color="white on #283b5b")

    print(window.size)
    print(sg.theme())

window.close()
