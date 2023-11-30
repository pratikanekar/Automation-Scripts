import minimalmodbus
import itertools

def check_modbus_settings(baud_rate, parity, stop_bits, slave_id):
    try:
        port = '/dev/ttyUSB0'
        instrument = minimalmodbus.Instrument(port, slave_id)
        instrument.serial.baudrate = baud_rate
        instrument.serial.parity = parity
        instrument.serial.stopbits = stop_bits

        # Try reading from different types of registers
        register_types = ['coil', 'discrete_input', 'input', 'holding']
        for register_type in register_types:
            try:
                if register_type == 'coil':
                    response = instrument.read_bit(0, functioncode=1)
                elif register_type == 'discrete_input':
                    response = instrument.read_bit(0, functioncode=2)
                elif register_type == 'input':
                    response = instrument.read_register(0, functioncode=4)
                elif register_type == 'holding':
                    response = instrument.read_register(0, functioncode=3)
                else:
                    continue

                # If the response is received without errors, display the settings and register type
                print(f"Successful communication with settings: Baud Rate={baud_rate}, Parity={parity}, Stop Bits={stop_bits}, Slave ID={slave_id}, Register Type={register_type}")
                break  # Exit the loop if successful

            except minimalmodbus.ModbusException:
                pass

    except Exception as e:
        # Uncomment the next line if you want to see the exception details
        # print(f"Error for settings: Baud Rate={baud_rate}, Parity={parity}, Stop Bits={stop_bits}, Slave ID={slave_id}, Error: {e}")
        pass

def main():
    baud_rates = [9600, 19200, 38400, 57600, 115200]
    parity = ["None", "Even", "Odd"]
    stop_bits = [1, 2]
    slave_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Iterate through all combinations of settings
    for settings in itertools.product(baud_rates, parity, stop_bits, slave_ids):
        baud_rate, parity_setting, stop_bits_setting, slave_id = settings
        check_modbus_settings(baud_rate, parity_setting, stop_bits_setting, slave_id)

if __name__ == "__main__":
    main()
