import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from NewDjangoProj.settings import BASE_DIR
from test_django.forms import CarForm, ClientForm, MessageForm, MechanicForm
from test_django.models import Client, Car, Mechanic, Message


def show_info(request):
    user = request.user
    sex_list = ['women', 'men']
    sex = random.choice(sex_list)
    num = random.randint(1, 80)
    if user.is_authenticated:
        if user.groups.filter(name="Mechanics").exists():
            mechanic = Mechanic.objects.get(id_user_id=user.id)
            cars = Car.objects.filter(mechanics=mechanic.id)
            cars = list(cars)
            return render(request, 'mechanicInfo.html',
                          {"mechanic": mechanic, "cars": cars,
                           "sex": sex, "number": num})
        client = Client.objects.get(id_user_id=user.id)
        cars = Car.objects.filter(client=client.id)
        cars = list(cars)
        return render(request, 'clientInfo.html',
                      {"client": client, "cars": cars,
                       "sex": sex, "number": num})
    else:
        return render(request, 'noAccess.html')

#test1_user
#daslFiwfn24
#test1user@bk.ru


def show_messages(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Mechanics").exists():
            mechanic = Mechanic.objects.get(id_user_id=user.id)

            cars = Car.objects.filter(mechanics=mechanic.id)

            return render(request, 'messagesInfo.html',
                          {"cars": cars, "mech": mechanic})
        else:
            return render(request, 'noAccess.html')
    else:
        return render(request, 'noAccess.html')


def show_client(request, id_user):
    user = request.user
    if user.is_authenticated:
        client = Client.objects.get(id_user_id=id_user)
        cars = Car.objects.filter(client=client.id)
        cars = list(cars)
        sex_list = ['women', 'men']
        sex = random.choice(sex_list)
        num = random.randint(1, 80)
        return render(request, 'clientInfo.html',
                      {"client": client, "cars": cars,
                       "number": num, "sex": sex})
    else:
        return render(request, 'noAccess.html')


def car_info(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'carInfo.html', {'car': car})


def accept_car(request, message_id):
    current_user = request.user
    if current_user.groups.filter(name="Mechanics").exists():
        mechanic = Mechanic.objects.get(id_user_id=current_user.id)
        cars = Car.objects.filter(mechanics=mechanic.id)
        message = Message.objects.get(id=message_id)
        message.isAccepted = True
        message.main_mech = mechanic
        message.save()
        return render(request, 'messagesInfo.html',
                      {"cars": cars})
    else:
        return render(request, 'noAccess.html')


def delete_car(request, car_id):
    current_user = request.user
    if current_user.groups.filter(name="Mechanics").exists():
        car = Car.objects.get(id=car_id)
        car.delete()
        mechanic = Mechanic.objects.get(id_user_id=current_user.id)
        cars = Car.objects.filter(mechanics=mechanic.id)
        cars = list(cars)
        sex_list = ['women', 'men']
        sex = random.choice(sex_list)
        num = random.randint(1, 80)
        return redirect('/')
    else:
        return render(request, 'noAccess.html')


def change_car_status(request, car_id):
    current_user = request.user
    if current_user.groups.filter(name="Mechanics").exists():
        car = Car.objects.get(id=car_id)
        car.repairIsDone = not car.repairIsDone
        car.save()
        return render(request, 'carInfo.html', {'car': car})
    else:
        return render(request, 'noAccess.html')


def create_car(request, id_user):
    if request.method == "GET":
        car_form = CarForm()
        message_form = MessageForm()
        return render(request, 'createCarForm.html', {'form': car_form, 'message_form': message_form})
    else:
        car_form = CarForm(request.POST)
        message_form = MessageForm(request.POST)
        if car_form.is_valid() and message_form.is_valid():
            message = Message.objects.create(
                title=message_form.cleaned_data['title'],
                body=message_form.cleaned_data['body']
            )
            obj = Car.objects.create(
                name=car_form.cleaned_data['name'],
                mileage=car_form.cleaned_data['mileage'],
                malfunction=car_form.cleaned_data['malfunction'],
                client_id=Client.objects.get(id_user_id=id_user).id,
            )
            mechs = car_form.cleaned_data['mechanics']
            obj.message = message
            obj.mechanics.add(*mechs)
            obj.save()
            return redirect(f"/showclient/{id_user}")
        else:
            return redirect('/')


def edit_client(request, id_user):
    if request.method == "GET":
        client_form = ClientForm()
        client = Client.objects.get(id_user_id=id_user)
        return render(request, 'formTemplate.html', {'form': client_form, 'client': client})
    else:
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client = Client.objects.get(id_user_id=id_user)
            client.first_name = client_form.cleaned_data['first_name']
            client.surname = client_form.cleaned_data['surname']
            client.phone_number = client_form.cleaned_data['phone_number']
            client.save()
            cars = Car.objects.filter(client=client.id)
            cars = list(cars)
            sex_list = ['women', 'men']
            sex = random.choice(sex_list)
            num = random.randint(1, 80)
            return render(request, 'clientInfo.html',
                          {"client": client, "cars": cars,
                           "sex": sex, "number": num})
        else:
            redirect('/')


def edit_mechanic(request, id_user):
    if request.method == "GET":
        mechanic_form = MechanicForm()
        mech = Mechanic.objects.get(id_user_id=id_user)
        return render(request, 'mechanicForm.html', {'form': mechanic_form, 'mech': mech})
    else:
        mechanic_form = MechanicForm(request.POST)
        if mechanic_form.is_valid():
            mech = Mechanic.objects.get(id_user_id=id_user)
            mech.first_name = mechanic_form.cleaned_data['first_name']
            mech.surname = mechanic_form.cleaned_data['surname']
            mech.department = mechanic_form.cleaned_data['department']
            mech.rating = mechanic_form.cleaned_data['rating']
            mech.experience = mechanic_form.cleaned_data['experience']
            mech.save()
            cars = Car.objects.filter(mechanics=mech.id)
            cars = list(cars)
            sex_list = ['women', 'men']
            sex = random.choice(sex_list)
            num = random.randint(1, 80)
            return render(request, 'mechanicInfo.html',
                          {"mechanic": mech, "cars": cars,
                           "sex": sex, "number": num})
        else:
            redirect('/')


def show_index(request):
    if request.method == "GET":
        current_user = request.user
        if current_user.is_authenticated:
            if current_user.groups.filter(name="Mechanics").exists():
                mechanic = Mechanic.objects.get(id_user_id=current_user.id)
                cars = Car.objects.filter(mechanics=mechanic.id)
                cars = list(cars)
                sex_list = ['women', 'men']
                sex = random.choice(sex_list)
                num = random.randint(1, 80)
                return render(request, 'mechanicInfo.html',
                              {"mechanic": mechanic, "cars": cars,
                               "sex": sex, "number": num})
            return redirect("showclient/" + str(current_user.id))
        else:
            return render(request, 'signUp.html', {})
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        user = User.objects.create_user(email=email,
                                        username=username,
                                        password=password)
        try:
            return redirect("/signin")
        except Exception:
            print("Incorrect data")
            return redirect("/")


def show_sign_in(request):
    current_user = request.user
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect("showclient/" + str(current_user.id))
        else:
            return render(request, 'signIn.html', {})
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        cur_user = User.objects.get(email=email)
        if not cur_user.check_password(password):
            return redirect("/signin")
        if Client.objects.filter(id_user_id=cur_user.id).exists() or \
                Mechanic.objects.filter(id_user_id=cur_user.id).exists():
            user = authenticate(username=cur_user.username, password=password)
            login(request, cur_user)
        else:
            user = authenticate(username=cur_user.username, password=password)
            obj = Client.objects.create(
                first_name=cur_user.username,
                id_user_id=user.id
            )
            obj.save()
            login(request, user)

        return redirect("/info")


def validate_username_email(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    response = {
        'taken_username': User.objects.filter(username__exact=username).exists(),
        'taken_email': User.objects.filter(email__exact=email).exists()
    }
    return JsonResponse(response)


def validate_mileage(request):
    mileage = int(request.GET.get('mileage', None))
    response = {
        'mileage_pos': mileage >= 0
    }
    return JsonResponse(response)
# Create your views here.
