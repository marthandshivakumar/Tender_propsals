from django.contrib import admin
from .models import Proposal,ProposalSection,saved_proposals,UserProfile
# Register your models here.


admin.site.register(Proposal)
admin.site.register(ProposalSection)
admin.site.register(saved_proposals)
admin.site.register(UserProfile)