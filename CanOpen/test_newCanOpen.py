from typing import List
import unittest
import warnings
import canopen
from canopen.objectdictionary import Variable as ODVariable, ODArray, ODRecord
import canopen.sdo
from pytest_check import check, is_false, is_true
from enum import IntEnum

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

class CanOpenSupport:
    def __init__(self, node: int, eds_path: str):
        self.node_id = node
        self.network = canopen.Network()
        self.network.connect(interface='kvaser', channel=0, bitrate=500000)
        self.node = self.network.add_node(self.node_id, eds_path)

    def disconnect(self):
        self.network.disconnect()

    def _check_type(self, index, expected_type) -> bool:

        try:
            obj = self.node.sdo[index]
            if type(obj) is expected_type:
                return True
            else:
                return False
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
        
    
    def _check_upload(self, index, subindex=0) -> bool:

        try:
            self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

    
    def _check_download(self, index, subindex=0, value=b'\x00\x00') -> bool:
        
        try:
            self.node.sdo.download(index, subindex, value)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
        
        
    def _check_readOnly(self, index, subindex=None, value=b'\x00\x00') -> bool:

        try:
            obj = self.node.sdo[index]
            if isinstance(obj, canopen.sdo.SdoVariable):
                obj.raw = value
            else:               
                obj[subindex].raw = value
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            if e.code != 0x06010002:
                warnings.warn(f"Index 0x{hex(index)}.{(subindex)} doesn't return 0x06010002(readonly) error", UserWarning)
            return 0x06010002 == e.code

        return False
    
    
    def _check_writeable(self, index, subindex=None, value=0) -> bool:

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
        
        
    def _check_readable(self, index, subindex=None) -> bool:

        try:
            if subindex is None:
                self.node.sdo.upload(index, 0)
            else:
                self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
        

    def _check_acces(self, acces: str, index, subindex=None, value=b'\x00\x00') -> bool:
        if acces == 'wo':
            return self._check_writeable(index, subindex, value) and not (self._check_readable(index, subindex))     
        elif acces == 'ro' or acces == 'const':
            return self._check_readOnly(index, subindex, value)
        elif acces == 'rw':
            return self._check_writeable(index, subindex, value) and self._check_readable(index, subindex)


    def _build_command_bytes(self, command: int, index: int, subindex: int, data: bytearray) -> bytearray:
        result = bytearray([command, index & 0xFF, (index >> 8) & 0xFF, subindex])
        result.extend(data)
        return result
    
    
    def _check_size(self, index, subindex) -> List[int]:
        lista = []
        
        for size in range(1, 65):
            try:
                self.node.sdo.download(index, subindex, bytearray([0 for _ in range(size)]))
                lista.append(size)
            except canopen.SdoAbortedError as e: 
                error_code = f"Code 0x{e.code:08X}"
                pass
        
        return lista
    

    def _check_string_size(self, index, subindex) -> bool:

        try:
            self.node.sdo.download(index, subindex, bytes('string', 'utf-8'))
            return True
        except canopen.SdoAbortedError as e: 
            error_code = f"Code 0x{e.code:08X}"
            return False

    
    def _check_datatype(self, index: int, subindex=0, datatype=None) -> bool:
        
        def if_check_size(check: int) -> bool:
            if sizes == [check]:
                return True
            elif check in sizes and len(sizes) > 1:
                warnings.warn(f"Sizes contain {check} but also other values.", UserWarning)
                return True
            elif check not in sizes:
                return False
            
        try:
            if subindex is None:
                subindex = 0
            sizes = []
            sizes = self._check_size(index, subindex)
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
        
        try:
            # Check if sizes
            match datatype:
                case 0x01 | 0x02 | 0x05:  # BOOLEAN, INTEGER8, UNSIGNED8
                    return if_check_size(1)
                case 0x03 | 0x06:  # INTEGER16, UNSIGNED16
                    return if_check_size(2)
                case 0x04 | 0x07 | 0x08:  # INTEGER32, UNSIGNED32, REAL32
                    return if_check_size(4)
                case 0x09: #VISIBLE_STRING
                    return self._check_string_size(index, subindex)
                case 0x0F | 0x15:  # INTEGER24, UNSIGNED24
                    return if_check_size(3) 
                case 0x11 | 0x16:  # INTEGER40, UNSIGNED40
                    return if_check_size(5)
                case 0x12 | 0x17:  # INTEGER48, UNSIGNED48
                    return if_check_size(6)
                case 0x13 | 0x18:  # INTEGER56, UNSIGNED56
                    return if_check_size(7)
                case 0x14 | 0x19 | 0x10:  # INTEGER64, UNSIGNED64, REAL64
                    return if_check_size(8)
                
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

        
    def _check_datatype_od(self, index, subindex=None, datatype=None) -> bool:
            
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
                warnings.warn(f"Index 0x{hex(index)} Subindex 0x{hex(subindex)} is not in the device.", UserWarning)
                return False
            case (True, False):
                warnings.warn(f"Index 0x{hex(index)} Subindex 0x{hex(subindex)} is not in s/oD/OD.", UserWarning)
                return False
            case (False, False):
                return False
            
    def _test_obj(self, obj):
        if isinstance(obj, ODVariable):
            if self.exists(obj.index, obj.subindex):   


                match obj.access_type:
                    case "rw":
                        self.is_readwrite(obj.index, obj.subindex)
                    case "ro" | "const":
                        self.is_readonly(obj.index, obj.subindex)

                self.has_datatype(obj.index, obj.subindex, obj.data_type)

                nodeIndex = self.node.sdo[obj.index]
                if obj.max:
                    if isinstance(nodeIndex, canopen.sdo.SdoVariable):
                        check.less_equal(nodeIndex.raw, obj.max)
                    else:
                        check.less_equal(nodeIndex[obj.subindex].raw, obj.max)

                if obj.min:
                    if isinstance(nodeIndex, canopen.sdo.SdoVariable):
                        check.greater_equal(nodeIndex.raw, obj.min)
                    else:
                        check.greater_equal(nodeIndex[obj.subindex].raw, obj.min)
            else:
                assert False
        elif isinstance(obj, ODArray) or isinstance(obj, ODRecord):
            for item in obj:
                self._test_obj(obj[item])

    #set up the Check functions 

    @check.check_func
    def is_readonly(self, index, subindex=None, value=b'\x00\x00'):

        access = 'ro'

        assert self._check_acces(access, index, subindex, value)


    @check.check_func
    def is_readwrite(self, index, subindex=None, value=b'\x00\x00'):

        access = 'rw'

        assert self._check_acces(access, index, subindex, value)


    @check.check_func
    def has_datatype(self, index: int, subindex=None, DT=None):

        if DT is None:
            warnings.warn("Data type not specified.", UserWarning)

        if DT in (0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x09, 0x0A, 0x0B, 0x0F, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19):
            if self._check_datatype(index, subindex, DT):
                assert True
            else:
                assert self._check_datatype_od(index, subindex, DT)
        else:
            assert False

    
