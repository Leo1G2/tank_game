import serial

class JoystickReader:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.state = {"X": 2048, "Y": 2048, "SW": 1}

    def read(self):
        try:
            line = self.ser.readline().decode(errors="ignore").strip()
            if line.startswith("X="):
                parts = line.split()
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=")
                        self.state[k] = int(v)
        except:
            pass

    def get_direction(self, threshold=400):
        self.read()
        dx = self.state["X"] - 2048
        dy = self.state["Y"] - 2048
        sw = self.state["SW"]

        return {
            "forward": dy < -threshold,
            "left": dx < -threshold,
            "right": dx > threshold,
            "shoot": sw == 0
        }
