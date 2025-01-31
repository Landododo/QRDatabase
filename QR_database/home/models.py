from django.db import models

# Create your models here.
class gds_files(models.Model):
    # all values in um if not noted
    file_name = models.CharField(max_length=50)
    num_qrs = models.IntegerField()
    qr_size = models.FloatField()
    qrs_per_row = models.IntegerField()
    qrs_per_col = models.IntegerField()
    spacing = models.FloatField()
    padding = models.FloatField()
    time_uploaded = models.CharField(max_length=50)
    last_updated = models.CharField(max_length=50)

    def __str__(self):
        return(self.file_name + " for a "+\
               self.qrs_per_row + "x" + self.qrs_per_col+" grid")
    
class sample_images(models.Model):
    gds_file_id = models.IntegerField()
    file_name = models.CharField(max_length = 50)
    width = models.IntegerField()
    height = models.IntegerField()
    row = models.IntegerField()
    col = models.IntegerField()
    abs_x = models.FloatField()
    abs_y = models.FloatField()
    num_codes = models.IntegerField()
    img_id = models.IntegerField()