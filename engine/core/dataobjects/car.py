class Car:
    # __ private member
    fuel = 10
    brand = ''

    def __init__(self, brand='Ford'):
        self.brand = brand

    def run(self):
        self.fuel -= 1

    def add(self):
        self.fuel += 1

    def debug(self):
        Car.__private_function()
        print(self.brand, self.fuel)

    def get_fuel(self):
        return self.fuel

    def __private_function():
        print('Where public cannot see')

    def __str__(self):
        return 'Hello'
        # '"%s is a %d" % (self.brand, self.fuel)




