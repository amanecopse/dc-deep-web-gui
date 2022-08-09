from django.db import models

# message type values: Temperature Humidity Co2 Light Camera Motor
# keys: type celsius rh ppm lux index status


class Temperature(models.Model):

    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    celsius = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'mac: {self.mac}, date:{self.dateTime}, celsius: {self.celsius}'


class Humidity(models.Model):

    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    rh = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'mac: {self.mac}, date:{self.dateTime}, rh: {self.rh}'


class Co2(models.Model):

    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    ppm = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'mac: {self.mac}, date:{self.dateTime}, ppm: {self.ppm}'


class Light(models.Model):

    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    lux = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'mac: {self.mac}, date:{self.dateTime}, lux: {self.lux}'


class Camera(models.Model):

    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    index = models.CharField(max_length=20)
    status = models.IntegerField()

    def __str__(self):
        return f'mac: {self.mac}, date:{self.dateTime}, index: {self.index}, status: {self.status}'


class Motor(models.Model):

    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()

    def __str__(self):
        return f'mac: {self.mac}, date:{self.dateTime}, status: {self.status}'
