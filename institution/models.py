from django.db import models

class Faculty(models.Model):
    acronym = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=62)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.acronym

class Career(models.Model):
    name = models.CharField(max_length=38, primary_key=True)
    id_faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Organization(models.Model):
    abbreviation = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    mission = models.CharField(max_length=500, default='')
    vision = models.CharField(max_length=500, default='')
    banner = models.JSONField(default=dict)
    gallery = models.JSONField(default=dict)
    id_tutor = models.OneToOneField('user.Professor', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class SubOrganization(models.Model):
    sub_org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    id_organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    id_member_in_charge = models.ForeignKey('user.Member', on_delete=models.CASCADE, blank=True, null=True)
    gallery = models.JSONField(default=dict)
    members = models.ManyToManyField('user.Member', related_name="list_of_branch_members")

    def __str__(self):
        return f"{self.id_organization.abbreviation} {self.name}"
