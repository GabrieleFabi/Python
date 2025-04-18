import argparse
import serial
import time
import sys
import serial.tools.list_ports
import os
import warnings
import platform
import shutil

# Determine the OS and set the paths dynamically
if platform.system() == "Windows":
    stm32_programmer_dir = os.environ.get("PROGRAMFILES", "C:\\Program Files") + "\\STMicroelectronics\\STM32Cube\\STM32CubeProgrammer\\bin"
    cmd_program = ".\\STM32_Programmer_CLI.exe -c port=SWD -w"
elif platform.system() == "Linux":
    stm32_programmer_dir = "/usr/local/STMicroelectronics/STM32CubeProgrammer/bin"
    cmd_program = "./STM32_Programmer_CLI -c port=SWD -w"
else:
    raise OSError("Unsupported operating system")

# Verify the STM32CubeProgrammer path exists
if not os.path.exists(stm32_programmer_dir):
    raise FileNotFoundError(f"STM32CubeProgrammer not found in {stm32_programmer_dir}")

cmd_path = f'cd {stm32_programmer_dir}'

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
def flash_master(firmware_master_path, serial_port):
    command = master_message
    result = send_command_and_receive_result(command, serial_port)  # Select master
    if not result:
        return False
    time.sleep(1)  # Wait for the end of selection
    try:
        if platform.system() == "Windows":
            os.system(f'"{cmd_path} & {cmd_program} {firmware_master_path} 0x08000000"')  # Windows
        else:
            os.system(f'cd {stm32_programmer_dir} && {cmd_program} "{firmware_master_path}" 0x08000000')  # Linux
        reboot_micros(serial_port)  # Restart after the flashing
        return True
    except Exception as e:
        print(f"Error during flashing on master: {e}.")
        return False
    
# Flash firmware on slave
def flash_slave(firmware_slave_path, serial_port):
    command = slave_message
    result = send_command_and_receive_result(command, serial_port)  # Select master
    if not result:
        return False
    time.sleep(1)  # Wait for the end of selection
    try:
        if platform.system() == "Windows":
            os.system(f'"{cmd_path} & {cmd_program} {firmware_slave_path} 0x08000000"')  # Windows
        else:
            os.system(f'cd {stm32_programmer_dir} && {cmd_program} "{firmware_slave_path}" 0x08000000')  # Linux
        reboot_micros(serial_port)  # Restart after the flashing
        return True
    except Exception as e:
        print(f"Error during flashing on master: {e}.")
        return False

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
        if "stlink" in port.description.lower():
            return port.device
    return None

# Parser of args
def main():
    parser = argparse.ArgumentParser(description="Script to manage the flashing and reboot of the inverter.")
    parser.add_argument("-i", "--inhibit", help="Set inhibition.", action="store_true")
    parser.add_argument("-o", "--turnoff", help="Turn off inverter.", action="store_true")
    parser.add_argument("-n", "--turnon", help="Turn on inverter.", action="store_true")
    parser.add_argument("-r", "--reboot", help="Reboot inverter.", action="store_true")
    parser.add_argument("-m", "--master", help="Path of master firmware.", type=str)
    parser.add_argument("-s", "--slave", help="Path of slave firmware.", type=str)
    parser.add_argument("-p", "--port", help="Serial port (e.g. COM5 or /dev/ttyUSB0). If not specified the port will be found automatically.", type=str)

    args = parser.parse_args()

    # Check if at least one operation is executed
    if not (args.master or args.slave or args.inhibit or args.turnoff or args.turnon or args.reboot):
        print("Errore: nessuna azione selezionata.")
        return False

    # If port is not specified, it will be found automatically
    if not args.port:
        args.port = find_stlink_port()
        if not args.port:
            print("Error: serial port not found.")
            return False  # Errore

    # Check if flashing on master is requested
    if args.master:
        firmware_master_path = os.path.abspath(args.master)
        if not os.path.exists(firmware_master_path):
            warnings.warn("path del master non trovato")
            return False
        result = flash_master(firmware_master_path, args.port)
        if not result:
            return False

    # Check if flashing on slave is requested
    if args.slave:
        firmware_slave_path = os.path.abspath(args.slave)
        if not os.path.exists(firmware_slave_path):
            warnings.warn("path del master non trovato")
            return False
        result = flash_slave(firmware_slave_path, args.port)
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
