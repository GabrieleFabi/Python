import unittest
import canopen


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
            if type(obj) == expected_type:
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

    
    def _check_download(self, value, index, subindex=0) -> bool:
        
        try:
            self.node.sdo.download(index, subindex, value)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
        
        
    def _check_readOnly(self, value, index, subindex=None) -> bool:

        try:
            obj = self.node.sdo[index] 
            if subindex is None:
                obj.raw = value
            else:               
                obj[index].raw = value
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return 0x06010002 == e.code

        return False
    
    
    def _check_readable(self, index, subindex=0) -> bool:

        try:
            self.node.sdo.upload(index, subindex)
            return True
        except canopen.SdoAbortedError as e:
            error_code = f"Code 0x{e.code:08X}"
            return False
    
    
    def _check_writable(self, value, index, subindex=None) -> bool:

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


    #start the tests

    def test_type(self):
        self.assertTrue(self._test_check_type(0x1018, canopen.sdo.base.SdoRecord))

    def test_upload(self):
        self.assertTrue(self._check_upload(0x6048))

    def test_download(self):
        self.assertTrue(self._check_download(b'\x00\x00', 0x6040)) #might have issues with indexes

    def test_read_only(self):
        self.assertTrue(self._check_readOnly(b'\x00\x00', 0x6043))

    def test_readable(self):
        self.assertTrue(self._check_readable(0x1018))
    
    def test_writable(self):
        self.assertTrue(self._check_writable(b'\x00\x00', 0x6046))


if __name__ == '__main__':
    unittest.main()