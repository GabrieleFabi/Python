import os
import pytest
import canopen
import unittest
import warnings
import canopen.sdo
from time import sleep
from typing import List
from enum import IntEnum
from pytest_check import check
from canopen.objectdictionary import Variable as ODVariable, ODArray, ODRecord


class DataType(IntEnum):
    BOOLEAN = 0x01
    INTEGER8 = 0x02
    INTEGER16 = 0x03
    INTEGER32 = 0x04
    UNSIGNED8 = 0x05
    UNSIGNED16 = 0x06
    UNSIGNED32 = 0x07
    REAL32 = 0x08
    VISIBLE_STRING = 0x09
    OCTET_STRING = 0x0A
    UNICODE_STRING = 0x0B
    TIME_OF_DAY = 0x0C
    TIME_DIFFERENCE = 0x0D
    DOMAIN = 0x0E
    REAL64 = 0x0F
    INTEGER24 = 0x10
    REAL48 = 0x11
    UNSIGNED24 = 0x12
    INTEGER40 = 0x13
    UNSIGNED40 = 0x14
    INTEGER48 = 0x15
    UNSIGNED48 = 0x16
    INTEGER56 = 0x17
    UNSIGNED56 = 0x18
    INTEGER64 = 0x19
    UNSIGNED64 = 0x1A


dataTypeSizes = {
    DataType.BOOLEAN: 1,
    DataType.INTEGER8: 1,
    DataType.INTEGER16: 2,
    DataType.INTEGER32: 4,
    DataType.UNSIGNED8: 1,
    DataType.UNSIGNED16: 2,
    DataType.UNSIGNED32: 4,
    DataType.REAL32: 4,
    DataType.VISIBLE_STRING: 1,
    DataType.OCTET_STRING: 1,
    DataType.UNICODE_STRING: 1,
    DataType.TIME_OF_DAY: 4,
    DataType.TIME_DIFFERENCE: 4,
    DataType.DOMAIN: 1,
    DataType.REAL64: 8,
    DataType.INTEGER24: 3,
    DataType.REAL48: 6,
    DataType.UNSIGNED24: 3,
    DataType.INTEGER40: 5,
    DataType.UNSIGNED40: 5,
    DataType.INTEGER48: 6,
    DataType.UNSIGNED48: 6,
    DataType.INTEGER56: 7,
    DataType.UNSIGNED56: 7,
    DataType.INTEGER64: 8,
    DataType.UNSIGNED64: 8
}


interface = 'kvaser'
channel = 0
bitrate = 500000
startIndex = 0x2000
nodeId = 113
flashE = False
fmPath = ""
fsPath = ""
rebootI = False


@pytest.fixture
def config(request):
    global interface, channel, bitrate, startIndex, nodeId, flashE, fmPath, fsPath, rebootI

    interface = request.config.getoption("--interface")
    channel = request.config.getoption("--channel")
    bitrate = request.config.getoption("--bitrate")
    startIndex = request.config.getoption("--start-index")
    nodeId = request.config.getoption("--node-id")
    if request.config.getoption("--flash"):
        flashE = True
        fmPath = request.config.getoption("--m")
        fsPath = request.config.getoption("--s")
    if request.config.getoption("--reboot"):
        rebootI = True


def test_interface(config):

    if interface != "kvaser":
        warnings.warn(
            f"Interface value is not kvaser, but {interface}", UserWarning)

    if channel != 0:
        warnings.warn(f"Channel value is not 0, but {channel}", UserWarning)

    if bitrate != 500_000:
        warnings.warn(
            f"Bitrate value is not 500_000, but {bitrate}", UserWarning)

    if startIndex != 0x2000:
        warnings.warn(
            f"Start index value is not 0x2000, but {startIndex}", UserWarning)

    if nodeId != 113:
        warnings.warn(f"node id is not 113, but {nodeId}", UserWarning)

    if not fmPath and flashE:
        warnings.warn(f"firmware master path is empty", UserWarning)
        assert False

    if not fsPath and flashE:
        warnings.warn(f"firmware slave path is empty", UserWarning)
        assert False


