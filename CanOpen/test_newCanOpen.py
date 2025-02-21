from typing import List
import unittest
import warnings
import canopen
from pytest_check import check, is_false, is_true


class TestCANopen(unittest.TestCase):

    def setUp(self):
        self.node_id = 113
        self.network = canopen.Network()
        self.network.connect(interface='kvaser', channel=0, bitrate=500000)
        self.node = self.network.add_node(self.node_id, 'C:/Users/g.fabi/Test/CanOpen/eds_data.eds')

    def tearDown(self):
        self.network.disconnect()


    #set up the test logic

    def _test_check_type(self, index, expected_type) -> bool:

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
    
    def check_access(self, acces: str, index, subindex=None, value=b'\x00\x00') -> bool:
        if acces == 'wo':
            return self.is_writable(index, subindex, value) and not (self.is_readable(index, subindex))     
        elif acces == 'ro' or acces == 'const':
            return self._check_readOnly(index, subindex, value)
        elif acces == 'rw':
            return self.is_writable(index, subindex, value) and self.is_readable(index, subindex)
      
    
    
    def is_readable(self, index, subindex=None) -> bool:

        try:
            if subindex is None:
                self.node.sdo.upload(index, 0)
            else:
                self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
    
    
    def is_writable(self, index, subindex=None, value=0) -> bool:

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


    def command_bytes(self, command: int, index: int, subindex: int, data: bytearray) -> bytearray:
        result = bytearray([command, index & 0xFF, (index >> 8) & 0xFF, subindex])
        result.extend(data)
        return result
    
    
    def check_size(self, index, subindex) -> List[int]:
        lista = []
        
        for size in range(1, 65):
            try:
                self.node.sdo.download(index, subindex, bytearray([0 for _ in range(size)]))
                lista.append(size)
            except canopen.SdoAbortedError as e: 
                error_code = f"Code 0x{e.code:08X}"
                pass
        
        return lista
    

    def check_string_size(self, index, subindex) -> bool:

        try:
            self.node.sdo.download(index, subindex, bytearray(b'string', 'utf-8'))
            return True
        except canopen.SdoAbortedError as e: 
            error_code = f"Code 0x{e.code:08X}"
            return False

    
    def check_datatype_size(self, datatype: int, index: int, subindex=0) -> bool:
        
        def if_check_size(check: int) -> bool:
            if sizes == [check]:
                return True
            elif check in sizes and len(sizes) > 1:
                warnings.warn(f"Sizes contain {check} but also other values.")
                return True
            elif check not in sizes:
                return False
            
        try:
            sizes = []
            sizes = self.check_size(index, subindex)
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
                    return self.check_string_size(index, subindex)
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

        
    def check_datatype_from_od(self, index, subindex=None, datatype=None) -> bool:
            
            try:
                obj = self.node.sdo[index]
                if subindex is None:
                    return obj.od.data_type is datatype
                else:
                    return obj[subindex].od.data_type is datatype
            except canopen.SdoAbortedError as e:
                error_code = f"Code 0x{e.code:08X}"
                return False

            
        

    #start the tests

    def test_type(self):
        self.assertTrue(self._test_check_type(0x1018, canopen.sdo.base.SdoRecord))

    def test_upload(self):
        self.assertTrue(self._check_upload(0x6048))

    def test_download(self):
        self.assertTrue(self._check_download(0x6040)) #might have issues with indexes

    def test_read_only(self):
        self.assertTrue(self._check_readOnly(0x6043))

    def test_readable(self):
        self.assertTrue(self.is_readable(0x6040))
    
    def test_writable(self):
        self.assertTrue(self.is_writable(0x6046, 1, 0x123))

    def test_build_bytearray(self):
        self.command_bytes(0x2F, 0x1080, 0x01, bytearray([0x00]))

    def test_check_size(self):
        print(self.check_size(0x6048, 1))
        
    def test_check_single_size(self):
        self.assertTrue(self.check_datatype_size(0x03, 0x6042))



    #start the tests for mandatory objects

    def test_0x1000_access(self):
        self.assertTrue(self.check_access('ro', 0x1000, value=b'\x00\x00'))
    
    def test_0x1000_check_datatype_from_od(self):
        self.assertTrue(self.check_datatype_from_od(0x1000, datatype=0x07))

    def test_0x1001_access(self):
        self.assertTrue(self.check_access('ro', 0x1001, value=b'\x00\x00'))  

    def test_0x1001_check_datatype_from_od(self):
        self.assertTrue(self.check_datatype_from_od(0x1001, datatype=0x05))

    def test_0x1018_0_access(self):
        self.assertTrue(self.check_access('ro', 0x1018, 0, b'\x00\x00'))
    
    def test0x1018_0_check_datatype_from_od(self):
        self.assertTrue(self.check_datatype_from_od(0x1018, 0, 0x05))
    
    def test_0x1018_1_access(self):
        self.assertTrue(self.check_access('ro', 0x1018, 1, b'\x00\x00'))
    
    def test0x1018_1_check_datatype_from_od(self):
        self.assertTrue(self.check_datatype_from_od(0x1018, 1, 0x07))

    def test_0x1021_access(self):
        self.assertTrue(self.check_access('const', 0x1021, value=b'\x00\x00'))
    
    def test_0x1021_check_datatype_from_od(self):
        self.assertTrue(self.check_datatype_from_od(0x1021, datatype=0x09))
    
    

    def test_pytest_check_1018(self):
        check.is_true(self.check_access('ro', 0x1018, 0, b'\x00\x00'), "access is not read only")
        check.is_true(self.check_datatype_from_od(0x1018, 0, 0x05), "datatype is not correct")
        check.is_true(self.check_access('ro', 0x1018, 1, b'\x00\x00'), "access is not read only")
        check.is_true(self.check_datatype_from_od(0x1018, 1, 0x07), "datatype is not correct")
        

    
    
        
if __name__ == '__main__':
    unittest.main()