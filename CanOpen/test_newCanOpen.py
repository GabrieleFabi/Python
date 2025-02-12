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

    def test_IdentityRo(self):
        # Attempt to write to the read-only object dictionary entry
        obj = self.node.sdo[0x1018]
        
        with self.assertRaises(canopen.SdoAbortedError) as cm:
            obj[1].raw = 0x1234
        
        # Check the error code
        self.assertEqual(cm.exception.code, 0x06010002)# Error code for attempt to write a read-only object
        
    def _test_checkErrorCode(self, index, subindex, errCode):
        # Attempt to write to the read-only object dictionary entry
        obj = self.node.sdo[index]
        
        with self.assertRaises(canopen.SdoAbortedError) as cm:
            obj[subindex].raw = 0x1234
        
        # Check the error code
        self.assertEqual(cm.exception.code, errCode)






if __name__ == '__main__':
    unittest.main()