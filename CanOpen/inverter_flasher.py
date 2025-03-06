import argparse
import serial
import time
import sys
import serial.tools.list_ports
import os

# Messages
silent_message = bytearray([0x90, 0x01, 0x00, 0x91, 0x01])
master_message = bytearray([0x90, 0x01, 0x01, 0x91, 0x02])
slave_message = bytearray([0x90, 0x01, 0x02, 0x91, 0x03])
power_off_message = bytearray([0x90, 0x02, 0x00, 0x91, 0x02])
power_on_message = bytearray([0x90, 0x02, 0x01, 0x91, 0x03])
operation_succeed = bytearray([0x90, 0x03, 0x01, 0x91, 0x04])
operation_failed = bytearray([0x90, 0x03, 0xFF, 0x91, 0x02])

# Send commands to board and receive response
def send_command_and_receive_result(command, serial_port):
    try:
        with serial.Serial(serial_port, 115200, timeout=2) as ser:
            ser.write(command)
            ser.flush()
            time.sleep(0.1)  # Time to guarantee the sending of the message
            response = ser.read(ser.in_waiting or 1)  # Reading the response

            # Response check
            if response == operation_succeed:
                return True
            elif response == operation_failed:
                return False
            else:
                return False
    except Exception as e:
        return False  # Errore

# Flash firmware on master
def flash_master(firmware_master, serial_port):
    command = master_message
    result = send_command_and_receive_result(command, serial_port)  # Select master
    if not result:
        return False
    time.sleep(1)  # Wait for the end of selection
    try:
        os.system(f' "cd C:\\Program Files\\STMicroelectronics\\STM32Cube\\STM32CubeProgrammer\\bin & .\\STM32_Programmer_CLI.exe -c port=SWD -w {firmware_master} 0x08000000"')  #Flashing
        reboot_micros(serial_port)  # Restart after the flashing
        return True
    except Exception as e:
        print(f"Error during flashing on master: {e}.")
        return False
    
# Flash firmware on slave
def flash_slave(firmware_slave, serial_port):
    command = slave_message
    result = send_command_and_receive_result(command, serial_port)  # Select master
    if not result:
        return False
    time.sleep(1)  # Wait for the end of selection
    try:
        os.system(f' "cd C:\\Program Files\\STMicroelectronics\\STM32Cube\\STM32CubeProgrammer\\bin & .\\STM32_Programmer_CLI.exe -c port=SWD -w {firmware_slave} 0x08000000"')  #Flashing
        reboot_micros(serial_port)  # Restart after the flashing
        return True
    except Exception as e:
        print(f"Error during flashing on master: {e}.")
        return False

# Flash firmware on both master and slave
def flash_master_and_slave(firmware_master, firmware_slave, serial_port):

    # Flash firmware on master
    result_master = flash_master(firmware_master, serial_port)
    if not result_master:
        return False

    # Flash firmware on slave
    result_slave = flash_slave(firmware_slave, serial_port)
    if not result_slave:
        return False

    return True

# Set inhibit
def inhibit(serial_port):
    command = silent_message
    result = send_command_and_receive_result(command, serial_port)
    if not result:
        print("Error during inhibition.")
        return False
    time.sleep(1)
    return True

# Turn off inverter
def turn_off(serial_port):
    power_off_command = power_off_message
    power_off = send_command_and_receive_result(power_off_command, serial_port)

    if power_off:
        print("Inverter successfully turned off.")
        return True
    else:
        print("Failed to turn off.")
        return False

# Turn on inverter
def turn_on(serial_port):
    power_on_command = power_on_message
    power_on = send_command_and_receive_result(power_on_command, serial_port)

    if power_on:
        print("Inverter successfully turned on.")
        return True
    else:
        print("Failed to turn on.")
        return False

# Reboot inverter
def reboot_micros(serial_port):
    if not turn_off(serial_port):
        return False

    time.sleep(3)

    if turn_on(serial_port):
        return True
    else:
        return False

# Find STLink port automatically
def find_stlink_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "STMicroelectronics STLink Virtual COM Port" in port.description:
            return port.device
    return None

# Parser of args
def main():
    parser = argparse.ArgumentParser(description="Script to manage the flashing and reboot of the inverter.")
    parser.add_argument("-m", "--master", help="Flash firmware on master.", action="store_true")
    parser.add_argument("-s", "--slave", help="Flash firmware on slave.", action="store_true")
    parser.add_argument("-b", "--both", help="Flash firmware both on master and slave.", action="store_true")
    parser.add_argument("-i", "--inhibit", help="Set inhibition.", action="store_true")
    parser.add_argument("-o", "--turnoff", help="Turn off inverter.", action="store_true")
    parser.add_argument("-n", "--turnon", help="Turn on inverter.", action="store_true")
    parser.add_argument("-r", "--reboot", help="Reboot inverter.", action="store_true")
    parser.add_argument("-fm", "--firmware_master", help="Path of master firmware.", type=str)
    parser.add_argument("-fs", "--firmware_slave", help="Path of slave firmware.", type=str)
    parser.add_argument("-p", "--port", help="Serial port (e.g. COM5 or /dev/ttyUSB0). If not specified the port will be found automatically.", type=str)

    args = parser.parse_args()

    # Check if at least one operation is executed
    if not (args.master or args.slave or args.both or args.inhibit or args.turnoff or args.turnon or args.reboot):
        print("Errore: nessuna azione selezionata.")
        return False

    # Check if firmware path is specified when trying to flash on master
    if args.master and not args.firmware_master:
        print("Error: master's firmware path must be specified in the option -fm.")
        return False

    # Check if firmware path is specified when trying to flash on master
    if args.slave and not args.firmware_slave:
        print("Error: slave's firmware path must be specified in the option -fs.")
        return False

    # If port is not specified, it will be found automatically
    if not args.port:
        args.port = find_stlink_port()
        if not args.port:
            print("Error: serial port not found.")
            return False  # Errore

    # Check if flashing on master is requested
    if args.master:
        result = flash_master(args.firmware_master, args.port)
        if not result:
            return False

    # Check if flashing on slave is requested
    if args.slave:
        result = flash_slave(args.firmware_slave, args.port)
        if not result:
            return False
        
    # Check if both slave and master flashings are requested
    if args.both:
        if not args.firmware_master or not args.firmware_slave:
            print("Error: you must specify both master's and slave's firmware paths with --firmware_master e --firmware_slave.")
            return False

        result = flash_master_and_slave(args.firmware_master, args.firmware_slave, args.port)
        if not result:
            return False

    # Check if inhibition is requested
    if args.inhibit:
        result = inhibit(args.port)
        if not result:
            return False  #Errore

    # Spegnimento
    if args.turnoff:
        result = turn_off(args.port)
        if not result:
            return False

    #Accensione
    if args.turnon:
        result = turn_on(args.port)
        if not result:
            return False

    # Esegue il riavvio
    if args.reboot:
        result = reboot_micros(args.port)
        if not result:
            print("Error during reboot.")
            return False  # Errore

    print("Successful operation.")
    return True  # Successo

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)  # Exit con codice di errore
    sys.exit(0)  # Exit con successo