class TestCANopen(unittest.TestCase):

    
    def setUp(self):
        self.can = CanOpenSupport(113, 'C:/Users/g.fabi/Test/CanOpen/eds_data.eds')

    def tearDown(self):
        self.can.disconnect()



    #start the tests for mandatory objects
    
    def test_0x1000(self):
        if self.can.exists(0x1000):
            self.can.has_datatype(0x1000, DT=DataType.UNSIGNED32.value)
            self.can.is_readonly(0x1000, value=b'\x00\x00')
        else:
            assert False
        

    def test_0x1001(self):
        if self.can.exists(0x1001):
            self.can.is_readonly(0x1001, value=b'\x00\x00')
            self.can.has_datatype(0x1001, DT=DataType.UNSIGNED8.value)
        else:
            assert False

    def test_0x1018(self):
        if self.can.exists(0x1018):
            self.can.is_readonly(0x1018, 0, b'\x00\x00\x00')
            self.can.has_datatype(0x1018, 0, DataType.UNSIGNED8.value)

            if self.can.exists(0x1018, 1):
                self.can.is_readonly(0x1018, 1, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1018, 1, DataType.UNSIGNED32.value)
            else:
                assert False

        else:
            assert False    
        
    def test_0x1021(self):
        if self.can.exists(0x1021):
            self.can.is_readonly(0x1021, value=b'stringa')
            self.can.has_datatype(0x1021, DT=DataType.VISIBLE_STRING.value)
        else:
            assert False


    #start test for optional objects

    def test_0x1002(self):
        if self.can.exists(0x1002):
            self.can.is_readonly(0x1002, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1002, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("Index 0x1002 is missing", UserWarning)
            

    def test_0x1003(self):
        if self.can.exists(0x1003):
            self.can.is_readwrite(0x1003, 0, b'\x00')
            self.can.has_datatype(0x1003, 0, DataType.UNSIGNED8.value)
            try:
                self.can.node.sdo[0x1003][0].raw = 1
                assert False
            except canopen.SdoAbortedError as error:
                check.equal(error.code, 0x06090030)

            if self.can.exists(0x1003, 1):
                self.can.is_readonly(0x1003, 1, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1003, 1, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1003, subindex 1 is missing", UserWarning)
            
            if self.can.exists(0x1003, 2):
                self.can.is_readonly(0x1003, 2, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1003, 2, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1003, subindex 2 is missing", UserWarning)
        else:
            assert False
    
    def test_0x1004(self):
        if self.can.exists(0x1004):
            warnings.warn("Index 0x1004 is a reserved entry", UserWarning)
        else:
            warnings.warn("Index 0x1004 is missing", UserWarning)

    def test_0x1005(self):
        if self.can.exists(0x1005):
            self.can.is_readwrite(0x1005, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1005, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("Index 0x1005 is missing", UserWarning)

    def test_0x1006(self):
        if self.can.exists(0x1006):
            self.can.is_readwrite(0x1006, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1006, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("Index 0x1006 is missing", UserWarning)
    
    def test_0x1007(self):
        if self.can.exists(0x1007):
            self.can.is_readwrite(0x1007, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1007, DT=DataType.UNSIGNED32.value)
        else:    
            warnings.warn("Index 0x1007 is missing", UserWarning)

    def test_0x1008(self):
        if self.can.exists(0x1008):
            self.can.is_readonly(0x1008, value=b'stringa')
            self.can.has_datatype(0x1008, DT=DataType.VISIBLE_STRING.value)
        else:
            warnings.warn("Index 0x1008 is missing", UserWarning)
    
    def test_0x1009(self):
        if self.can.exists(0x1009):
            self.can.is_readonly(0x1009, value=b'stringa')
            self.can.has_datatype(0x1009, DT=DataType.VISIBLE_STRING.value)
        else:
            warnings.warn("Index 0x1009 is missing", UserWarning)

    def test_0x100A(self):
        if self.can.exists(0x100A):
            self.can.is_readonly(0x100A, value=b'stringa')
            self.can.has_datatype(0x100A, DT=DataType.VISIBLE_STRING.value)
        else:
            warnings.warn("Index 0x100A is missing", UserWarning)

    def test_0x100B(self):
        if self.can.exists(0x100B):
            warnings.warn("Index 0x100B is a reserved entry", UserWarning)
        else:
            warnings.warn("Index 0x100B is missing", UserWarning)
    
    def test_0x100C(self):
        if self.can.exists(0x100C):
            self.can.is_readwrite(0x100C, value=b'\x00\x00')
            self.can.has_datatype(0x100C, DT=DataType.UNSIGNED16.value)
        else:
            warnings.warn("Index 0x100C is missing", UserWarning)
        
    def test_0x100D(self):
        if self.can.exists(0x100D):
            self.can.is_readwrite(0x100D, value=b'\x00')
            self.can.has_datatype(0x100D, DT=DataType.UNSIGNED8.value)
        else:
            warnings.warn("Index 0x100D is missing", UserWarning)
    
    def test_0x100E(self):
        if self.can.exists(0x100E):
            warnings.warn("Index 0x100E is a reserved entry", UserWarning)
        else:
            warnings.warn("Index 0x100E is missing", UserWarning)
    
    def test_0x100F(self):
        if self.can.exists(0x100F):
            warnings.warn("Index 0x100F is a reserved entry", UserWarning)
        else:
            warnings.warn("Index 0x100F is missing", UserWarning)
    
    def test_0x1010(self): #error 80000020 l'index ritorna sempre errore
        if self.can.exists(0x1010): 
            self.can.is_readonly(0x1010, 0, b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1010, 0, DataType.UNSIGNED8.value)

            if self.can.exists(0x1010, 1):
                #self.can.is_readwrite(0x1010, 1, b'\x65\x76\x61\x73')
                self.can.has_datatype(0x1010, 1, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1010, subindex 1 is missing", UserWarning)

            if self.can.exists(0x1010, 2):
                #self.can.is_readwrite(0x1010, 2, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1010, 2, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1010, subindex 2 is missing", UserWarning)

            if self.can.exists(0x1010, 3):
                #self.can.is_readwrite(0x1010, 3, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1010, 3, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1010, subindex 3 is missing", UserWarning)
        else:
            warnings.warn("Index 0x1010 is missing", UserWarning)

    def test_0x1011(self): #error 80000020 l'index ritorna sempre errore
        if self.can.exists(0x1011):
            #self.can.is_readonly(0x1011, 0, b'\x00')
            self.can.has_datatype(0x1011, 0, DataType.UNSIGNED8.value)

            if self.can.exists(0x1011, 1):
                #self.can.is_readwrite(0x1011, 1, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1011, 1, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1011, subindex 1 is missing", UserWarning)

            if self.can.exists(0x1011, 2):
                #self.can.is_readwrite(0x1011, 2, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1011, 2, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1011, subindex 2 is missing", UserWarning)

            if self.can.exists(0x1011, 3):
                #self.can.is_readwrite(0x1011, 3, b'\x00\x00\x00\x00')
                self.can.has_datatype(0x1011, 3, DataType.UNSIGNED32.value)
            else:
                warnings.warn("Index 0x1011, subindex 3 is missing", UserWarning)
        else:
            assert False
    
    def test_0x1012(self):
        if self.can.exists(0x1012):
            self.can.is_readwrite(0x1012, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1012, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("Index 0x1012 is missing", UserWarning)
    
    def test_0x1013(self):
        if self.can.exists(0x1013):
            self.can.is_readwrite(0x1013, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1013, DT=DataType.UNSIGNED32.value)
        else:
           warnings.warn("Index 0x1013 is missing", UserWarning)

    def test_0x1014(self):
        if self.can.exists(0x1014):
            self.can.is_readwrite(0x1014, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1014, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("Index 0x1014 is missing", UserWarning)

    def test_0x1015(self):
        if self.can.exists(0x1015):
            self.can.is_readonly(0x1015, value=b'\x00\x00')
            self.can.has_datatype(0x1015, DT=DataType.UNSIGNED16.value)
        else:
            warnings.warn("Index 0x1015 is missing", UserWarning)

    def test_0x1016(self):
        if self.can.exists(0x1016):
            self.can.is_readwrite(0x1016, value=b'\x00\x00\x00\x00')
            self.can.has_datatype(0x1016, DT=DataType.UNSIGNED32.value)
        else:
            warnings.warn("Index 0x1016 is missing", UserWarning)   

    def test_0x1017(self):
        if self.can.exists(0x1017):
            self.can.is_readwrite(0x1017, value=b'\x00\x00')
            self.can.has_datatype(0x1017, DT=DataType.UNSIGNED16.value)
        else:
            warnings.warn("Index 0x1017 is missing", UserWarning)

    #start test for looped objects

    def test_0x1022_to_0x11ff(self):
        for index in range(0x1019, 0x1020):
            check.is_false(self.can.exists(index))

        for index in range(0x1022, 0x11FF):
            check.is_false(self.can.exists(index))

        
    #start tests from OD

    def test_general_obj(self):
        for item in list(filter(lambda key: key >= 0x2004, self.can.node.object_dictionary.keys())):
            self.can._test_obj(self.can.node.object_dictionary[item])

        
    

if __name__ == '__main__':
    unittest.main()