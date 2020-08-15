from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from members.models import account_activation_token
from members.models import Member
from django.views.generic import View
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .forms import EditMemberForm, ProfileForm

class LoginView(View):
    def get(self, request):
        context = {
            'title': 'GammaTrades Login'
        }
        return render(request, 'hbi-homepage/login.html', context)

    def post(self, request):
        context = {
            'title': 'GammaTrades Login',
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR, 'username are required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error'] = True
        checkmember0 = Member.objects.filter(username=username).count()
        #print("username=", username)
        #print("count checkmember0=",checkmember0)
        if checkmember0 != 0:
            #print ("Member EXIST!")
            checkmember = Member.objects.get(username=username)
            #print('checkmember = ', checkmember)
            #print('checkmember is_activated = ', checkmember.is_activated)
            # user = authenticate(request, username=username, password=password)

            if checkmember is not None and checkmember.is_activated == True:  # member exist and is_activated
                if checkmember.is_approved == True:                           # member is approved by admininstrator
                        #print("Member exist, is_activated")
                        user = authenticate(request, username=username, password=password)
                        if not context['has_error'] and not user:
                            messages.add_message(request, messages.ERROR, 'Incorrect Password, Please Re-try')
                            context = {
                                'title': 'GammaTrades Login',
                                'has_error' : True
                            }
                            return render(request, 'hbi-homepage/login.html', context)
                        else:
                            login(request, user)
                            return redirect('home')
                else:                                                            # member is approved by admininstrator
                    messages.add_message(request, messages.ERROR, 'Your membership is pending approval from Administrator, please try again later')
                    context = {
                        'title': 'GammaTrades Login',
                        'has_error': True
                    }
                    return render(request, 'hbi-homepage/login.html', context)

            elif checkmember is not None and checkmember.is_activated == False:
                #print("Member exist but the account not active!")
                messages.info(request, mark_safe('Please check Email to activate your account.. <br> To re-send activation code, click <a href="http://127.0.0.1:8000/requestactivatecode/">HERE</a>'))

                #messages.add_message(request, messages.ERROR,'Your account is not yet activated.. Please check your Email to activate <a href="http://127.0.0.1:8000/members/password_change">Change Password  </a>')
                context = {
                    'title': 'GammaTrades Login',
                    'has_error': True
                }
                return render(request, 'hbi-homepage/login.html', context)
            else:
                # the authentication system was unable to verify the username and password
                #print("Password is incorrect.")
                messages.add_message(request, messages.ERROR, 'Wrong Password, Please re-try')
                context = {
                    'title': 'GammaTrades Login',
                    'has_error': True
                }
                return render(request, 'hbi-homepage/login.html', context)
        else:
            #print("Member DOES NOT EXIST!")
            messages.add_message(request, messages.ERROR, 'No Such Accounts, Please Re-Try')
            context = {
                'title': 'GammaTrades Login',
                'has_error': True
            }
            return render(request, 'hbi-homepage/login.html', context)


class RegistrationView(View):
    def get(self, request):
        return render(request, 'hbi-homepage/signup.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if first_name == '':
            messages.add_message(request, messages.ERROR, 'please provide your first name')
            context['has_error'] = True
        if last_name == '':
            messages.add_message(request, messages.ERROR, 'please provide your last name')
            context['has_error'] = True
        #if email == '' or not validate_email(email):
        if email == '':
            messages.add_message(request, messages.ERROR, 'please provide a valid email')
            context['has_error'] = True
        if password == '' or password2 == '':
            messages.add_message(request, messages.ERROR, 'Passwords are required')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            context['has_error'] = True
        if Member.objects.filter(username=email).exists():
            messages.add_message(request, messages.ERROR, 'email is taken, use another one')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'hbi-homepage/signup.html', context, status=400)

        new_user = Member.objects.create_user(username=email, first_name=first_name, last_name=last_name, password=password2)
        #new_user.set_password(password)
        new_user.is_activated = False
        new_user.save()

        current_site = get_current_site(request)
        print('1. current_site=',current_site)
        print('2. current_site.domain=', current_site.domain)
        mail_subject = 'GammaTrades: Activate Your Account'
        message = render_to_string('hbi-homepage/acc_active_email.html', {
            'user': new_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token123': account_activation_token.make_token(new_user),
        })
        send_mail(mail_subject, message, 'admin@gammatrades.net', [email])

        print("3. mail_subject=", mail_subject)
        print("4. message=", message)
        print("5 . email=", [email])

        messages.add_message(request, messages.SUCCESS,'Please check your Email to activate your Account')
        return redirect('login')


class RequestResetLinkView(View):
    def get(self, request):
        return render(request, 'hbi-homepage/request-reset-password.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        email = request.POST.get('email')
        #print('1. email = ', email)
        if email == '':
        #if not validate_email(email=email):
            messages.add_message(request, messages.ERROR, 'please provide an email')
            return render(request, 'hbi-homepage/request-reset-password.html', context, status=400)
        current_site = get_current_site(request)
        #print('3. current_site=', current_site)
        #print('4. current_site.domain=', current_site.domain)
        user = Member.objects.filter(username=email).first()
        #print('2. user = ', user)
        if not user:
            messages.add_message(request, messages.ERROR, 'This email is not in our records, please re-try')
            return render(request, 'hbi-homepage/request-reset-password.html', context, status=404)

        mail_subject = 'GammaTrades: Reset Your Password'
        message = render_to_string('hbi-homepage/acc_finish-reset.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token123': account_activation_token.make_token(user),
        })

        # to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, 'admin@gammatrades.net', [email])

        #print("1. mail_subject=", mail_subject)
        #print("2. message=", message)
        #print("3. email=", [email])

        messages.add_message(request, messages.INFO, 'We have sent you an email with a link to reset your password')
        return render(request, 'hbi-homepage/login.html', context)


