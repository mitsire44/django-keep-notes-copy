from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import NoteForm
from .models import note
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'notes/home.html')


def signupuser(request):
    context = {'form':UserCreationForm()}
    if request.method=="GET":
        return render(request, 'notes/signupuser.html', context)
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('notes')

            except IntegrityError:
                return render(request, 'notes/signupuser.html', {'form':UserCreationForm(), 'error':'The username is taken!'})
        else:
            return render(request, 'notes/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match!'})

def loginuser(request):
    if request.method=='GET':
        return render(request, 'notes/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'notes/loginuser.html', {'form':AuthenticationForm(), 'error':'The username and password did not match'})
        else:
            login(request, user)
            return redirect('notes')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required
def notes(request):
    notes = note.objects.filter(user = request.user)
    return render(request, 'notes/notes.html', {'notes':notes})

@login_required
def createnote(request):
        if request.method=="GET":
            return render(request, 'notes/createnote.html', {'form':NoteForm()})
        else:
            note = NoteForm(request.POST)
            newNote = note.save(commit=False)
            newNote.user = request.user
            newNote.save()
            return redirect('notes')

@login_required
def viewnote(request, note_pk):
    fullnote=get_object_or_404(note, pk=note_pk, user=request.user)
    if request.method=='GET':
        form = NoteForm(instance=fullnote)
        return render(request, 'notes/note.html', {'fullnote':fullnote, 'form':form})
    else:
        form = NoteForm(request.POST, instance=fullnote)
        form.save()
        return redirect('notes')

@login_required
def search(request):
    if request.method=="POST":
        searched = request.POST['searched']
        anime = Review.objects.filter(title__contains=searched)
        return render(request, 'reviews/searchresultsrework.html', {'searched':searched, 'reviews':anime})
    else:
        return render(request, 'reviews/searchresultsrework.html', {})

@login_required
def filtercolours(request):
    if request.method=="POST":
        colour = request.POST['colour']
        notes = note.objects.filter(colour=colour, user=request.user)
        return render(request, 'notes/filtercolours.html', {'colour':colour, 'notes':notes})
    else:
        return render(request, 'notes/filtercolours.html', {})

@login_required
def deletenote(request, note_pk):
    fullnote=get_object_or_404(note, pk=note_pk, user=request.user)
    if request.method=='POST':
        fullnote.delete()
        return redirect('notes')

