from django.db import models

class ApartmentBuilding(models.Model):
    company_name = models.CharField(max_length=20)
    building_name = models.CharField(max_length=20)
    address_number = models.IntegerField()
    address_street = models.CharField(max_length=20)
    address_city = models.CharField(max_length=20)
    address_state = models.CharField(max_length=5)
    address_zip_code = models.CharField(max_length=5)
    year_built = models.IntegerField()

    class Meta:
        unique_together = ('company_name', 'building_name')

class ApartmentUnit(models.Model):
    unit_number = models.CharField(max_length=10)
    monthly_rent = models.IntegerField()
    square_footage = models.IntegerField()
    available_date_for_move_in = models.DateField()
    building = models.ForeignKey(ApartmentBuilding, on_delete=models.CASCADE)

class Room(models.Model):
    name = models.CharField(max_length=20)
    square_footage = models.IntegerField()
    description = models.CharField(max_length=50)
    unit = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'unit')

class Amenities(models.Model):
    type = models.CharField(max_length=20, unique=True)
    description = models.TextField()

class ApartmentAmenities(models.Model):
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    unit = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE)


class PetPolicy(models.Model):
    apartment_building = models.ForeignKey(ApartmentBuilding, on_delete=models.CASCADE)
    pet_type = models.CharField(max_length=50)
    pet_size = models.CharField(max_length=20)
    is_allowed = models.BooleanField()
    registration_fee = models.IntegerField(null=True, blank=True)
    monthly_fee = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('apartment_building', 'pet_type', 'pet_size')