class CompletePasswordChangeView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Member.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
            user = None
        if user is None or not account_activation_token.check_token(user, token):
            messages.add_message(request, messages.WARNING, 'Link is no longer valid,please request a new one')
            return render(request, 'hbi-homepage/reset-password.html', status=401)
        return render(request, 'hbi-homepage/change-password.html', context={'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        context = {'uidb64': uidb64, 'token': token}
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Member.objects.get(pk=uid)
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if len(password) < 6:
                messages.add_message(request, messages.ERROR, 'Password should be at least 6 characters long')
                return render(request, 'hbi-homepage/change-password.html', context, status=400)
            if password != password2:
                messages.add_message(request, messages.ERROR, 'Passwords must match')
                return render(request, 'hbi-homepage/change-password.html', context, status=400)
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.INFO, 'Password changed successfully,login with your new password')
            return redirect('login')
        except DjangoUnicodeDecodeError:
            messages.add_message(request, messages.ERROR, 'Something went wrong,you could not update your password')
            return render(request, 'hbi-homepage/change-password.html', context, status=401)

class RequestActivationCode(View):
    def get(self, request):
        return render(request, "hbi-homepage/request_activation_code.html")

    def post(self, request):
        username = request.POST.get('username')
        checkmember0 = Member.objects.filter(username=username).count()
        #print('At requestActivationCode')
        #print('1. username=', username)
        #print("2. count checkmember0=", checkmember0)
        if checkmember0 != 0:
            #print ('3. User EXIST!!')
            checkmember = Member.objects.get(username=username)
            mail_subject = 'GammaTrades: Activate Your Account (Immediate Action Needed)'
            current_site = get_current_site(request)
            print('5. current_site=', current_site)
            print('6. current_site.domain=', current_site.domain)
            message = render_to_string('hbi-homepage/acc_active_email.html', {
                'user': checkmember,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(checkmember.pk)),
                'token123': account_activation_token.make_token(checkmember),
                })

            # to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'admin@gammatrades.net', [username])

            #print("1. mail_subject=", mail_subject)
            #print("2. message=", message)
            #print("3. username=", [username])
            messages.add_message(request, messages.SUCCESS, 'Please check your Email and activate your Account')
            return redirect('login')
        else:
            #print('3. User DOES NOT EXIST!!')
            messages.add_message(request, messages.SUCCESS, 'There is no such User registered in our System, please sign-up')
            return redirect('signup')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_activated = True


        # send message to IT Administrator to inform new member activation require approval (set is_approved = True)
        mail_subject = 'GammaTrades: New Member Requiring Approval From IT Admin'
        message = render_to_string('hbi-homepage/acc_activated_notice_email.html', {
            'user': user,
        })

        send_mail(mail_subject, message, 'admin@gammatrades.net', ['admin@gammatrades.net'])

        user.save()
        messages.add_message(request, messages.SUCCESS, 'Thank you for your Email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

class MySettingsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            #print("At GET: MySettingsView")
            my_qs = Member.objects.filter(username=request.user)
            #print('1. first_name=', my_qs[0].first_name)
            #print('2. items_per_page=', my_qs[0].items_per_page)
            #print('3. brochure_country=', my_qs[0].brochure_country)
            context = {"title": "mysettings.html", 'blog_list': my_qs}
            return render(request, 'hbi-dashboard/mysettings.html', context)
        else:
            return render(request, 'hbi-homepage/index.html')

    def post(self, request):
        if request.user.is_authenticated:
            #print("At POST: MySettingsView")
            my_qs = Member.objects.filter(username=request.user).get()
            #print('4. last_name=', my_qs.last_name)
            #print('5. items_per_page=', my_qs.items_per_page)
            radioinline = request.POST.get('radio-inline')
            #print('6. radioinline=', radioinline)
            my_qs.items_per_page = radioinline

            my_qs.brochure_country = request.POST.get('brochure_country')
            my_qs.certificate_country = request.POST.get('certificate_country')
            my_qs.eproof_country = request.POST.get('eproof_country')
            my_qs.manual_country = request.POST.get('manual_country')
            my_qs.proposal_country = request.POST.get('proposal_country')
            my_qs.powerpoint_country = request.POST.get('powerpoint_country')
            my_qs.quotation_country = request.POST.get('quotation_country')

            my_qs.save()
            return redirect('home')
        else:
            return render(request, 'hbi-homepage/index.html')

def edit_myprofile(request):
    selected_document = get_object_or_404(Member, username=request.user)
    form = EditMemberForm(instance=selected_document)

    if request.method == 'POST':
        form = EditMemberForm(request.POST, request.FILES, instance=selected_document)
        if form.is_valid():
            #print('1. form position=', form.cleaned_data['position'])
            #print('2. form department=', form.cleaned_data['department'])
            #print('3. form photo=', form.cleaned_data['photo'])
            form.save()
            return redirect('home')
        else:
            return render(request, "hbi-dashboard/myprofile.html")

    context = {'form':form,
               'title': 'My Profile',
              }
    return render(request, 'hbi-dashboard/myprofile.html', context)