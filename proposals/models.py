from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Proposal(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    proposal_summary = models.TextField()
    project_planning = models.TextField()
    financing = models.TextField()


    def __str__(self):
        return self.title

class saved_proposals(models.Model):
    username = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    proposal_summary = models.TextField()
    project_planning = models.TextField()
    financing = models.TextField()
    
    def __str__(self):
        return self.title


class ProposalSection(models.Model):
    username = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    section_name = models.CharField(max_length=200)
    content = models.TextField()
    position = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.proposal.title} - {self.section_name}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()