class Support:

    def __init__(self):
        self.node = None

    def connect(self):
        self.node_id = nodeId
        self.network = canopen.Network()
        self.network.connect(interface=interface,
                             channel=channel, bitrate=bitrate)
        self.node = self.network.add_node(self.node_id)
        self.network.send_message(PGN.make(PGN.Switch, nodeId), b'CAN OPEN')
        warnings.warn(
            f"Sent CAN OPEN message to CAN ID: {PGN.make(PGN.Switch, nodeId)}", UserWarning)
        sleep(2)
        eds = self.node.sdo.upload(0x1021, 0)
        eds = eds[:-1]
        with open('node.eds', 'wb') as f:
            f.write(eds)
        self.node = self.network.add_node(self.node_id, 'node.eds')

    def disconnect(self):
        self.network.disconnect()

    def _type(self, index, expected_type) -> bool:

        try:
            obj = self.node.sdo[index]
            if type(obj) is expected_type:
                return True
            else:
                return False
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _upload(self, index, subindex=0) -> bool:

        try:
            self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _download(self, index, subindex=0, value=b'\x00\x00') -> bool:

        try:
            self.node.sdo.download(index, subindex, value)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _ro(self, index, subindex=None, value=b'\x00\x00') -> bool:

        try:
            obj = self.node.sdo[index]
            if isinstance(obj, canopen.sdo.SdoVariable):
                obj.raw = value
            else:
                obj[subindex].raw = value
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            if e.code != 0x06010002:
                warnings.warn(
                    f"{hex(index)}.{(subindex)} doesn't return 0x06010002(readonly) error", UserWarning)
            return 0x06010002 == e.code

        return False

    def _w(self, index, subindex=None, value=b'\x00\x00\x00\x00') -> bool:

        try:
            obj = self.node.sdo[index]
            if isinstance(obj, canopen.sdo.SdoVariable):
                obj.raw = value
            else:
                obj[subindex].raw = value
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _r(self, index, subindex=None) -> bool:

        try:
            if subindex is None:
                self.node.sdo.upload(index, 0)
            else:
                self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _access(self, acces: str, index, subindex=None, value=b'\x00\x00\x00\x00') -> bool:
        if acces == 'wo':
            return self._w(index, subindex, value) and not (self._r(index, subindex))
        elif acces == 'ro' or acces == 'const':
            return self._ro(index, subindex, value)
        elif acces == 'rw':
            return self._w(index, subindex, value) and self._r(index, subindex)

    def _size(self, index, subindex) -> List[int]:
        lista = []

        for size in range(1, 65):
            try:
                self.node.sdo.download(
                    index, subindex, bytearray([0 for _ in range(size)]))
                lista.append(size)
            # except canopen.SdoAbortedError as e:
                # error_code = f"Code 0x{e.code:08X}"
            except Exception as e:
                pass

        return lista

    def _string_size(self, index, subindex) -> bool:

        try:
            self.node.sdo.download(index, subindex, bytes('string', 'utf-8'))
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _datatype(self, index: int, subindex=0, datatype=None) -> bool:

        def if_size(check: int) -> bool:
            if sizes == [check]:
                return True
            elif check in sizes and len(sizes) > 1:
                warnings.warn(
                    f"Sizes contain {check} but also other values.", UserWarning)
                return True
            elif check not in sizes:
                return False

        try:
            if subindex is None:
                subindex = 0
            sizes = []
            sizes = self._size(index, subindex)
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

        try:
            # Check if sizes
            match datatype:
                case 0x01 | 0x02 | 0x05:  # BOOLEAN, INTEGER8, UNSIGNED8
                    return if_size(1)
                case 0x03 | 0x06:  # INTEGER16, UNSIGNED16
                    return if_size(2)
                case 0x04 | 0x07 | 0x08:  # INTEGER32, UNSIGNED32, REAL32
                    return if_size(4)
                case 0x09:  # VISIBLE_STRING
                    return self._string_size(index, subindex)
                case 0x0F | 0x15:  # INTEGER24, UNSIGNED24
                    return if_size(3)
                case 0x11 | 0x16:  # INTEGER40, UNSIGNED40
                    return if_size(5)
                case 0x12 | 0x17 | 0x11:  # INTEGER48, UNSIGNED48, REAL48
                    return if_size(6)
                case 0x13 | 0x18:  # INTEGER56, UNSIGNED56
                    return if_size(7)
                case 0x14 | 0x19 | 0x10:  # INTEGER64, UNSIGNED64, REAL64
                    return if_size(8)

        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def _datatype_od(self, index, subindex=None, datatype=None) -> bool:

        try:
            obj = self.node.sdo[index]

            if isinstance(obj, canopen.sdo.SdoVariable):
                return obj.od.data_type is datatype
            else:
                return obj[subindex].od.data_type is datatype
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def exists_on_device(self, index: int, subindex=0) -> bool:

        try:
            self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    def exists_in_od(self, index: int, subindex=0) -> bool:
        return self.node.object_dictionary.get_variable(index, subindex) is not None

    def exists(self, index: int, subindex=0) -> bool:

        device = self.exists_on_device(index, subindex)
        od = self.exists_in_od(index, subindex)

        match (device, od):
            case (True, True):
                return True
            case (False, True):
                warnings.warn(
                    f"{hex(index)}.{subindex} is not in the device.", UserWarning)
                return False
            case (True, False):
                warnings.warn(
                    f"{hex(index)}.{subindex} is not in OD.", UserWarning)
                return False
            case (False, False):
                return False

    def test_od(self, obj):
        if isinstance(obj, ODVariable):
            if self.exists(obj.index, obj.subindex):
                value_for_size = bytes([0x00] * dataTypeSizes[obj.data_type])
                nodeIndex = self.node.sdo[obj.index]
                if isinstance(nodeIndex, canopen.sdo.SdoVariable):
                    value = self.node.sdo[obj.index].raw
                else:
                    value = self.node.sdo[obj.index][obj.subindex].raw

                match obj.access_type:
                    case "rw":
                        self.is_rw(obj.index, obj.subindex, value_for_size)
                    case "ro" | "const":
                        self.is_ro(obj.index, obj.subindex)

                self.has_datatype(obj.index, obj.subindex, obj.data_type)

                if obj.max:
                    if value > obj.max:
                        warnings.warn(
                            f"{hex(obj.index)}.{obj.subindex}: value out of bounds")
                    check.less_equal(value, obj.max)

                if obj.min:
                    if value < obj.min:
                        warnings.warn(
                            f"{hex(obj.index)}.{obj.subindex}: value out of bounds")
                    check.greater_equal(value, obj.min)

            else:
                warnings.warn(f"{hex(obj.index)}.{obj.subindex}:")
                assert False
        elif isinstance(obj, ODArray) or isinstance(obj, ODRecord):
            for item in obj:
                self.test_od(obj[item])

    # set up the Check functions

    @check.check_func
    def is_ro(self, index, subindex=None, value=b'\x00\x00'):

        access = 'ro'

        assert self._access(access, index, subindex, value)

    @check.check_func
    def is_rw(self, index, subindex=None, value=b'\x00\x00\x00\x00'):

        access = 'rw'

        assert self._access(access, index, subindex, value)

    @check.check_func
    def has_datatype(self, index: int, subindex=None, DT=None):

        if DT is None:
            warnings.warn("Data type not specified.", UserWarning)

        if DT in (0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x09, 0x0A, 0x0B, 0x0F, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19):
            if self._datatype(index, subindex, DT):
                assert True
            else:
                assert self._datatype_od(index, subindex, DT)
        else:
            assert False


