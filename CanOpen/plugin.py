def pytest_addoption(parser):
    parser.addoption(
        "--interface",
        action="store",
        type=str,
        default="kvaser",
        help="insert the interface, default is setted to kvaser"
    )
    parser.addoption(
        "--channel",
        action="store",
        type=int,
        default=0,
        help="insert the channel, default is setted to 0"
    )
    parser.addoption(
        "--bitrate",
        action="store",
        type=int,
        default=500_000,
        help="insert the bitrate, default is setted to 500000"
    )
    parser.addoption(
        "--start-index",
        action="store",
        type=lambda x: int(x, 0),
        default=0x2000,
        help="index of the first message to be sent, default is 0x2000, this value is included"
    )

    parser.addoption(
        "--node-id",
        action="store",
        type=int,
        default=113,
        help="id of the node to add to the network, default is setted to 113"
    )

    parser.addoption(
        "--flash",
        action="store_true",
        help="flash the master and the slave"
    )

    parser.addoption(
        "--fm",
        action="store",
        type=str,
        default="",
        help="insert the interface, default is setted to empty"
    )

    parser.addoption(
        "--fs",
        action="store",
        type=str,
        default="",
        help="insert the interface, default is setted to kvaser"
    )

    parser.addoption(
        "--reboot",
        action="store_true",
        help="reboot the inverter"
    )
    