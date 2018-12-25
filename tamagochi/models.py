from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
import time

from django.utils.timezone import utc
import datetime

class Tamagochi(models.Model):
    name = models.CharField(max_length=20)
    GENDER_CHOICES = (('F', 'Female',),('M', 'Male',))
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES)
    apperance = models.ImageField(upload_to="tamaEvolve", blank=True)
    apperanceNum = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    longitude = models.DecimalField(max_digits=20,decimal_places=12,null=True)
    latitude = models.DecimalField(max_digits=20,decimal_places=12,null=True)
    birthday = models.DateTimeField(auto_now_add=True)
    age = models.CharField(max_length=120, null=True, default=None)
    health = models.IntegerField(default=100)
    energy = models.IntegerField(default=100)
    happiness = models.IntegerField(default=100)
    wallet = models.IntegerField(default=1000)
    sickness = models.BooleanField(default=False)
    game_status = models.CharField(default="Not Ready",max_length=30)
    friends = models.ManyToManyField('Tamagochi',blank=True)
    friend_waitlist = models.ManyToManyField('self',related_name="waitlist",blank=True,symmetrical=False)
    user = models.ForeignKey(User, related_name="tamagochi", on_delete=models.CASCADE)
    play_innvitation=models.ManyToManyField('self',related_name="play_invitation",blank=True,symmetrical=False)
    current_game_room_id=models.IntegerField(null=True,blank=True,default=0)
    online=models.BooleanField(default=False)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    partner = models.ForeignKey('Tamagochi',related_name='partner2',blank=True, null=True, on_delete=models.CASCADE)
    partner_waitlist=models.ManyToManyField('self',related_name="partner_waitlist2",blank=True,symmetrical=False)


    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return self.name
    #search_friend_list html
    def html(self):
        return "<div id='friend_%s'><br> \
        <table><tr><td><img src='/static/media/tamaEvolve/%s/%s.png' id='photo_%s' class='friendItem hvr-bounce-in apart'></td>\
        <td><h6 id='name_%s' class='wareText apart' style='display: inline'>Name: %s</h6><br>\
        <p id='gender_%s'class='wareTextRed apart' style='display: inline'>Gender: %s</p></td>\
        <td><button id='invite-%s' class='btnPWD apart'>Invite</button></td>\
        </tr></table></div><br>" \
        %(self.id,self.apperanceNum,self.level,self.id,self.id,escape(self.name),self.id,escape(self.gender),self.id)
    #friend_list html
    def html2(self):
        return "<div class='row'><div class='wareList'>\
        <div class='col-md-4' >\
        <a href='othermap/%s'><img src='/static/media/tamaEvolve/%s/%s.png' class='friendItem2 hvr-bounce-in' >\
        </div>\
        <div class='col-md-6'>\
        <p class='wareText'>%s</p><p class='wareTextRed'>%s</p>\
        </div>\
        </div></div>" %(self.id,self.apperanceNum,self.level,escape(self.name),escape(self.gender))
    #friend_waitlist html
    def html3(self):
        return "<div id='waitlist-row-%s'>\
        <table><tr><td><img src='/static/media/tamaEvolve/%s/%s.png' id='photo_%s' class='friendItem hvr-bounce-in apart'></td>\
        <td><h6 id='waitlist-name-%s' class='wareText'>Name: %s</h6>\
        <p id='waitlist-gender-%s' class='wareTextRed'>Gender: %s</p></td></tr></table>\
        <button id='approve-%s'class='waitlistbtn'>Approve</button>\
        <button id='dismiss-%s'class='waitlistbtn'>Dismiss</button>\
        </div><br>" %(self.id,self.apperanceNum,self.level,self.id,self.id,escape(self.name),self.id,escape(self.gender),self.id,self.id)

    def html4(self):
        energy_percent = "{0:.0f}%".format(self.energy)
        happiness_percent = "{0:.0f}%".format(self.happiness)
        health_percent = "{0:.0f}%".format(self.health)
        return "<h4>HEALTH: %s/100</h4>\
                <div class='progress'>\
                <div class='progress-bar progress-bar-success progress-bar-striped active' role='progressbar' aria-valuenow='%s' aria-valuemin='0' aria-valuemax='100' style='width: %s'>\
                </div></div>\
                <h4>ENERGY: %s/100</h4>\
                <div class='progress'>\
                <div class='progress-bar progress-bar-warning progress-bar-striped active' role='progressbar' aria-valuenow='%s' aria-valuemin='0' aria-valuemax='100' style='width: %s'>\
                </div></div>\
                <h4>HAPPINESS: %s/100</h4>\
                <div class='progress'>\
                <div class='progress-bar progress-bar-danger progress-bar-striped active' role='progressbar' aria-valuenow='%s' aria-valuemin='0' aria-valuemax='100' style='width: %s'>\
                </div></div>"% (self.health, self.health, health_percent,
                                self.energy, self.energy, energy_percent,
                                self.happiness, self.happiness, happiness_percent,)

    def html5(self):
        return "<h4>%s</h4>" % (self.age)
    #invite multigame
    def html6(self):
        return "<li id='friend_%s'>\
    <img src='/static/media/tamaEvolve/%s/%s.png' id='photo_%s' class='friendItem hvr-bounce-in'>\
           <h6 id='name_%s' class='wareText'>%s</h6>\
           <p id='gender_%s'class='wareTextRed'>%s</p>\
           <button id='invite-%s' rel='%s' class='btn btn-info'>Invite</button>\
         </li>" \
        %(self.id,self.apperanceNum,self.level,self.id,self.id,escape(self.name),self.id,escape(self.gender),self.id,escape(self.current_game_room_id))
    #receive multigame invitation
    def html7(self):
        return "<li id='invitation-row-%s'>\
        <p id='invitation-name-%s'>%s</p>\
        <p id='invitation-gender-%s''>%s</p>\
        <p><button id='join-%s'rel='%s'>Join!</button></p>\
        <p><button id='dismiss-%s'>Dismiss</button></p>\
        </li>" %(self.id,self.id,escape(self.name),self.id,escape(self.gender),self.id,escape(self.current_game_room_id),self.id)
    #multigame ready room
    def html8(self):
        return "<div class='col-md-3' id='player_%s'>\
        <img src='/static/media/tamaEvolve/%s/%s.png' class='playersimg'>\
        <h4 class='playersfont'>Name:&nbsp;%s</h4>\
        <h4 class='playersfont player_status' id='status_%s'>Status:&nbsp;%s</h4>\
        </div> " % (self.user.id, self.apperanceNum, self.level, escape(self.name), self.user.id, escape(self.game_status))

