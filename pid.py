from pyb import millis

class Pid:
    def __init__(self, p=0, i=0, d=0, imax=100):
        if not all(isinstance(param, (int, float)) for param in [p, i, d, imax]):
            raise ValueError("All parameters (p, i, d, imax) must be numeric.")

        self.kp = float(p)
        self.ki = float(i)
        self.kd = float(d)
        self.imax = abs(imax)
        self.integrator = 0
        self.last_error = 0
        self.last_t = 0

    def get_pid(self, error):
        tnow = millis()
        dt = tnow - self.last_t
        output = 0

        if (self.last_t == 0 or dt > 1000):
            dt = 0
            self.integrator = 0

        self.last_t = tnow
        delta_time = float(dt) / float(1000)
        output += error * self.kp

        if (abs(self.kd) > 0 and dt > 0):
            derivative = (error - self.last_error) / delta_time
            self.last_error = error
            output += derivative * self.kd

        if (abs(self.ki) > 0 and dt > 0):
            self.integrator += (error * self.ki) * delta_time
            self.integrator = max(min(self.integrator, self.imax), -self.imax)
            output += self.integrator

        return output
