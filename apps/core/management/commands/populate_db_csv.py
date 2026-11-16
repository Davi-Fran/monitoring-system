import csv

from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.laboratories.models import Laboratory
from apps.devices.models import MicroControllerModel, MicroController
from apps.sensors.models import SensorModel, Sensor, SensorReading

class Command(BaseCommand):
    help = "Inserts data into the database from CSV files in the \"data\" folder"

    def _read_csv(self, file_name: str):
        with open(f"./data/{file_name}", encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            data = []
            
            for line in reader:
                data.append(line)
            
            return data

    def handle(self, *args, **options):
        users = self._read_csv("users.csv")
        labs = self._read_csv("laboratories.csv")
        mc_models = self._read_csv("micro_controller_models.csv")
        mcs = self._read_csv("micro_controllers.csv")
        sen_models = self._read_csv("sensor_models.csv")
        sens = self._read_csv("sensors.csv")
        sen_readings = self._read_csv("sensor_readings.csv")

        # Inserting users
        self.stdout.write(
            self.style.SUCCESS("INSERTING USERS")            
        )
        
        for user in users:
            if not User.objects.filter(email=user.get("email")).exists():
                new_user = User(
                    id=user.get("id"),
                    username=user.get("username"),
                    password=user.get("raw_password"),
                    first_name=user.get("first_name"),
                    last_name=user.get("last_name"),
                    email=user.get("email"),
                    is_superuser=user.get("is_superuser"),
                    is_staff=user.get("is_staff"),
                    is_active=user.get("is_active"),
                    date_joined=user.get("date_joined"),
                )

                new_user.set_password(user.get("raw_password"))
                new_user.full_clean()
                new_user.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Create user: {new_user.get_full_name()}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {user.get("first_name")} {user.get("last_name")}"
                    )
                )

        print()

        # Inserting laboratories
        self.stdout.write(
            self.style.SUCCESS("INSERTING LABORATORIES")            
        )

        for lab in labs:
            if not Laboratory.objects.filter(lab_name=lab.get("lab_name")).exists():
                new_lab = Laboratory(
                    lab_id=lab.get("lab_id"),
                    lab_name=lab.get("lab_name"),
                    lab_block=lab.get("lab_block"),
                    lab_floor=lab.get("lab_floor"),
                    lab_is_active=lab.get("lab_is_active"),
                )

                new_lab.full_clean()
                new_lab.save()
        
                self.stdout.write(
                    self.style.SUCCESS(f"Created laboratory: {lab.get("lab_name")}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Laboratory already exists: {lab.get("lab_name")}")
                )

        print()

        # Inserting Micro Controller Models
        self.stdout.write(
            self.style.SUCCESS("INSERTING MICRO CONTROLLER MODELS")            
        )
        
        for model in mc_models:
            if not MicroControllerModel.objects.filter(mcm_name=model.get("mcm_name")).exists():
                new_mc_model = MicroControllerModel(
                    mcm_id=model.get("mcm_id"),
                    mcm_name=model.get("mcm_name"),
                    mcm_is_active=model.get("mcm_is_active"),
                )

                new_mc_model.full_clean()
                new_mc_model.save()
        
                self.stdout.write(
                    self.style.SUCCESS(f"Created Micro Controller Model: {model.get("mcm_name")}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Micro Controller Model already exists: {model.get("mcm_name")}")
                )
        
        print()

        # Inserting Micro Controllers
        self.stdout.write(
            self.style.SUCCESS("INSERTING MICRO CONTROLLERS")            
        )
        
        for mc in mcs:
            if not MicroController.objects.filter(mc_mac_address=mc.get("mc_mac_address")).exists():
                new_mc = MicroController(
                    mc_id=mc.get("mc_id"),
                    mc_mac_address=mc.get("mc_mac_address"),
                    mc_latitude=mc.get("mc_latitude"),
                    mc_longitude=mc.get("mc_longitude"),
                    mc_registered_at=mc.get("mc_registered_at"),
                    mc_model_id=mc.get("mc_model_id"),
                    mc_laboratory_id=mc.get("mc_laboratory_id"),
                    mc_is_active=mc.get("mc_is_active"),
                )

                new_mc.full_clean()
                new_mc.save()
        
                self.stdout.write(
                    self.style.SUCCESS(f"Created Micro Controller: {mc.get("mc_mac_address")}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Micro Controller already exists: {mc.get("mc_mac_address")}")
                )

        print()

        # Inserting Sensor Models
        self.stdout.write(
            self.style.SUCCESS("INSERTING SENSOR MODELS")            
        )

        for sen_model in sen_models:
            if not SensorModel.objects.filter(sm_name=sen_model.get("sm_name")).exists():
                new_sen_model = SensorModel(
                    sm_id=sen_model.get("sm_id"),
                    sm_name=sen_model.get("sm_name"),
                    sm_function=sen_model.get("sm_function"),
                    sm_measurement_unit=sen_model.get("sm_measurement_unit"),
                    sm_is_active=sen_model.get("sm_is_active")
                )

                new_sen_model.full_clean()
                new_sen_model.save()
        
                self.stdout.write(
                    self.style.SUCCESS(f"Created Sensor Model: {sen_model.get("sm_name")}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Sensor Model already exists: {sen_model.get("sm_name")}")
                )

        print()

        # Inserting Sensor
        self.stdout.write(
            self.style.SUCCESS("INSERTING SENSORS")            
        )

        for sen in sens:
            if not Sensor.objects.filter(sen_id=sen.get("sen_id")).exists():
                new_sen = Sensor(
                    sen_id=sen.get("sen_id"),
                    sen_model_id=sen.get("sen_model_id"),
                    sen_connected_to_id=sen.get("sen_connected_to_id"),
                    sen_is_active=sen.get("sen_is_active"),
                )

                new_sen.full_clean()
                new_sen.save()
        
                self.stdout.write(
                    self.style.SUCCESS(f"Created Sensor: Id {sen.get("sen_id")}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Sensor already exists: Id {sen.get("sen_id")}")
                )

        print()

        # Inserting Sensor Readings
        self.stdout.write(
            self.style.SUCCESS("INSERTING SENSOR READINGS")            
        )

        for sen_reading in sen_readings:
            if not SensorReading.objects.filter(sr_id=sen_reading.get("sr_id")).exists():
                new_sen_reading = SensorReading(
                    sr_id=sen_reading.get("sr_id"),
                    sr_measured_value=sen_reading.get("sr_measured_value"),
                    sr_measured_at=sen_reading.get("sr_measured_at"),
                    sr_sen_id=sen_reading.get("sr_sen_id")
                )

                new_sen_reading.full_clean()
                new_sen_reading.save()
        
                self.stdout.write(
                    self.style.SUCCESS(f"Created Sensor Reading: Id {sen_reading.get("sr_id")}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Sensor Reading already exists: Id {sen_reading.get("sr_id")}")
                )