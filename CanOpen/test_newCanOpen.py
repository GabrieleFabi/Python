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

       
            
    def _check_Ro(self, index, subindex, value):
        # Attempt to write to the read-only object dictionary entry
        obj = self.node.sdo[index]      

        try:
            obj[subindex].raw = value
        except canopen.SdoAbortedError as e:
            return 0x06010002 == e.code

        return False


    def _check_error_upload(self, index, subindex, error) -> bool:

        # Check the error code
        try:
            self.node.sdo.upload(index, subindex)
        except canopen.SdoAbortedError as e:
            return error == e.code

        return False
        


    def _check_error_download(self, index, subindex, value, error) -> bool:
        
        # Check the error code
        try:
            self.node.sdo.download(index, subindex, value)
        except canopen.SdoAbortedError as e:
            return error == e.code

        return False

    def _test_checkType(self, index, expected_type):
        obj = self.node.sdo[index]
        self.assertEqual(type(obj), expected_type)

    def test_ErrorCode(self):
        self._test_checkErrorCode(0x1018, 1, 0x06010002)

    def test_Type(self):
        self._test_checkType(0x1018, canopen.sdo.base.SdoRecord)

    def test_ErrorUpload(self):
        self.assertTrue(self._check_error_upload(0x1012, 0, 0x06020000))

    def test_ErrorDownload(self):
        self.assertTrue(self._check_error_download(0x1012, 0, b'\x00\x00', 0x06020000))

    def test_IdentityRo(self):
        self.assertTrue(self._check_Ro(0x1018, 1, 0x1234))

        

if __name__ == '__main__':
    unittest.main()