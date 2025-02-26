from typing import List
import unittest
import warnings
import canopen
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

class TestCANopen(unittest.TestCase):

    def setUp(self):
        self.node_id = 113
        self.network = canopen.Network()
        self.network.connect(interface='kvaser', channel=0, bitrate=500000)
        self.node = self.network.add_node(self.node_id, 'C:/Users/g.fabi/Test/CanOpen/eds_data.eds')

    def tearDown(self):
        self.network.disconnect()


    
    #set up the test logic

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
            if subindex is None:
                obj.raw = value
            else:               
                obj[subindex].raw = value
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return 0x06010002 == e.code

        return False
    

    def _check_acces(self, acces: str, index, subindex=None, value=b'\x00\x00') -> bool:
        if acces == 'wo':
            return self.is_writable(index, subindex, value) and not (self.is_readable(index, subindex))     
        elif acces == 'ro' or acces == 'const':
            return self._check_readOnly(index, subindex, value)
        elif acces == 'rw':
            return self._check_writeable(index, subindex, value) and self._check_readable(index, subindex)
      
    
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
    
    
    def _check_writeable(self, index, subindex=None, value=0) -> bool:

        try:
            obj = self.node.sdo[index] 
            if subindex is None:
                obj.raw = value
            else: 
                obj[subindex].raw = value
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False


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
                warnings.warn(UserWarning, f"Sizes contain {check} but also other values.")
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
            if subindex is None:
                return obj.od.data_type is datatype
            else:
                return obj[subindex].od.data_type is datatype
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False

            

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
    def is_variable(self, index, subindex=None, DT=None):

        if DT is None:
            warnings.warn(UserWarning, "Data type not specified.")

        if DT in (0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x0F, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19):

            if self._check_datatype(index, subindex, DT):
                assert True
            else:
                assert self._check_datatype_od(index, subindex, DT)                       
        else:
            assert False
            

    @check.check_func
    def is_bool(self, index, subindex=None, DT=None):

        if DT is None:
            warnings.warn(UserWarning, "Data type not specified.")

        if DT is 0x01:
            assert self._check_datatype_od(index, subindex, DT)
        else:
            assert False

    @check.check_func
    def is_string(self, index, subindex=None, DT=None):

        if DT is None:
            warnings.warn(UserWarning, "Data type not specified.")

        if DT in (0x09, 0x0A, 0x0B):

            if self._check_datatype(index, subindex, DT):
                assert True
            else:
                assert self._check_datatype_od(index, subindex, DT) 
        else:
            assert False



    #start the debug tests

    def test_download(self):
        self.assertTrue(self._check_download(0x6040)) #might have issues with indexes
   

    #start the tests for mandatory objects
    
    def test_1000(self):
        self.is_variable(0x1000, DT=DataType.UNSIGNED32.value)
        self.is_readonly(0x1000, value=b'\x00\x00')

    def test_1001(self):
        self.is_readonly(0x1001, value=b'\x00\x00')
        self.is_variable(0x1001, DT=DataType.UNSIGNED8.value)

    def test_1018(self):
        self.is_readonly(0x1018, 0, b'\x00\x00')
        self.is_variable(0x1018, 0, DataType.UNSIGNED8.value)
        self.is_readonly(0x1018, 1, b'\x00\x00')
        self.is_variable(0x1018, 1, DataType.UNSIGNED32.value)
        
    def test_1021(self):
        self.is_readonly(0x1021, value=b'\x00\x00') 
        self.is_string(0x1021, DT=DataType.VISIBLE_STRING.value) 


    #start test for optional objects

    def test_6040(self):
        self.is_variable(0x6040, DT=DataType.UNSIGNED16.value)
        self.is_readwrite(0x6040, value=b'\x00\x00')
    
    
        
if __name__ == '__main__':
    unittest.main()