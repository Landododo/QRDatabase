from django.db import models

# Create your models here.
class gds_files(models.Model):
    file_name = models.CharField(max_length=50)
    num_qrs = models.IntegerField()
    qr_size = models.FloatField()
    qrs_per_row = models.IntegerField()
    qrs_per_col = models.IntegerField()
    time_uploaded = models.CharField(max_length=50)
    last_updated = models.CharField(max_length=50)

    def __str__(self):
        return(self.file_name + " for a "+\
               self.qrs_per_row + "x" + self.qrs_per_col+" grid")