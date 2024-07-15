import serial  #pyserial
import time

class SerialConnection:
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Opened serial port {self.port} with baudrate {self.baudrate}")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def close(self):
        if self.ser:
            self.ser.close()
            print("Serial port closed")
            self.ser = None

    def send_string(self, string_to_send):
        if not self.ser:
            print("Serial port not open")
            return

        try:
            self.ser.write(string_to_send.encode('utf-8'))
            print(f"Sent: {string_to_send}")
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")

    def read_string(self, read_timeout=5):
        if not self.ser:
            print("Serial port not open")
            return None

        try:
            end_time = time.time() + read_timeout
            received_data = ""
            
            while time.time() < end_time:
                if self.ser.in_waiting > 0:
                    received_data += self.ser.read(self.ser.in_waiting).decode('utf-8')
                time.sleep(0.1)  # Small delay to avoid busy-waiting

            if received_data:
                print(f"Received: {received_data}")
            else:
                print("No data received")

            return received_data
        except serial.SerialException as e:
            print(f"Error reading from serial port: {e}")
            return None
    
    def read_and_format(self, read_timeout=5):
        received_data = self.read_string(read_timeout)
        if received_data:
            formatted_data = received_data.split('\r\n')
            print(f"Formatted data: {formatted_data}")
            return formatted_data
        else:
            print("No data to format")
            return []
        
    def read_distance(self, read_timeout=5):
        formatted_data = self.read_and_format(read_timeout)
        for line in formatted_data:
            if line.startswith('d '):
                try:
                    distance = float(line.split(' ')[1])
                    print(f"Distance found: {distance}")
                    return distance
                except ValueError:
                    print(f"Error converting distance to float: {line}")
                    return None
        print("No distance string found")
        return None
    
    def read_state(self, read_timeout=5):
        formatted_data = self.read_and_format(read_timeout)
        for line in formatted_data:
            if line.startswith('s '):
                try:
                    distance = int(line.split(' ')[1])
                    print(f"State found: {distance}")
                    return distance
                except ValueError:
                    print(f"Error converting state to int: {line}")
                    return None
        print("No state string found")
        return None
    
    def contains_string(self, string_to_find, read_timeout=5):
        formatted_data = self.read_and_format(read_timeout)
        for line in formatted_data:
            if string_to_find in line:
                print(f"String '{string_to_find}' found in: {line}")
                return True
        print(f"String '{string_to_find}' not found in received data")
        return False


if __name__ == "__main__":
    # Replace 'COM3' with your serial port, e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows
    port = 'COM9'
    baudrate = 9600
    string_to_send = "Hello, Serial Port!"

    connection = SerialConnection(port, baudrate)
    connection.open()
    
    connection.send_string(string_to_send)
    
    # Optionally, read and find distance data from serial port
    read_timeout = 5  # seconds
    distance_data = connection.read_distance(read_timeout)
    if distance_data is not None:
        print(f"Final distance data: {distance_data}")

    # Check if a specific string is in the received data
    string_to_find = "Hello"
    string_found = connection.contains_string(string_to_find, read_timeout)
    print(f"String '{string_to_find}' found: {string_found}")

    connection.close()
