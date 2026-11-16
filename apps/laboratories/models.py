from django.db import models

class Laboratory(models.Model):
    lab_id = models.AutoField(primary_key=True)
    lab_name = models.CharField(max_length=20)
    lab_block = models.CharField(max_length=1)
    lab_floor = models.SmallIntegerField()
    lab_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Laboratory #{self.lab_id}:{self.lab_name}"

    class Meta:
        db_table = "app_laboratory"