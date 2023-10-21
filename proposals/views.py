from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .models import Proposal,ProposalSection,saved_proposals,UserProfile
from .forms import ProposalForm,DeleteProposalForm,Createuser,ProposalSectionForm
from django.http import Http404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.



from django.template.loader import render_to_string
from django.http import FileResponse
from xhtml2pdf import pisa
from io import BytesIO


def generate_pdf(request, proposal_id):
    proposal = Proposal.objects.get(pk=proposal_id)

    # Convert the proposal details to HTML string
    sections = ProposalSection.objects.filter(proposal=proposal).order_by('position')
    html_content = render_to_string('view_proposal.html', {'proposal': proposal, 'sections': sections, 'pdf_version': True})

    # Convert the HTML to PDF
    result = BytesIO()
    pdf_gen_status = pisa.CreatePDF(html_content, dest=result)

    if not pdf_gen_status.err:
        # Create response with PDF data
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'filename="proposal_{proposal_id}.pdf"'
        return response

    return HttpResponse('Error Rendering PDF', status=400)



def registerUser(request):
    form = Createuser()
    if request.method == 'POST':
        obj = Createuser(request.POST)
        if obj.is_valid():
            obj.save()
            return redirect('loginPage')
        else:
            print(obj.errors)
        return HttpResponse('check credentials')
    return render(request,'registration/user_create.html',{'form':form})


def loginPage(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        valid_user = authenticate(request,username=uname,password=pwd)
        if valid_user != None:
            login(request,valid_user)
            
            if valid_user.is_superuser: 
                # Super user login
                # return redirect('list_proposals')
                return HttpResponse('under process')
                #return HttpResponse('under process')
            elif valid_user.is_staff:   
                # staff user login
                return redirect('under process')
            else:                       
                # Student login
                return redirect('list_proposals')
        else:                           
            # Invalid credentials shows error message
            #return render(request, 'home/login.html', {'error': 'Invalid username or password'})
            return HttpResponse('Your are not valid user')
        
    return render(request,'login.html')



def user_logout(request):
    logout(request)
    return redirect('home') 


def save_record(request,record_id):
    specific_rec = Proposal.objects.get(id=record_id)
    destination_rec = saved_proposals.objects.create(username=specific_rec.username,
        title=specific_rec.title,company_name=specific_rec.company_name,
        contact_name=specific_rec.contact_name,contact_email=specific_rec.contact_email,
        contact_phone=specific_rec.contact_phone,proposal_summary=specific_rec.proposal_summary,
        project_planning=specific_rec.project_planning,financing=specific_rec.financing
    )
    return redirect('saved_prop_display')


def saved_prop_display(request):
    user_profile = request.user.userprofile  # This fetches the UserProfile instance related to the user
    record = saved_proposals.objects.filter(username=user_profile)  # Filtering based on the user_profile
    return render(request, 'saved_prop.html', {'record': record, 'user_profile': user_profile})


from django.contrib.auth.decorators import login_required,user_passes_test


@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def ind_user(request):
    profile_page = request.user.UserProfile
    proposals = Proposal.objects.filter(profile_page=profile_page)
    saved_prop = saved_proposals.objects.filter(profile_page=profile_page)
    # prop_sec = ProposalSection.objects.filter(profile_page = profile_page)
    
    return render(request,'list_proposals.html',{'proposals':proposals,
                                                 'saved_prop':saved_prop})
    

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('list_proposals')  # Redirect to the create proposal page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def create_section_proposal(request):
    if request.method == 'POST':
        form = ProposalSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proposals:proposal_detail', proposal_id=form.cleaned_data['proposal'].id)
    else:
        form = ProposalSectionForm()
    
    return render(request, 'create_section_proposal.html', {'form': form})

@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def list_proposals(request):
    # proposals = Proposal.objects.all()
    proposals = Proposal.objects.all().order_by('order')
    return render(request, 'list_proposals.html', {'proposals': proposals})

@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def create_proposal(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            # Save the new proposal
            new_proposal = form.save(commit=False) 
            
            # Get or create the user profile for the logged-in user
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            new_proposal.username = user_profile  # Assign the UserProfile object to the proposal
            new_proposal.save()  # Now save the proposal

            return redirect('list_proposals')
    else:
        form = ProposalForm()

    return render(request, 'create_proposal.html', {'form': form})

@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def view_proposal(request, proposal_id):
    try:
        proposal = Proposal.objects.get(pk=proposal_id)
    except Proposal.DoesNotExist:
        proposal = None

    # Retrieve sections ordered by position
    sections = ProposalSection.objects.filter(proposal=proposal).order_by('position')

    return render(request, 'view_proposal.html', {'proposal': proposal, 'sections': sections})

@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def view_saved_proposal(request, proposal_id):
    try:
        proposal = saved_proposals.objects.get(pk=proposal_id)
    except saved_proposals.DoesNotExist:
        proposal = None
    return render(request, 'view_saved_prop.html', {'proposal': proposal})


@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def edit_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    if request.method == 'POST':
        form = ProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect('list_proposals')
    else:
        form = ProposalForm(instance=proposal)

    return render(request, 'proposals/edit_proposal.html', {'form': form, 'proposal': proposal})

@user_passes_test(lambda user:user.is_active,login_url='loginPage')
@login_required(login_url='loginPage')
def delete_proposal(request, proposal_id):
    try:
        proposal = Proposal.objects.get(pk=proposal_id)
    except Proposal.DoesNotExist:
        raise Http404("Proposal does not exist")

    if request.method == 'POST':
        form = DeleteProposalForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('confirm'):
            proposal.delete()
            return redirect('list_proposals')
    else:
        form = DeleteProposalForm()

    return render(request, 'proposals/delete_proposal.html', {'proposal': proposal, 'form': form})


 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json  # Import the json module at the top


@csrf_exempt
def reorder_proposals(request):
    if request.method == 'POST':
        proposal_order = json.loads(request.body).get('proposal_order')
        for index, proposal_id in enumerate(proposal_order):
            proposal = Proposal.objects.get(pk=int(proposal_id))
            proposal.order = index
            proposal.save()
        return JsonResponse({'message': 'Proposals reordered successfully'})
    return JsonResponse({'message': 'Invalid request method'}, status=400)


