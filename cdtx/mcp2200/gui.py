from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout


class EasyLayoutWidget(QtWidgets.QWidget):
    __layouts = []
    def __init__(self, *args, **kwargs):
        super(EasyLayoutWidget, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout()
        self.deployLayouts(layout, self.get_layouts())
        self.setLayout(layout)

    def get_layouts(self):
        return []

    def deployLayouts(self, parent, tree):
        for _name, _type, _tree in tree:
            setattr(self, _name, _type())
            parent.addLayout(getattr(self, _name))
            self.deployLayouts(getattr(self, _name), _tree)

class MCP2200Widget(EasyLayoutWidget):
    def __init__(self, *args, **kwargs):
        super(MCP2200Widget, self).__init__(*args, **kwargs)

        # Detected devices
        self.lv_devices = QtWidgets.QListView()
        self.lv_devices.setMinimumHeight(50)
        self.l_00.addWidget(self.lv_devices)


        self.l_1111.addWidget(QtWidgets.QLabel('IO Config'), 0, 0)
        self.io_config = QtWidgets.QLineEdit()
        self.l_1111.addWidget(self.io_config, 0, 1)

        self.l_1111.addWidget(QtWidgets.QLabel('Output Default'), 1, 0)
        self.output_default = QtWidgets.QLineEdit()
        self.l_1111.addWidget(self.output_default, 1, 1)

        # LEDs groupbox
        self.gb_leds = QtWidgets.QGroupBox('LED Function')
        self.gl_leds = QHBoxLayout()
        self.gb_leds.setLayout(self.gl_leds)

        self.gl_leds_11 = QVBoxLayout()
        self.gl_leds.addLayout(self.gl_leds_11)

        self.gb_leds_2 = QtWidgets.QGroupBox('Blink Duration')
        self.gl_leds_12 = QVBoxLayout()
        self.gb_leds_2.setLayout(self.gl_leds_12)
        self.gl_leds.addWidget(self.gb_leds_2)

        self.rb_leds_blink = QtWidgets.QRadioButton('Blink LEDs')
        self.rb_leds_toggle = QtWidgets.QRadioButton('Toggle LEDs')
        self.rb_leds_100ms = QtWidgets.QRadioButton('100 ms')
        self.rb_leds_200ms = QtWidgets.QRadioButton('200 ms')
        self.gl_leds_11.addWidget(self.rb_leds_blink)
        self.gl_leds_11.addWidget(self.rb_leds_toggle)
        self.gl_leds_12.addWidget(self.rb_leds_100ms)
        self.gl_leds_12.addWidget(self.rb_leds_200ms)
        self.l_111.addWidget(self.gb_leds)


        self.baud_rate = QtWidgets.QComboBox()
        self.baud_rate.addItems(['50', '300', '600', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        self.l_112.addWidget(self.baud_rate, 0, 0)
        self.l_112.addWidget(QtWidgets.QLabel('Baud Rate'), 0, 1)

        for _index, (_name, _value) in enumerate((
            ('enable_tx_rx_leds',    QtWidgets.QCheckBox('Enable Tx/Rx LEDs')),
            ('enable_cts_rts_pins',  QtWidgets.QCheckBox('Enable CTS/RTS Pins')),
            ('enable_usbcfg_pin',    QtWidgets.QCheckBox('Enable USBCFG Pin')),
            ('enable_suspend_pin',   QtWidgets.QCheckBox('Enable Suspend Pin')),
            ('invert_uart_polarity', QtWidgets.QCheckBox('Invert UART Polarity (UPOL)')),
        )):
            setattr(self, _name, _value)
            self.l_112.addWidget(getattr(self, _name), _index+1, 0, columnSpan=2)

        # vid/pid
        self.l_12.addWidget(QtWidgets.QLabel('New'), 0, 1)
        self.l_12.addWidget(QtWidgets.QLabel('Using'), 0, 2)

        self.l_12.addWidget(QtWidgets.QLabel('Vendor ID'), 1, 0)
        self.tb_vid = QtWidgets.QLineEdit('0x04D8')
        self.tb_vid.setFixedWidth(80)
        self.l_12.addWidget(self.tb_vid, 1, 1)
        self.l_12.addWidget(QtWidgets.QLabel('Product ID'), 2, 0)
        self.tb_pid = QtWidgets.QLineEdit()
        self.tb_pid.setFixedWidth(80)
        self.l_12.addWidget(self.tb_pid, 2, 1)

        self.lbl_vid = QtWidgets.QLabel('0x04D8')
        self.l_12.addWidget(self.lbl_vid, 1, 2)
        self.lbl_pid = QtWidgets.QLabel('0x00DF')
        self.l_12.addWidget(self.lbl_pid, 2, 2)

        self.bp_update_vidpid = QtWidgets.QPushButton('Update\nVID/PID')
        self.l_12.addWidget(self.bp_update_vidpid, 1, 3, 2, 1)

        # String descriptors
        self.gb_str_desc = QtWidgets.QGroupBox('String Descriptors')
        self.gl_str_desc = QGridLayout()
        self.gb_str_desc.setLayout(self.gl_str_desc)

        self.gl_str_desc.addWidget(QtWidgets.QLabel('Manufacturer'), 0, 0)
        self.tb_manufacturer = QtWidgets.QLineEdit()
        self.gl_str_desc.addWidget(self.tb_manufacturer, 0, 1)

        self.gl_str_desc.addWidget(QtWidgets.QLabel('Product'), 1, 0)
        self.tb_product = QtWidgets.QLineEdit()
        self.gl_str_desc.addWidget(self.tb_product, 1, 1)

        self.l_13.addWidget(self.gb_str_desc)

        # Logs
        self.txt_logs = QtWidgets.QTextEdit()
        self.txt_logs.setFixedHeight(250)
        self.l_14.addWidget(self.txt_logs)

        



    def get_layouts(self):
        # name, type, childs
        return [['l_1', QVBoxLayout, 
            [
                # Connected devices
                ['l_00', QVBoxLayout, []
                ],
                # mcp2200 features
                ['l_11', QHBoxLayout, 
                    [
                        # gpio stuffs
                        ['l_111', QVBoxLayout, 
                            [
                                ['l_1111', QGridLayout, []]
                            ]
                        ],
                        # uart stuffs
                        ['l_112', QGridLayout, []
                        ]
                    ]
                ],
                # vid/pid
                ['l_12', QGridLayout, []
                ],
                # String descriptors
                ['l_13', QVBoxLayout, []
                ],
                # Logs
                ['l_14', QVBoxLayout, []
                ],
            ]
        ]]


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    wgt = MCP2200Widget()

    window = QtWidgets.QMainWindow()
    window.setCentralWidget(wgt)
    window.show()

    app.exec_()
    
