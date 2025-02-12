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

    def _test_r(self, index, subindex, expected=None) -> bool:
        value = None
        try:
            value = int.from_bytes(self.node.sdo.upload(index, subindex), 'little')
        except Exception as e:
            self.fail(f"Reading 0x{hex(index)}.{subindex} failed: {e}")
        if expected is not None:
            self.assertEqual(value, expected, f"{hex(index)}.{subindex} read failed")

    def _test_ro(self, index, subindex) -> bool:
        try:
            value = self.node.sdo.upload(index, subindex)
            self.node.sdo.download(index, subindex, value)
        except Exception as e:
            e = e
            self.assertTrue(True, f"{hex(index)}.{subindex} readonly failed")
            return
        self.assertTrue(False, f"{hex(index)}.{subindex} readonly failed")

    def _test_w(self, index, subindex, value=0) -> bool:
        value = None
        try:
            read = self.node.sdo.upload(index, subindex)
            self.node.sdo.download(index, subindex, read)
        except Exception as e:
            self.fail(f"{hex(index)}.{subindex} write failed: {e}")
        self.assertEqual(value, read, f"{hex(index)}.{subindex} write failed")

    def test_download_eds(self):
        # Read EDS file size from Object Dictionary
        result = ""
        try:
            sdo_client = canopen.sdo.SdoClient(0x600 + self.node_id, 0x580 + self.node_id, canopen.objectdictionary.ObjectDictionary())
            sdo_client.network = self.network
            self.network.subscribe(0x580 + self.node_id, sdo_client.on_response)
            with sdo_client.open(0x1021, 0, "rt") as eds_fp:
                while True:
                    line = eds_fp.read(448)
                    if not line:
                        break
                    result += line
        except Exception as e:
            self.fail(f"Reading EDS failed: {e}")
        self.assertTrue(result != "", "EDS file was not successfully downloaded")

    def test_0x1000_device_type(self):
        self._test_ro(0x1000, 0)

    def test_0x1001_error_register(self):
        self._test_ro(0x1001, 0)

    def test_0x1010_store(self):
        for i in range(1, 4):
            self._test_r(0x1010, i)

    def test_0x1011_restore(self):
        for i in range(1, 4):
            self._test_r(0x1011, i)

    def test_0x1018_identity(self):
        values = [None, 0x504d50, 0x9, None, None]
        for i in range(1, 4):
            self._test_r(0x1018, i, values[i])
            self._test_ro(0x1018, i)


if __name__ == '__main__':
    unittest.main()