class previousTama(models.Model):
    user = models.ForeignKey(User, related_name="preTamagochi",
                             on_delete=models.CASCADE)
    dead_date = models.DateTimeField(auto_now_add=True, unique=True)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    apperance = models.ImageField(upload_to="tamaEvolve", blank=True)
    level = models.IntegerField(default=1)
    age = models.CharField(max_length=120, null=True, default=None)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(blank=True)
    price = models.IntegerField()
    health = models.IntegerField(blank=True, null=True)
    energy = models.IntegerField(blank=True, null=True)
    happiness = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    item = models.ForeignKey(Item, related_name="item",on_delete=models.CASCADE)
    tamagochi = models.ForeignKey(Tamagochi, related_name="warehouse",on_delete=models.CASCADE)

    def __str__(self):
        return str((self.tamagochi.name, self.item.name))

class LoginLogoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    temp = models.DateTimeField(blank=True, null=True)
    length = models.DurationField(blank=True, null=True)

class Gameroom(models.Model):
    owner=models.ForeignKey('Tamagochi', on_delete=models.CASCADE)
    guests=models.ManyToManyField('Tamagochi',related_name="guests",blank=True,symmetrical=False)
    status=models.CharField(default="NotReady",max_length=30)
    room_active=models.BooleanField(default=True)
    winner=models.ForeignKey('Tamagochi', on_delete=models.CASCADE, null=True, related_name="winner")
    room_time = models.DateTimeField(auto_now_add=True)
    game_time = models.DateTimeField(null=True, blank=True)

class Gamerecord(models.Model):
    room = models.ForeignKey('Gameroom', on_delete=models.CASCADE)
    player = models.ForeignKey('Tamagochi', on_delete=models.CASCADE)
    score = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return str((self.room.id, self.player.name))

class Post(models.Model):
    pet=models.ForeignKey('Tamagochi', on_delete=models.CASCADE)
    text=models.CharField(max_length=150, blank=True, null=True)
    last_changed = models.DateTimeField(auto_now_add=True)
    agree_time=models.DateTimeField(auto_now=True)
    agree_pet=models.ManyToManyField(User,blank=True)
    agree_number=models.IntegerField(default=0)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()
    @property
    def html(self):
        Time = self.last_changed.__str__()
        modTime = Time.split(".")[0]
        return "<div  class='postItem'><div class='row'>\
        <div class='col-md-2'>\
        <img src='/static/media/tamaEvolve/%s/%s.png' class='author hvr-bounce-in'>\
        </div>\
        <div class='col-md-8' id='post-%s'>\
        <h5>Author: %s &nbsp; Active Time: %s</h5>\
        <h4>%s</h4>\
        </div>\
        <div class='col-md-2'>\
        <button id='agree-%s'class='hvr-grow-shadow thumbsupbtn glyphicon glyphicon-thumbs-up'> %s</button>\
        </div></div></div>" \
        %(self.pet.apperanceNum,self.pet.level,self.id,escape(self.pet),escape(modTime),escape(self.text),self.id,escape(self.agree_number))
