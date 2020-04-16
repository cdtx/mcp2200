from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtCore import SIGNAL, Signal, Slot, QObject
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

from cdtx.mcp2200.device import MCP2200_VID, MCP2200_PID
import cdtx.mcp2200.api
from cdtx.mcp2200.api import SimpleIOClass

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
        self.build_gui()

        self.mcp2200 = SimpleIOClass()
        self.mcp2200.InitMCP2200(MCP2200_VID, MCP2200_PID)
        self.update_devices_list()
        self.mcp2200.SelectDevice(0)
        self.load_device()

    def update_devices_list(self):
        lst = QtCore.QStringListModel()
        lst.setStringList([self.mcp2200.GetDeviceInfo(x) for x in range(self.mcp2200.GetNoOfDevices())])
        self.lv_devices.setModel(lst)

    @Slot(int)
    def select_device(self, index):
        self.mcp2200.SelectDevice(index.row())
        self.load_device()
        
    def load_device(self):
        config = self.mcp2200.device.read_all()
        self.io_config.setText('{0:08b}'.format(config['IO_bmap']))
        self.output_default.setText('{0:08b}'.format(config['IO_Default_Val_bmap']))

        divisor = config['Baud_H']*256 + config['Baud_L']
        baud_rate = 12000000 / (divisor+1)
        rates = []
        for i in range(self.baud_rate.count()):
            rates.append(abs(int(self.baud_rate.itemText(i)) - baud_rate))

        self.baud_rate.setCurrentIndex(rates.index(min(rates)))

        self.enable_cts_rts_pins.setChecked(config['Config_Alt_Options'] & 0x01)
        self.enable_rx_led.setChecked(config['Config_Alt_Pins'] & 0x08)
        self.enable_tx_led.setChecked(config['Config_Alt_Pins'] & 0x04)
        self.enable_usbcfg_pin.setChecked(config['Config_Alt_Pins'] & 0x40)
        self.enable_suspend_pin.setChecked(config['Config_Alt_Pins'] & 0x80)
        # self.invert_uart_polarity.setChecked(config['Config_Alt_Options'] & 0x02)
        self.rb_leds_blink.setChecked(config['Config_Alt_Options'] & 0x80 == 0x00)
        self.rb_leds_toggle.setChecked(config['Config_Alt_Options'] & 0x80 == 0x80)
        self.rb_leds_100ms.setChecked(config['Config_Alt_Options'] & 0x20 == 0x00)
        self.rb_leds_200ms.setChecked(config['Config_Alt_Options'] & 0x20 == 0x20)
    
    @Slot(int)
    def configure_device(self, *args, **kwargs):
        self.mcp2200.ConfigureIoDefaultOutput(int(self.io_config.text(), 2), int(self.output_default.text(), 2))

        self.mcp2200.fnSetBaudRate(int(self.baud_rate.currentText()))
        self.mcp2200.fnHardwareFlowControl(self.enable_cts_rts_pins.isChecked())
        if self.enable_rx_led.isChecked():
            if self.rb_leds_toggle.isChecked():
                self.mcp2200.fnRxLED(cdtx.mcp2200.api.TOGGLE)
            elif self.rb_leds_blink.isChecked():
                if self.rb_leds_100ms.isChecked():
                    self.mcp2200.fnRxLED(cdtx.mcp2200.api.BLINKFAST)
                else:
                    self.mcp2200.fnRxLED(cdtx.mcp2200.api.BLINKSLOW)
        else:
            self.mcp2200.fnRxLED(cdtx.mcp2200.api.OFF)

        if self.enable_tx_led.isChecked():
            if self.rb_leds_toggle.isChecked():
                self.mcp2200.fnTxLED(cdtx.mcp2200.api.TOGGLE)
            elif self.rb_leds_blink.isChecked():
                if self.rb_leds_100ms.isChecked():
                    self.mcp2200.fnTxLED(cdtx.mcp2200.api.BLINKFAST)
                else:
                    self.mcp2200.fnTxLED(cdtx.mcp2200.api.BLINKSLOW)
        else:
            self.mcp2200.fnTxLED(cdtx.mcp2200.api.OFF)

        self.mcp2200.fnULoad(self.enable_usbcfg_pin.isChecked())
        self.mcp2200.fnSuspend(self.enable_suspend_pin.isChecked())

        self.load_device()


    def build_gui(self):
        # Detected devices
        self.lv_devices = QtWidgets.QListView()
        self.lv_devices.setMinimumHeight(50)
        self.lv_devices.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lv_devices.activated.connect(self.select_device)
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
        self.baud_rate.addItems(['300', '600', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        self.l_112.addWidget(self.baud_rate, 0, 0)
        self.l_112.addWidget(QtWidgets.QLabel('Baud Rate'), 0, 1)

        for _index, (_name, _value) in enumerate((
            ('enable_tx_led',    QtWidgets.QCheckBox('Enable Tx LED')),
            ('enable_rx_led',    QtWidgets.QCheckBox('Enable Rx LED')),
            ('enable_cts_rts_pins',  QtWidgets.QCheckBox('Enable CTS/RTS Pins')),
            ('enable_usbcfg_pin',    QtWidgets.QCheckBox('Enable USBCFG Pin')),
            ('enable_suspend_pin',   QtWidgets.QCheckBox('Enable Suspend Pin')),
            # ('invert_uart_polarity', QtWidgets.QCheckBox('Invert UART Polarity (UPOL)')),
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

        # Buttons
        self.bp_configure = QtWidgets.QPushButton('Configure')
        self.bp_configure.clicked.connect(self.configure_device)
        self.l_15.addWidget(self.bp_configure)



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
                # Butons
                ['l_15', QHBoxLayout, []
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
    