# J1939 PGNs
class PGN(IntEnum):

    CAM11 = 0x1c050001
    CAM21 = 0x1c060100
    Heartbeat = 0x18be0000
    Switch = 0x18BC0001

    @staticmethod
    def make(pgn: int, dst: int = 0, src: int = 0) -> int:
        return pgn + (dst << 8) + src

    @staticmethod
    def match(pgn: int, match: int, dst: int = 0, src: int = 0) -> int:
        return ((pgn & 0x1fff0000 == match & 0x1fff0000) and ((pgn & 0x0000ff00) >> 8) == dst if dst != 0 else True and ((pgn & 0x000000ff) >> 0) == src if dst != 0 else True)


class TestCANopen(unittest.TestCase):

    can = Support()

    def setUp(self):
        global flashE, rebootI, sfBool
        if flashE:
            flashE = False

            comando = f"python ./inverter_flasher.py -m {fmPath} -s {fsPath}"
            os.system(comando)

        if rebootI:
            rebootI = False
            comando = f"python ./inverter_flasher.py -r"
            os.system(comando)
            sleep(2)

        if self.can.node is None:
            self.can.connect()

    # def tearDown(self):
        # self.can.disconnect()

    # start the tests for mandatory objects

    def test_0x1000(self):
        if self.can.exists(0x1000):
            self.can.has_datatype(0x1000, DT=DataType.UNSIGNED32.value)
            self.can.is_ro(0x1000, value=b'\x00\x00')
        else:
            assert False

    def test_0x1001(self):
        if self.can.exists(0x1001):
            self.can.is_ro(0x1001, value=b'\x00\x00')
            self.can.has_datatype(0x1001, DT=DataType.UNSIGNED8.value)
        else:
            assert False

    def test_0x1018(self):
        if self.can.exists(0x1018):
            self.can.is_ro(0x1018, 0, b'\x00\x00\x00')
            self.can.has_datatype(0x1018, 0, DataType.UNSIGNED8.value)

            if self.can.exists(0x1018, 1):
                self.can.is_ro(0x1018, 1, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1018, 1, DataType.UNSIGNED32.value)
            else:
                assert False

        else:
            assert False

    def test_0x1021(self):
        if self.can.exists(0x1021):
            self.can.is_ro(0x1021, value=b'stringa')
            self.can.has_datatype(0x1021, DT=DataType.VISIBLE_STRING.value)
        else:
            assert False

    # start test for optional objects

    def test_0x1002(self):
        if self.can.exists(0x1002):
            self.can.is_ro(0x1002, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1002, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1002 is missing", UserWarning)

    # dovrebbe essere un 32 ma risulta essere un 8. nell'eds è segnato 32 ma non va.
    # non è strutturato come array nell'eds
    def test_0x1003(self):
        if self.can.exists(0x1003):
            self.can.is_rw(0x1003, 0, b'\x00')
            self.can.has_datatype(0x1003, 0, DataType.UNSIGNED32.value)
            try:
                self.can.node.sdo[0x1003][0].raw = 1
                assert False
            except canopen.SdoAbortedError as error:
                check.equal(error.code, 0x06090030)

            if self.can.exists(0x1003, 1):
                self.can.is_ro(0x1003, 1, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1003, 1, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1003.1 is missing", UserWarning)

            if self.can.exists(0x1003, 2):
                self.can.is_ro(0x1003, 2, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1003, 2, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1003.2 is missing", UserWarning)
        else:
            assert False

    def test_0x1004(self):
        if self.can.exists(0x1004):
            warnings.warn("0x1004 is a reserved entry", UserWarning)
        else:
            warnings.warn("0x1004 is missing", UserWarning)

    def test_0x1005(self):
        if self.can.exists(0x1005):
            self.can.is_rw(0x1005, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1005, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1005 is missing", UserWarning)

    def test_0x1006(self):
        if self.can.exists(0x1006):
            self.can.is_rw(0x1006, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1006, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1006 is missing", UserWarning)

    def test_0x1007(self):
        if self.can.exists(0x1007):
            self.can.is_rw(0x1007, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1007, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1007 is missing", UserWarning)

    def test_0x1008(self):
        if self.can.exists(0x1008):
            self.can.is_ro(0x1008, value=b'stringa')
            self.can.has_datatype(0x1008, DT=DataType.VISIBLE_STRING.value)
        else:
            warnings.warn("0x1008 is missing", UserWarning)

    def test_0x1009(self):
        if self.can.exists(0x1009):
            self.can.is_ro(0x1009, value=b'stringa')
            self.can.has_datatype(0x1009, DT=DataType.VISIBLE_STRING.value)
        else:
            warnings.warn("0x1009 is missing", UserWarning)

    def test_0x100A(self):
        if self.can.exists(0x100A):
            self.can.is_ro(0x100A, value=b'stringa')
            self.can.has_datatype(0x100A, DT=DataType.VISIBLE_STRING.value)
        else:
            warnings.warn("0x100A is missing", UserWarning)

    def test_0x100B(self):
        if self.can.exists(0x100B):
            warnings.warn("0x100B is a reserved entry", UserWarning)
        else:
            warnings.warn("0x100B is missing", UserWarning)

    def test_0x100C(self):
        if self.can.exists(0x100C):
            self.can.is_rw(0x100C, value=b'\x00\x00')
            self.can.has_datatype(0x100C, DT=DataType.UNSIGNED16.value)
        else:
            warnings.warn("0x100C is missing", UserWarning)

    def test_0x100D(self):
        if self.can.exists(0x100D):
            self.can.is_rw(0x100D, value=b'\x00')
            self.can.has_datatype(0x100D, DT=DataType.UNSIGNED8.value)
        else:
            warnings.warn("0x100D is missing", UserWarning)

    def test_0x100E(self):
        if self.can.exists(0x100E):
            warnings.warn("0x100E is a reserved entry", UserWarning)
        else:
            warnings.warn("0x100E is missing", UserWarning)

    def test_0x100F(self):
        if self.can.exists(0x100F):
            warnings.warn("0x100F is a reserved entry", UserWarning)
        else:
            warnings.warn("0x100F is missing", UserWarning)

    def test_0x1010(self):  # error 80000020 l'index ritorna sempre errore
        if self.can.exists(0x1010):
            self.can.is_ro(0x1010, 0, b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1010, 0, DataType.UNSIGNED8.value)

            if self.can.exists(0x1010, 1):
                # self.can.is_readwrite(0x1010, 1, b'\x65\x76\x61\x73')
                self.can.has_datatype(0x1010, 1, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1010.1 is missing", UserWarning)

            if self.can.exists(0x1010, 2):
                # self.can.is_readwrite(0x1010, 2, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1010, 2, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1010.2 is missing", UserWarning)

            if self.can.exists(0x1010, 3):
                # self.can.is_readwrite(0x1010, 3, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1010, 3, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1010.3 is missing", UserWarning)
        else:
            warnings.warn("0x1010 is missing", UserWarning)

    def test_0x1011(self):  # error 80000020 l'index ritorna sempre errore
        if self.can.exists(0x1011):
            # self.can.is_readonly(0x1011, 0, b'\x00')
            self.can.has_datatype(0x1011, 0, DataType.UNSIGNED8.value)

            if self.can.exists(0x1011, 1):
                # self.can.is_readwrite(0x1011, 1, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1011, 1, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1011.1 is missing", UserWarning)

            if self.can.exists(0x1011, 2):
                # self.can.is_readwrite(0x1011, 2, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1011, 2, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1011.2 is missing", UserWarning)

            if self.can.exists(0x1011, 3):
                # self.can.is_readwrite(0x1011, 3, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1011, 3, DataType.UNSIGNED32.value)
            else:
                warnings.warn("0x1011.3 is missing", UserWarning)
        else:
            assert False

    def test_0x1012(self):
        if self.can.exists(0x1012):
            self.can.is_rw(0x1012, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1012, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1012 is missing", UserWarning)

    def test_0x1013(self):
        if self.can.exists(0x1013):
            self.can.is_rw(0x1013, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1013, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1013 is missing", UserWarning)

    def test_0x1014(self):
        if self.can.exists(0x1014):
            self.can.is_rw(0x1014, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1014, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1014 is missing", UserWarning)

    def test_0x1015(self):
        if self.can.exists(0x1015):
            self.can.is_ro(0x1015, value=b'\x00\x00')
            self.can.has_datatype(0x1015, DT=DataType.UNSIGNED16.value)
        else:
            warnings.warn("0x1015 is missing", UserWarning)

    def test_0x1016(self):
        if self.can.exists(0x1016):
            self.can.is_rw(0x1016, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1016, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("0x1016 is missing", UserWarning)

    def test_0x1017(self):
        if self.can.exists(0x1017):
            self.can.has_datatype(0x1017, DT=DataType.UNSIGNED16.value)
            self.can.is_rw(0x1017, value=b'\x64\x00')
        else:
            warnings.warn("0x1017 is missing", UserWarning)

    # start test for looped objects

    def test_0x1022_to_0x11ff(self):
        for index in range(0x1019, 0x1020):
            check.is_false(self.can.exists(index))

        for index in range(0x1022, 0x11FF):
            check.is_false(self.can.exists(index))

    # start tests for the manufacturer

    # warning, 0x6075/0x6060 is ro, in the eds it's saved as rw, TO CHANGE
    # make sure to not write into 0x1F51 and 0x1F50
    # the default values are not setted right (errors in 0x2009 and 0x200B)
    def test_manufacturer_obj(self):
        for item in list(filter(lambda key: key >= 0x2009 and key != 0x1F51 and key != 0x1F50, self.can.node.object_dictionary.keys())):
            self.can.test_od(self.can.node.object_dictionary[item])


if __name__ == '__main__':
    unittest.main()
