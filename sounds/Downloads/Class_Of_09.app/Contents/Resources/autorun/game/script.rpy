define beginMarker = "0.0"
define sceneAudio = ""
define endMarker = "0.0"
define waitTime = "0.0"
define drift = 0.0
define waitTag = ""
define line = ""
define tolerance = 0.5
define pad = .05
define playback_paused = False
define paused_position = 0.0
define current_line = ""
define current_character = None
define line_time_remaining = 0.0
define pause_start = 0.0
define pause_duration = 0.0

init python:
    import time
    renpy.music.register_channel("ambient","music",loop=True,tight=True)
    renpy.music.register_channel("sfx","music",loop=False,tight=True)
    renpy.music.register_channel("vo","music",loop=False,tight=True)

    def afterLoad():
        renpy.pause(1.0)

    config.after_load_callbacks = [afterLoad]
    preferences.show_empty_window = True

    def isclose(a,b,tolerance):
        return abs(a-b) < tolerance

    def seekvoice(event, interact=True, **kwargs):
        global beginMarker, tolerance, drift
        if(event == 'begin'):
            pos = renpy.music.get_pos('vo')
            if(pos is None):
                pos = float(beginMarker)
                drift = 0.0
                renpy.music.play("<from " + beginMarker + ">" + sceneAudio,'vo')
                return
            drift = pos - float(beginMarker)
            if(isclose(pos,float(beginMarker),tolerance) == False):
                renpy.music.play("<from " + beginMarker + ">" + sceneAudio,'vo')

    def setWait(begin, end):
        global beginMarker, endMarker, waitTime, waitTag, sceneAudio, current_line, drift
        beginMarker = str(begin)
        endMarker = str(end)
        waitTime = str((end - begin) - drift if drift >= 0 else (end - begin))
        waitTag = '{p=' + waitTime + '}{nw}' 

    def setVoiceTrack(name):
        global sceneAudio, beginMarker, endMarker, waitTime
        sceneAudio = name
        beginMarker = "0.0"
        endMarker = "0.0"
        waitTime = "0.0"
        drift = 0.0
        renpy.music.play(sceneAudio,'vo')
        renpy.music.set_pause(False, channel='vo')

    def killAudio():
        renpy.music.set_pause(True, channel='vo')
        renpy.music.set_pause(True, channel='ambient')

    def speak(c,line,resume = False):
        global pause_duration, waitTag, current_line, current_character, line_time_remaining
        current_line = line
        current_character = c
        if(resume == False):
            renpy.pause(0.0)
            renpy.checkpoint(renpy.say(c, line + waitTag))
        else:
            pause_duration = 0
            line_time_remaining = 0
            renpy.say(c.name,line)
        if(line_time_remaining > 0.0):
            p = line_time_remaining
            line_time_remaining = 0
            if(pause_duration >= p):
                speak(c, current_line + '{p=' + str(p) + '}{nw}',True)
            else:
                speak(c, current_line + '{p=' + str(pause_duration) + '}{nw}',True)

    
##add an optional pre-pause to the speak function 
    def game_unpause():
        global pause_duration
        if(pause_duration > 0):
            pause_duration += time.time() - pause_start
        else:
            pause_duration = time.time() - pause_start
        renpy.return_statement()

    def game_pause():
        global paused_position, endMarker, line_time_remaining, pause_start
        renpy.music.set_pause(True, channel='vo')
        renpy.music.set_pause(True, channel='ambient')
        pause_start = time.time()
        paused_position = renpy.music.get_pos('vo')
        line_time_remaining = float(endMarker) - paused_position

init:

    $config.enter_transition = None
    image black = Solid((0, 0, 0, 255))

transform transform_logo:
    on show:
        alpha 0 xalign 1.2 yalign 0.2 size (580.0,395.0)
        easein 1.0 alpha 1 xalign 0.88

screen pause_menu():
    tag menu

    on "show":
        action Function(game_pause)

    key "K_ESCAPE" action Function(game_unpause)
    key "mouseup_3" action Function(game_unpause)
    key "K_MENU" action Function(game_unpause)


    add "gui/nvl.png"
    style_prefix "main_menu"

    zorder 100

    hbox:
        frame:
            style "main_menu"

    add "gui/ClassOf09logo.png" at transform_logo

    vbox:
        xalign 0.5
        yalign 0.5
        #Menu options
        textbutton _("Resume"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3" 
            action Function(game_unpause)
        textbutton _("Options"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3" 
            action ShowMenu('pause_prefs')
        textbutton _("Save"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3" 
            action ShowMenu('pause_save')

        textbutton _("Main Menu"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3" 
            action [Stop("vo"),Stop("ambient"),MainMenu()]

style skip_button_text:
    size 50


screen disable_Controls():
    tag menu
    zorder 0

    key "mouseup_1" action NullAction()
    style_prefix "skip"

    vbox:
        spacing -5

        xalign 0.92
        yalign 1.0
        
        textbutton "Skip" action [Jump ("scene_0002"), Hide("disable_Controls")]




    


define NICOLE = Character("Nicole", callback=seekvoice)
define KYLAR = Character("Kylar", callback=seekvoice)
define GIRL_1 = Character("Ari", callback=seekvoice)
define CRISPIN = Character("Crispin", callback=seekvoice)
define GUY_1 = Character("Trody", callback=seekvoice)
define JEFFERY = Character("Jeffery", callback=seekvoice)
define TEACHER_1 = Character("Mr. Burleday", callback=seekvoice)
define JECKA = Character("Jecka", callback=seekvoice)
define MOM = Character("Mom", callback=seekvoice)
define GAMER_BROTHER = Character("Gamer Brother", callback=seekvoice)
define COP = Character("Cop", callback=seekvoice)
define COACH_COLBY = Character("Coach Colby", callback=seekvoice)
define MR_WHITE = Character("Mr. renWhite", callback=seekvoice)
define GUY_2 = Character("Kyle", callback=seekvoice)
define GIRL_2 = Character("Emily", callback=seekvoice)
define PRINCIPAL_LYNN = Character("Principal Lynn", callback=seekvoice)
define GUY_3 = Character("Hunter", callback=seekvoice)
define GIRL_3 = Character("Megan", callback=seekvoice)
define COUNSELOR = Character("Counselor", callback=seekvoice)
define TEACHER_2 = Character("TEACHER_2", callback=seekvoice)
define GIRL_4 = Character("Karen", callback=seekvoice)
define GUY_5 = Character("Braxton", callback=seekvoice)
define GIRL_5 = Character("Kelly", callback=seekvoice)
define EMT = Character("EMT", callback=seekvoice)
define LAWYER = Character("Lawyer", callback=seekvoice)
define none = Character("none", callback=seekvoice)
define BAND = Character("BAND", callback=seekvoice)

image gamer_brother flipped = im.Flip("gamer_brother.png", horizontal=True)
image nicole flipped = im.Flip("nicole.png", horizontal=True)
image nicole shirt flipped = im.Flip("nicole shirt.png", horizontal=True)
image nicole tanktop flipped = im.Flip("nicole tanktop.png", horizontal=True)
image crispin flipped = im.Flip("crispin.png", horizontal=True)
image nicole shirt flipped = im.Flip("nicole shirt.png", horizontal=True)
image nicole tanktop flipped = im.Flip("nicole tanktop.png", horizontal=True)
image girl_1 flipped = im.Flip("girl_1.png", horizontal=True)
image kylar flipped = im.Flip("kylar.png", horizontal=True)
image teacher_1 flipped = im.Flip("TEACHER_1.png", horizontal=True)
image guy_1 flipped = im.Flip("guy_1.png", horizontal=True)
image cop flipped = im.Flip("cop.png", horizontal=True)
image jeffery flipped = im.Flip("jeffery.png", horizontal=True)
image mom flipped = im.Flip("mom.png", horizontal=True)
image jecka flipped = im.Flip("jecka.png", horizontal=True)

transform leftstage:
    xalign 0.0

transform leftcenterstage:
    xalign 0.33

transform rightcenterstage:
    xalign 0.66

transform rightstage:
    xalign 1.0

transform off_right:
    xalign 1.4

transform off_left:
    xalign -0.4

transform off_farright:
    xalign 1.6

transform off_farleft:
    xalign -0.73
    
transform percsuperleft:
    xalign 0.228
    yalign 0.7

transform percrightcenter:
    xalign 0.65
    yalign 0.7

transform percfall:
    xalign 0.45
    yalign 5

transform percnotasright:
    xalign 0.56
    yalign 0.7

transform percentrist:
    xalign 0.45
    yalign 0.7    
    
transform percleftstage:
    xalign 0.456
    yalign 0.7

image opening cutscene = Movie(play="opening.webm")

image percpop = Movie (play="percpop.webm")


label start:
    $quick_menu = False
    $_game_menu_screen = "pause_menu"
    show black
    show opening cutscene
    show screen disable_Controls
    $renpy.pause(140,hard=True)
    jump scene_0002

label scene_0002:
    hide screen disable_Controls
    $setVoiceTrack("audio/Scenes/0002.mp3")
    
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1
    scene
    show black

    show school front with Pause(2.252):
        truecenter zoom 1.0
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.627 truecenter zoom 1.1

    scene school int 1:

    #xalign is the relative horizontal position
    #                ______________________
    #               |                      |
    # xalign 0.0 -->|                      | <- xalign 1.0
    #               |______________________|

    show girl_1:
        rightstage 
    
    # linear is a tween statement
    # you provide it with the number of seconds you want the tween to last
    # followed by the property you want to tween to
    $quick_menu = True
    show kylar:
        off_right
        linear 2.5 rightcenterstage     
    play ambient "audio/Ambience/Hallway_Ambience.mp3"


    $setWait(2.627,8.258)
    $speak(KYLAR, "Hey so for the senior prank this year what if we like parked our cars where we don't usually park them!")
    
    show kylar:
        rightcenterstage

    $setWait(8.258,10.093)
    $speak(GIRL_1, "Oh my god that is so funny!")

    show kylar:
        rightcenterstage
        2.0
        linear 6.0 off_left  

    show girl_1:
        rightstage
        5.0
        linear 3.0 off_right

    show nicole:
        off_left
        5.0
        linear 3.0 leftcenterstage

    $setWait(10.093,16.307)
    $speak(KYLAR, "Heh yeah math class this year with Mr. Burleday huh yeah like fuck Mr. Burleday dude ha ha ha ha!")


    $setWait(16.307,21.229)
    $speak(NICOLE, "God they are never funny. It's like the girls just laugh to avoid sexual assault.")
    
    show crispin:
        off_right
        linear 3.0 xalign 0.71
        
    show nicole:
        leftcenterstage
        
    show kylar:
        off_left


    $setWait(21.229,23.69)
    $speak(CRISPIN, "Hey yo you new to this educational prison?")
    
    show girl_1:
        off_right
    
    $setWait(23.69,26.234)
    $speak(NICOLE, "Ha ha ha ha ha wow yeah that was funny.")
    
    show kylar:
        off_left
    
    $setWait(26.234,31.99)
    $speak(CRISPIN, "Yeah I'm getting into like humor and stuff-- anyway you know anyone around here? Know where your classes are?")
    
    show crispin:
        xalign 0.71
    
    $setWait(31.99,36.1)
    $speak(NICOLE, "I mean kinda, there's like numbers on the doors I think I can figure it out.")
   
    $setWait(36.1,41.958)
    $speak(CRISPIN, "No no no no no I could show you around. Like a school tour? You wanna do that? You up for that?")
    

menu:
        "HUMOR THE SCHOOL TOUR":
            jump scene_0003
        "DECLINE AND GO STRAIGHT TO CLASS":
            jump scene_0004
        "TELL HIM OFF AND CUT CLASS":
            jump scene_0005
label scene_0003:

    $setVoiceTrack("audio/Scenes/0003.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3"

    scene school courtyard
    
    show nicole:
        xalign -0.7
        linear 8  leftstage
        
    show crispin flipped:
        off_left
        linear 8 leftcenterstage
    
    $setWait(0.289,8.755)

    $speak(CRISPIN, "Yeah so then my friend got the DLC, that's downloadable content, it's like 10 dollars like dude kinda not worth it for the gun.")
    $setWait(8.755,12.092)

    $speak(NICOLE, "Why are you talking to me about video games?")
    $setWait(12.092,17.306)
    
    show crispin:
        leftcenterstage
        
    show nicole:
        leftstage
    
    $speak(CRISPIN, "Just something y'know... uh.. what you don't like play video games or something?")
    $setWait(17.306,24.146)
    $speak(NICOLE, "I'm a thin girl do I fucking look like I play video games? I'd rather play dead at a necrophilia convention.")
    $setWait(24.146,29.568)
    $speak(CRISPIN, "Oh.. well... yeah y'know...")
    $setWait(29.568,31.82)
    $speak(NICOLE, "I know what?")
    $setWait(31.82,36.366)
    $speak(CRISPIN, "Did.. did you hear about how Mountain Dew makes guys sterile?")
    $setWait(36.366,40.871)
    $speak(NICOLE, "Yeah, from you and every other guy who reads the internet to try to be interesting.")
    $setWait(40.871,44.917)

        
    $speak(GUY_1, "Ha nice rollie backpack you fuckin' four-eyed double dick suckin' bitch!")
    $setWait(44.917,49.129)
    show nicole:
        leftstage
        linear 0.3 off_farleft
        
    show crispin:
        leftcenterstage
        linear 0.3 off_left
        
    show jeffery:
        off_farright
        linear 0.3 rightstage
        
    show guy_1 flipped:
        off_right
        linear 0.3 rightcenterstage
  

    $speak(JEFFERY, "Hey stop kicking it, this backpack holds priceless reading materials!")
    $setWait(49.129,52.799)
    $speak(GUY_1, "Oh yeah like what? The Bernstein Bears Make Eye Contact?")
    $setWait(52.799,58.597)
    $speak(JEFFERY, "Hey what is this? 4th grade? It is home to some of my favorite manga books.")
    $setWait(58.597,60.974)
    $speak(GUY_1, "Manga... What is that like Asian or something?")
    $setWait(60.974,66.897)
    $speak(JEFFERY, "Japanese thank you! Some of which go on to be very popular television shows.")
    $setWait(66.897,71.151)
    $speak(GUY_1, "Wait can't you watch half of those on cartoon channels? Why the hell would you read it?")
    $setWait(71.151,73.529)
    $speak(JEFFERY, "Rggghh! That's it!")
    $setWait(73.529,76.573)
    
    show nicole:
        xalign -0.5
        linear 2 leftcenterstage
       
    
    $speak(NICOLE, "Dude how do you care about anything this much?")
    $setWait(76.573,77.783)
    
    show guy_1:
        rightcenterstage
    
    show crispin flipped:
        off_farleft
        linear 4 leftstage
    
    $speak(JEFFERY, "What do you mean?")
    $setWait(77.783,81.787)
    
    show guy_1:
        rightcenterstage
        
    $speak(NICOLE, "Like okay he thinks your Chinese cartoon books are stupid, why defend it?")
    $setWait(81.787,85.749)
    $speak(JEFFERY, "Stay out of this you.. you girl!")

menu:
        "DOUBLE DOWN ON THE VERBAL ABUSE":
            jump scene_0006
        "JUST WATCH HIM GET BEAT UP":
            jump scene_0007
label scene_0004:

    $setVoiceTrack("audio/Scenes/0004.mp3")
    scene school int 1
    show crispin:
        xalign 0.71
        
    show nicole:
        leftcenterstage
    $setWait(0.129,7.345)
    $speak(NICOLE, "School tour um... that sounds nicely mediocre but I'm just gonna go to class, see ya.")
    $setWait(7.345,14.018)
    show nicole flipped:
        leftcenterstage
        linear 4 off_left
    $speak(CRISPIN, "Oh well yeah I'm Crispin by the way. Yeah we should hang out some time. Yeah okay! Alright bye yeah!")
    $setWait(14.018,19.273)
    
    
    scene classroom int 2
    play ambient "audio/Ambience/Classroom_Ambience.mp3"
    
    
    show teacher_1:
        leftcenterstage
        
    show nicole:
        off_left
        linear 2 leftstage
    
    $speak(TEACHER_1, "Oh you must be new. Yes please take a seat next to Jeffery.")
    $setWait(19.273,20.983)
    
    show teacher_1:
        leftcenterstage
        linear 1.6 off_left
        
    show nicole:
        leftstage
        linear 2 rightcenterstage
        
    show jeffery:
        off_right
        linear 1 rightstage

    $speak(JEFFERY, "Hey.")
    $setWait(20.983,22.819)
    $speak(NICOLE, "...")
    $setWait(22.819,29.325)
    $speak(JEFFERY, "Hey so uh... I guess... I guess we're lab partners huh?")
    $setWait(29.325,31.619)
    $speak(NICOLE, "I guess.")
    $setWait(31.619,33.496)

    $speak(JEFFERY, "Not a big talker, are ya?")
    $setWait(33.496,37.083)

    $speak(NICOLE, "I don't know you. Are you just chummy with everyone you meet?")
    $setWait(37.083,41.754)

    $speak(JEFFERY, "Not everyone. But if they look the type to like anime then may as well, right?")
    $setWait(41.754,44.924)
    
    show nicole:
        rightcenterstage
        linear 1 leftcenterstage

    $speak(NICOLE, "I'm sorry, I look like I like anime? How do I fix that?")
    $setWait(44.924,49.137)
    
    show jeffery:
        rightstage
        linear 1 rightcenterstage

    $speak(JEFFERY, "No no that's a good thing! It means you're cool and different.")
    $setWait(49.137,50.638)

    $speak(NICOLE, "...And 300 pounds.")
    $setWait(50.638,51.264)

    $speak(JEFFERY, "What was that?")
    $setWait(51.264,55.101)

    $speak(NICOLE, "Oh nothing was just converting British currency in my head.")
    $setWait(55.101,60.314)

    $speak(JEFFERY, "Cool, see? Um, well the teacher said I'm Jeffery, what's your name?")

menu:
        "THIS FREAK IS NOT GETTING MY NAME":
            jump scene_0008
        "PRETEND TO BE NICE":
            jump scene_0009
label scene_0005:

    $setVoiceTrack("audio/Scenes/0005.mp3")
    
    
    scene school int 1
    
    show nicole:
        leftcenterstage
        
    show crispin:
        xalign 0.71
    
    $setWait(0.123,5.003)

    $speak(NICOLE, "I'm gonna be honest, you seem like the most boring piece of shit I've ever met.")
    $setWait(5.003,5.754)

    $speak(CRISPIN, "Huh?")
    $setWait(5.754,12.844)
    $speak(NICOLE, "Well wait, most I've ever met would mean you stand out in some way. You're a very run of the mill waste of time.")
    $setWait(12.844,15.18)
    $speak(CRISPIN, "I don't get it, what'd I do?")
    $setWait(15.18,17.39)
    $speak(NICOLE, "You have time for the whole list?")
    $setWait(17.39,18.141)
    $speak(CRISPIN, "I guess--")
    $setWait(18.141,25.482)
    $speak(NICOLE, "First you wear classic rock T-shirts from Walmart. Girls don't compliment how you dress so you settled for old people hi-fiving you for being retro.")
    $setWait(25.482,27.484)
    $speak(CRISPIN, "Nah people think I'm cool--")
    $setWait(27.484,41.122)
    $speak(NICOLE, "Rapid fire of assumptions, tell me if I get any wrong. You call your bicycle a BMX, like energy drinks, take pictures of your skateboarding wounds, mention to anyone they can't get addicted to marijuana, and own a guitar pick necklace.")
    $setWait(41.122,46.002)
    
    show nicole:
        leftcenterstage
        pause 1.5
        linear 2 off_right
    
    $speak(CRISPIN, "Well... alright I'll see you later then.")
    $setWait(46.002,48.379)
    
    scene school int 2
    
    show nicole:
        off_left
        linear 3 leftcenterstage
        
    show kylar:
        rightstage
        linear 1 rightcenterstage

    $speak(KYLAR, "Hey I've seen your ass around here before.")
    $setWait(48.379,50.131)
    $speak(NICOLE, "It's my first day, you sure about that?")
    $setWait(50.131,52.342)
    $speak(KYLAR, "Whatever all you hot girls look the same.")
    $setWait(52.342,53.843)
    $speak(NICOLE, "That was real discreet.")
    $setWait(53.843,57.096)
    $speak(KYLAR, "Gotta be, especially cutting under this school's security.")
    $setWait(57.096,57.847)
    $speak(NICOLE, "Uh huh.")
    $setWait(57.847,61.976)
    $speak(KYLAR, "And a girl like you skipping the first day? Are you bad bitch or what?")
    $setWait(61.976,63.561)
    $speak(NICOLE, "I'm an abysmal bitch.")
    $setWait(63.561,67.732)
    $speak(KYLAR, "Fuckin' cool rock on. So what do you do here? Like cheerleading?")
    $setWait(67.732,69.15)
    $speak(NICOLE, "Doesn't pay so no.")
    $setWait(69.15,76.324)
    $speak(KYLAR, "Well I'm on the lacrosse team. Last season we went 7-5 like above 500 not bad. It's my life pretty much.")
    $setWait(76.324,80.787)
    $speak(NICOLE, "How can you make lacrosse your life? There's no pro league for it, is there?")
    $setWait(80.787,90.38)
    $speak(KYLAR, "Well.. I'm sure they're out there. Besides we only lost 5 games cause I fucked up my knee and couldn't play the rest of the season. But it's pretty bad ass cause they keep giving me Percocet.")
    $setWait(90.38,92.632)
    $speak(NICOLE, "Cool, seriously? How much?")
    $setWait(92.632,99.43)
    $speak(KYLAR, "Enough to demotivate an elephant. I got 'em right here you wanna do 'em with me? They only kinda get you fucked up but it's good.")

menu:
        "DECLINE HIS FREE DRUGS":
            jump scene_0010
        "POP PERCS WITH HIM":
            jump scene_0011
label scene_0006:

    $setVoiceTrack("audio/Scenes/0006.mp3")
    scene school courtyard
    
    show nicole:
        leftcenterstage
        
    show jeffery:
        rightstage
        
    show crispin flipped:
        leftstage
        
    show guy_1:
        rightcenterstage
    
    $setWait(0.202,2.788)

    $speak(NICOLE, "What the fuck you greasy bitch I was trying to help you.")
    $setWait(2.788,7.793)
    show jeffery at right
    $speak(JEFFERY, "I don't need help from someone who misnationalizes my Japanese manga books!")
    $setWait(7.793,10.88)
    
    show guy_1 flipped:
        rightcenterstage

    $speak(GUY_1, "\"Japanese manga books\" that's literally you, that's what you sound like.")
    $setWait(10.88,15.343)
    $speak(NICOLE, "Yeah first time you talk to a girl and you correct her on the origin of your backwards picture books.")
    $setWait(15.343,18.888)
    $speak(JEFFERY, "They're not backwards they just read right-to-left!")
    $setWait(18.888,20.222)
    $speak(GUY_1, "No one cares!")
    $setWait(20.222,30.983)
    $speak(JEFFERY, "I care! And the Youtube anime community cares too! Like NaruParty13 he's got 1,600 subscribers, do you have that many?")
    $setWait(30.983,33.444)
    $speak(NICOLE, "Why would you upload videos to Youtube?")
    $setWait(33.444,35.988)
    $speak(JEFFERY, "How else do you think videos get there?")
    $setWait(35.988,42.078)
    $speak(NICOLE, "It's for watching TV shows, you don't fucking participate in it. What am I gonna go on Youtube and get digitally molested?")
    $setWait(42.078,44.497)
    $speak(JEFFERY, "No it- ughhh!")
    $setWait(44.497,46.332)
    $speak(GUY_1, "Ha ha ha you gonna transform?")
    $setWait(46.332,53.047)
    $speak(JEFFERY, "Whatever everything's fine! My Mom said the bullies go nowhere and smart kids like me become notable adults.")
    show crispin:
        leftstage
        linear 2.2 off_left
    $setWait(53.047,61.013)
    $speak(NICOLE, "The most notable thing you could do is killing yourself before graduation. Then your Dad can cry in front of school assemblies next to a black and white photo of you.")
    $setWait(61.013,63.766)
    $speak(JEFFERY, "Wha- ...no...")
    $setWait(63.766,64.642)
    $speak(GUY_1, "Little bitch.")
    
    show jeffery flipped:
        rightstage
        linear 1.5 off_farright
    $setWait(64.642,68.354)
    $speak(JEFFERY, "Wahhh!! I'm straight!")
    
    show guy_1:
        rightcenterstage
    $setWait(68.354,71.649)
    $speak(GUY_1, "So hey you're like pretty cool, what's your name?")
    $setWait(71.649,74.443)
    $speak(NICOLE, "Well my last name's \"You\". Most people just call me that.")
    $setWait(74.443,76.779)
    $speak(GUY_1, "You? What is that like Asian? That's hot.")
    $setWait(76.779,78.656)
    $speak(NICOLE, "Yeah Grandma had yellow fever.")
    $setWait(78.656,81.7)
    $speak(GUY_1, "Cool yeah... So what's your first name?")
    $setWait(81.7,83.035)
    $speak(NICOLE, "Fuck.")
    
    stop ambient fadeout 1
    jump scene_0014
label scene_0007:
    window show
    $setVoiceTrack("audio/Scenes/0007.mp3")
    scene school courtyard
    
    show nicole:
        leftcenterstage
        
    show jeffery:
        rightstage
        
    show crispin flipped:
        leftstage
        
    show guy_1:
        rightcenterstage
        
    $setWait(0.165,1.5)

    $speak(NICOLE, "I'll just let this play out.")
    
    show guy_1 flipped:
        rightcenterstage
    
    $setWait(1.5,3.419)

    $speak(GUY_1, "I should beat your ass for liking anime.")
    $setWait(3.419,5.087)

    $speak(JEFFERY, "Wha- what're you talking about?")
    $setWait(5.087,6.255)
    $speak(NICOLE, "Yeah do it, I'm bored.")
    $setWait(6.255,7.881)


    $speak(CRISPIN, "Yeah do it yeah yeah.")
    
    show guy_1 flipped:
        rightcenterstage
        linear 3 rightstage
        
    show black onlayer screens:
        alpha 0.0
        linear 1 alpha 1.0
        1.8
        linear 0.8 alpha 0.0
        
    stop ambient fadeout 1

    
    $setWait(7.881,10.259)
    $speak(JEFFERY, "Don't pull my hair!")
    
    show guy_1 flipped:
        rightcenterstage   
        
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1
    
    show jeffery broken:
        rightstage
    
    $setWait(10.259,12.386)
    $speak(GUY_1, "Ah I broke his glasses, I gotta split!")
    
    show jeffery broken:
        rightstage
    
    show guy_1 flipped:
        rightcenterstage
        pause 2.4
        linear 0.9 off_farright
        
    show crispin flipped:
        leftstage
        pause 2.4
        linear 1.6 off_right
        
    $setWait(12.386,16.682)
    $speak(CRISPIN, "Oh yeah me too I'm on probation, I'll catch you around!")
    
    show jeffery broken:
        rightstage
        linear 2 rightcenterstage
    
    $setWait(16.682,18.684)
    $speak(JEFFERY, "...Why aren't you running off with them?")
    $setWait(18.684,21.645)

    $speak(NICOLE, "They're pussies, I'm not afraid to watch someone grovel in pain.")
    $setWait(21.645,28.569)
    $speak(JEFFERY, "Well they're all just assholes. That guy's been making fun of me for liking anime since the 6th grade.")
    $setWait(28.569,30.696)
    $speak(NICOLE, "Then just stop liking anime?")
    $setWait(30.696,35.534)
    $speak(JEFFERY, "But I can't do that, anime is my favorite thing ever, my life!")
    $setWait(35.534,40.748)
    $speak(NICOLE, "How are you emotionally invested in consumption? Are you trying to make anime? I don't get it.")
    $setWait(40.748,46.378)
    $speak(JEFFERY, "Kinda, I make fan art based on the works of Sento Takahashi")
    $setWait(46.378,49.423)
    $speak(NICOLE, "You know that anime will exist with or without you, right?")
    $setWait(49.423,52.051)
    $speak(JEFFERY, "No! Wait what do you mean?")
    $setWait(52.051,57.473)
    $speak(NICOLE, "Like Senti Takimokey whatever the fuck his name is, if you died he wouldn't care, he wouldn't even know.")
    $setWait(57.473,58.807)
    $speak(JEFFERY, "What's your point?")
    $setWait(58.807,61.81)
    $speak(NICOLE, "How do you give a fuck about anything that doesn't give a fuck about you?")
    $setWait(61.81,69.151)
    $speak(JEFFERY, "Hey in a translated newsletter he said \"thank you\" to each and every one of his fans! That includes me!")
    $setWait(69.151,70.736)
    $speak(NICOLE, "Oh he writes in English?")
    $setWait(70.736,73.614)
    $speak(JEFFERY, "No his fan club translated it from Japanese.")
    $setWait(73.614,77.91)
    $speak(NICOLE, "That's my point. He can't even talk to you, you think he cares about you?")
    $setWait(77.91,80.079)
    $speak(JEFFERY, "Well.. uh..")
    $setWait(80.079,84.083)
    $speak(NICOLE, "Anyway, you wanna stick to getting beat up over children's media? I'll leave you to it.")
    $setWait(84.083,84.958)
    $speak(JEFFERY, "Wait!")
    $setWait(84.958,86.752)
    $speak(NICOLE, "Huh what?")
    $setWait(86.752,91.215)
    $speak(JEFFERY, "...Thanks for talking to me. Not many people are as nice to me as you are.")
    $setWait(91.215,93.467)
    $speak(NICOLE, "That was nice to you? God dammit.")
    $setWait(93.467,97.179)
    $speak(JEFFERY, "Yeah I'm Jeffery by the way. What's your name?")
    $setWait(97.179,99.056)
    $speak(NICOLE, "Ugh.. Nicole.")
    $setWait(99.056,102.059)
    $speak(JEFFERY, "Wow.. okay.. bye Nicole.")
    
    show nicole flipped:
        leftcenterstage
        linear 3 off_left
    
    $setWait(102.059,103.268)
    $speak(NICOLE, "Yeah yeah okay.")
    
    stop ambient fadeout 1
    jump scene_0014
label scene_0008:

    $setVoiceTrack("audio/Scenes/0008.mp3")
    
    scene classroom int 2
    
    show nicole:
        leftcenterstage
        
    show jeffery:
        rightcenterstage
    

    $setWait(0.251,3.88)

    $speak(NICOLE, "What so you can look me up on MySpace or something? No thanks.")
    $setWait(3.88,6.966)

    $speak(JEFFERY, "Well we're gonna get to know each other anyway, right?")
    $setWait(6.966,15.349)
    $speak(NICOLE, "Probably not. Probably after this week we won't even talk anymore. I've moved to a lot of different schools so I'm fully aware you're using the new kid grace period.")
    $setWait(15.349,17.977)
    $speak(JEFFERY, "What's \"new kid grace period\"?")
    $setWait(17.977,32.366)
    $speak(NICOLE, "Ugh.. it's where the outcasts squeeze all the interaction they can out of new kids way above their social status. So when the new kids get here it's awkward, they don't know who's who. They'll humor any conversation or friendship until they find the people on their social level.")
    $setWait(32.366,34.452)
    $speak(JEFFERY, "How do you know I'm not on your social level?")
    $setWait(34.452,38.581)
    $speak(NICOLE, "Fucking look at you. Listen to how you talk \"How do you know I'm not\"-- shut the fuck up.")
    $setWait(38.581,40.166)
    $speak(JEFFERY, "Hey I didn't do anything!")
    $setWait(40.166,49.425)
    $speak(NICOLE, "I know, it's what you will do. I've had my ear talked off about comics, laser swords, lowering the age of consent, ninja hand signs-- just all that weird shit.")
    $setWait(49.425,53.596)
    $speak(JEFFERY, "You know the other pretty girls here are a lot nicer than you are.")
    $setWait(53.596,55.89)
    $speak(NICOLE, "They talk to you cause it's funny, get a clue.")
    $setWait(55.89,58.017)
    $speak(JEFFERY, "Yeah, a lot of people say I'm funny.")
    $setWait(58.017,60.686)
    $speak(NICOLE, "Oh you're funny? Tell me a joke.")
    $setWait(60.686,66.15)
    $speak(JEFFERY, "...Oh well, it's more like in the moment, you had to be there kind of funny.")
    $setWait(66.15,69.946)
    $speak(NICOLE, "Okay, Jeffery, you want me to save you years of guessing?")
    $setWait(69.946,71.53)
    $speak(JEFFERY, "Yeah sure, how?")
    $setWait(71.53,75.952)
    $speak(NICOLE, "They're not laughing with you, they're laughing at you cause they'll never have sex with you.")
    $setWait(75.952,81.415)
    $speak(JEFFERY, "Ah, I got ya there! A lot of the girls here said they're saving themselves for me.")
    $setWait(81.415,83.668)
    $speak(NICOLE, "Christ, they make it that obvious here?")
    $setWait(83.668,85.753)
    $speak(JEFFERY, "Yeah they're kinda easy if you ask me.")
    $setWait(85.753,93.511)
    show nicole:
        leftcenterstage
        pause 2.95
        xzoom -1
        linear 3 off_left
        
    $speak(NICOLE, "No it-- ugh... Believe what you want, I'm going to lunch.")
    $setWait(93.511,97.014)
    $speak(JEFFERY, "I'm funny, I know I am.")
    jump scene_0015
label scene_0009:

    $setVoiceTrack("audio/Scenes/0009.mp3")
    scene classroom int 2
    
    show nicole:
        leftcenterstage
        
    show jeffery:
        rightcenterstage
        
    $setWait(0.256,1.758)

    $speak(NICOLE, "I'm Nicole, hi.")
    $setWait(1.758,3.802)

    $speak(JEFFERY, "Huh, that's a nice name.")
    $setWait(3.802,4.636)
    $speak(NICOLE, "Thanks!")
    $setWait(4.636,8.765)
    $speak(JEFFERY, "Uh hehehe... So what animes do you like?")
    $setWait(8.765,13.645)
    $speak(NICOLE, "Um can't say I know too many animes, but I'd like to learn, which ones do you like?")
    $setWait(13.645,18.233)
    $speak(JEFFERY, "Well I don't really like some of the ones other guys like...")
    $setWait(18.233,21.736)
    $speak(NICOLE, "Oh so you're like really into it? Really hip, you don't like the popular stuff?")
    $setWait(21.736,32.372)
    $speak(JEFFERY, "Mmm some are popular it's more the genre. A lot of anime is kung-fu laser beam action, I like the animes with the girls.")
    $setWait(32.372,34.29)
    $speak(NICOLE, "Mhm so what do like about 'em?")
    $setWait(34.29,40.088)
    $speak(JEFFERY, "I don't know, th-they're just really cute, I get crushes on them.")
    $setWait(40.088,43.883)
    $speak(NICOLE, "Oh you get crushes on cartoons? That's pretty cool.")
    $setWait(43.883,49.389)
    $speak(JEFFERY, "Thanks yeah. And something else but... I should probably keep it a secret.")
    $setWait(49.389,51.391)
    $speak(NICOLE, "Hey hey no, come on tell me.")
    $setWait(51.391,53.726)
    $speak(JEFFERY, "I don't know, I just met you.")
    $setWait(53.726,60.859)
    $speak(NICOLE, "Here let's make a deal. You carry the load on this science lab today, and I'll keep your secret safe forever. I swear.")
    $setWait(60.859,65.947)
    $speak(JEFFERY, "Hm, okay that sounds like a fair deal to me. I'll tell you at lunch.")
    $setWait(65.947,67.615)
    $speak(NICOLE, "Cool I can't wait.")
    $setWait(67.615,71.411)
    $speak(JEFFERY, "Now you just sit back, I'll get us an A for sure!")
    
    stop ambient fadeout 1
    
    jump scene_0016
label scene_0010:

    $setVoiceTrack("audio/Scenes/0010.mp3")
    scene school int 2
    
    show nicole:
        leftcenterstage
        
    show kylar:
        rightcenterstage
    
    $setWait(0.209,4.547)

    $speak(NICOLE, "Like I'd love to, but I kinda make too good of decisions to get high with a stranger.")
    $setWait(4.547,10.178)

    $speak(KYLAR, "Aw come on don't be a pussy we fuckin' go to the same school. I'm a student athlete, people know me here.")
    $setWait(10.178,16.225)
    $speak(NICOLE, "Yeah \"student athlete's\" kinda the red flag here? If I pop too many I'm gonna wake up with my thighs covered in butter.")
    $setWait(16.225,20.605)
    $speak(KYLAR, "Bro I have done literally nothing to give you this impression of me.")
    $setWait(20.605,24.609)
    $speak(NICOLE, "You ever played with a sleeping teammate's ass?")
    $setWait(24.609,27.236)
    $speak(KYLAR, "Well... Like not in a gay way.")
    $setWait(27.236,27.862)
    $speak(NICOLE, "Uh huh.")
    $setWait(27.862,28.738)
    $speak(KYLAR, "How is that gay?")
    show nicole flipped:
        leftcenterstage
        linear 3 off_left
    
    $setWait(28.738,33.785)
    $speak(NICOLE, "Whatever I'm going to lunch. It was nice meeting you, very straight non-rapist.")
    
    show kylar:
        rightcenterstage
        linear 5 leftstage
    $setWait(33.785,36.412)
    $speak(KYLAR, "Heh yeah, makin' friends.")
    jump scene_0017
label scene_0011:

    $setVoiceTrack("audio/Scenes/0011.mp3")
    scene school int 2
    
    show nicole:
        leftcenterstage
        
    show kylar:
        rightcenterstage
        
    
    $setWait(0.248,2.542)

    $speak(NICOLE, "Free Percocet? Hell yeah hand it over.")
   
    $setWait(2.542,8.006)
    
    show pills full:
        percrightcenter
        linear 0.12 xalign 0.455 yalign 0.65 rotate 345.0


    show percpop onlayer screens:
        alpha 0.0
        3
        linear .7 alpha 1.0
        2
        linear 1.5 alpha 0.0
        
    stop ambient fadeout 4.9

    $speak(KYLAR, "This is actually my Mexican cartel supply but it probably won't kill ya.")
    


    show nicole:
        leftstage
    show pills full:
        xalign 0.22 yalign 0.65 rotate 345.0
        
    show kylar:
        leftcenterstage
    $setWait(8.006,11.926)

    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1

    $speak(NICOLE, "My feet feel great I could fall asleep standing right now.")
    $setWait(11.926,13.678)
    
    show percpop onlayer screens:
        alpha 0.0
    
    $speak(KYLAR, "Yeah I told you it was good shit.")
    $setWait(13.678,18.808)
    show teacher_1:
        off_right
        linear 1.7 leftcenterstage
        pause 1.85
        im.Flip("teacher_1.png", horizontal=True, vertical=False)
        
    show kylar:
        leftcenterstage
        pause 1.5
        linear 0.3 rightcenterstage
    show pills full:
        pause 0.35
        linear 0.09 yalign 0.7 xalign 0.28
        pause 1.15
        linear 0.2155 yalign 0.7 xalign 0.545
        
    $speak(TEACHER_1, "I'm sorry are we lost? Both of you should be in class, this isn't a skip period!")
    $setWait(18.808,22.228)

    show pills full:
        linear 0.15 yalign 0.7 xalign 0.72
        linear 0.15 yalign 0.9 xalign 0.55 rotate 30.0
        yalign 2.0 xalign 2.0
    show kylar:
        xzoom -1
        pause 0.5
        xzoom 1        
   


    
    $speak(KYLAR, "Oh fuck! Um, hey dude we were just on our way y'know?")

    

    show kylar:
        rightcenterstage

    hide pills full
    
    
    show teacher_1 flipped:
        linear 0.2 xalign 0.33 yalign 0.0
        pause 1.1
        linear 0.2 xalign 0.66 yalign 0.0
        linear 0.2 xalign 0.33 yalign 0.0
    show pills full:
        yalign -1.0 xalign 0.555
        pause 1.65
        yalign 0.35 xalign 0.555
        linear 0.75 yalign 2.0 xalign 0.4 rotate 270
 

    $setWait(22.228,24.272)
    $speak(TEACHER_1, "What are you hiding there?")
        
    
    $setWait(24.272,25.231)
    $speak(NICOLE, "Oh shit.")
   
    show teacher_1 flipped:
        pause 1.68
        linear 0.11 xalign 0.45
        pause 1.2
        xzoom -1
        pause 1.43
        linear 0.11 xalign 0.35



    $setWait(25.231,31.404)
    $speak(TEACHER_1, "Prescription pills? Whose are these? Actually it doesn't matter, you're both in big trouble!")

menu:
        "PIN IT ON THE OTHER GUY":
            jump scene_0012
        "SHARE THE BLAME":
            jump scene_0013
label scene_0012:

    $setVoiceTrack("audio/Scenes/0012.mp3")
    scene school int 2
    
    show nicole:
        leftstage
        
    show teacher_1:
        leftcenterstage
        
    show kylar:
        rightcenterstage
    
    $setWait(0.251,1.419)

    $speak(NICOLE, "Wait wait what!?")
    $setWait(1.419,2.712)

    $speak(TEACHER_1, "Oh don't play dumb.")
    $setWait(2.712,12.055)
    $speak(NICOLE, "I didn't do anything, I was on my way back from the bathroom and this guy just stopped me trying to sell his.. Persoket Per- um.. I don't know but he won't leave me alone.")
    $setWait(12.055,13.014)

    $speak(KYLAR, "Aw come on.")
    
    show teacher_1 flipped:
        leftcenterstage
    
    $setWait(13.014,16.726)
    $speak(TEACHER_1, "Trying to find yet another customer huh, Kylar? Come with me!")
    $setWait(16.726,19.27)
    $speak(KYLAR, "Bro what the fuck you're seriously believing that?")
    
    show teacher_1 flipped:
        leftcenterstage
        pause 1.7
        linear 3 off_farright
    
    $setWait(19.27,21.564)
    $speak(TEACHER_1, "I don't wanna hear it, come with me!")
    
    show kylar:
        rightcenterstage
        linear 3.75 off_farright
    
    $setWait(21.564,26.444)
    $speak(KYLAR, "You're such a fucking bitch dude like not cool!")
    
    show nicole flipped:
        leftstage
        linear 2 off_left
    $setWait(26.444,28.071)
    $speak(NICOLE, "Oh lunchtime.")
    jump scene_0018
label scene_0013:

    $setVoiceTrack("audio/Scenes/0013.mp3")
    
    show nicole:
        leftstage
        
    show teacher_1 flipped:
        leftcenterstage
        
    show kylar:
        rightcenterstage

    $setWait(0.203,2.58)

    $speak(NICOLE, "In trouble? Fuck you I'm not in anything!")
    $setWait(2.58,5.583)

    $speak(TEACHER_1, "Uh yeah you definitely are in trouble.")
    $setWait(5.583,8.419)
    $speak(NICOLE, "Well you're in the model train fan club you freak.")
    $setWait(8.419,12.34)
    $speak(TEACHER_1, "I'm not in the model train fan club I just sponsor the model train fan club.")
    $setWait(12.34,13.967)
    $speak(NICOLE, "That's even worse.")
    $setWait(13.967,19.514)
    $speak(TEACHER_1, "You look new here. I'm not sure what you think you're doing but I can assure you it won't last long.")
    $setWait(19.514,22.976)
    $speak(NICOLE, "A bitch can't pop Percs here, what the fuck? What if I had glaucoma?")
    $setWait(22.976,29.565)
    $speak(TEACHER_1, "But you don't have glaucoma... and you just confessed to drug use on school grounds. Come with me, both of you.")
    
    stop ambient fadeout 1
    jump scene_0019
label scene_0014:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $setVoiceTrack("audio/Scenes/0014.mp3")

    scene cafeteria int
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1
    
    
    
    show nicole:
        off_left
        linear 2.6 leftcenterstage
        
    show jecka:
        rightcenterstage
    
    $setWait(2.501,5.463)

    $speak(JECKA, "Oh you look new, the lunch line's on the other end there.")
    $setWait(5.463,6.339)

    $speak(NICOLE, "Huh?")
    $setWait(6.339,12.219)
    $speak(JECKA, "You're trying to find where the lunch line starts, right? You got here a little late so it's pretty long now.")
    $setWait(12.219,15.64)
    $speak(NICOLE, "Oh! Fuck for a sec I thought everyone else was skipping too.")
    $setWait(15.64,17.266)
    $speak(JECKA, "Where'd you come in from?")
    $setWait(17.266,21.103)
    $speak(NICOLE, "Like just outside. There was this weird kid getting his shit handed to him.")
    $setWait(21.103,22.647)
    $speak(JECKA, "Like weird how?")
    $setWait(22.647,23.856)
    $speak(NICOLE, "I don't fuckin' know.")
    $setWait(23.856,30.655)
    $speak(JECKA, "Is he like \"talks about a bunch of dumb shit\" weird? Or like \"how can he afford so much adderall with a job at the Shop 'n Save\" weird?")
    $setWait(30.655,32.615)
    $speak(NICOLE, "Um... first one.")
    $setWait(32.615,42.124)
    $speak(JECKA, "Oh, glasses, bowl cut, that's Jeffery. I don't think he's all there. Like he's too socially awkward for the normal people but too smart for the special eddies.")
    $setWait(42.124,43.125)
    $speak(NICOLE, "Can I sit here?")
    $setWait(43.125,46.671)
    $speak(JECKA, "Yeah sure, all my friends got put in a different lunch period.")
    $setWait(46.671,48.506)
    $speak(NICOLE, "What's your name? I'm Nicole.")
    $setWait(48.506,49.757)
    $speak(JECKA, "I'm Jecka.")
    $setWait(49.757,52.718)
    $speak(NICOLE, "Jecka? That's like on your birth certificate?")
    $setWait(52.718,54.428)
    $speak(JECKA, "Short for Jessica, obvi.")
    $setWait(54.428,57.974)
    $speak(NICOLE, "That's pretty punk for someone who dresses so...")
    $setWait(57.974,65.439)
    $speak(JECKA, "Preppy? Yeah my Mom works corporate for department stores so I get all this expensive stuff for free but trust me, I don't give a fuck.")
    $setWait(65.439,67.024)
    $speak(NICOLE, "Cool yeah same.")
    
    stop ambient fadeout 1
    
    jump END_OF_DEMO
label scene_0015:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $setVoiceTrack("audio/Scenes/0015.mp3")
    scene cafeteria int
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show nicole:
        leftstage
    
    $setWait(0.67,4.174)

    $speak(NICOLE, "God the food here is tragic. Even the air has preservatives.")
    
    show jecka:
        off_right
        linear 1.6 rightcenterstage
    $setWait(4.174,6.509)

    $speak(JECKA, "Fucking tell me about it, that's why I pack.")
    
    
    $setWait(6.509,8.136)
    $speak(NICOLE, "Oh sorry, didn't see you.")
    $setWait(8.136,12.015)
    $speak(JECKA, "Nah it's okay you can sit here. I'm Jecka, where you in from?")
    
    show nicole:
        leftstage
        linear 1 leftcenterstage
    
    $setWait(12.015,16.227)
    $speak(NICOLE, "Uh Chemistry? I think, I don't know I didn't really do anything.")
    $setWait(16.227,20.315)
    $speak(JECKA, "Aw that sucks yeah you have to like wash acid off you before you can touch your food.")
    $setWait(20.315,27.572)
    $speak(NICOLE, "I'm not eating anyway. The guy I had to sit next to scared my appetite away... pretty much just me away in general.")
    $setWait(27.572,29.657)
    $speak(JECKA, "Who was it? Do you know?")
    $setWait(29.657,31.242)
    $speak(NICOLE, "Um, Jeffery?")
    $setWait(31.242,33.411)
    $speak(JECKA, "Ohhh yep, he's a fun one.")
    $setWait(33.411,36.372)
    $speak(NICOLE, "But he's so like overly chummy, that's fun to you?")
    $setWait(36.372,45.757)
    $speak(JECKA, "No like fun to fuck with him, duh. Freshman year every girl put love notes on his locker, right? So he went up to some of the girls' boyfriends like \"ha she's in love with me now\"")
    $setWait(45.757,47.759)
    $speak(NICOLE, "Oh my god, that's funny.")
    $setWait(47.759,54.39)
    $speak(JECKA, "But cause they were all like 14, three guys just beat the shit out of him for it. Now we have all these stupid anti-bullying rules.")
    $setWait(54.39,56.893)
    $speak(NICOLE, "I never got how they could like enforce that?")
    $setWait(56.893,61.189)
    $speak(JECKA, "It's baby simple, if you don't wanna get bullied just be hot and sociable.")
    $setWait(61.189,64.776)
    $speak(NICOLE, "Fucking accurate... I'm Nicole by the way.")
    $setWait(64.776,67.445)
    $speak(JECKA, "Well I'll see you around, Nicole.")
    
    stop ambient fadeout 1
    
    jump END_OF_DEMO
label scene_0016:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $setVoiceTrack("audio/Scenes/0016.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1
    
    show nicole:
        leftcenterstage
        
    show jeffery:
        rightcenterstage
   
    $setWait(0.498,4.043)

    $speak(NICOLE, "You did such a good job, I'm almost jealous actually.")
    $setWait(4.043,7.755)

    $speak(JEFFERY, "Aw there's nothing to it, I could tutor you after school or something.")
    $setWait(7.755,11.759)
    $speak(NICOLE, "Mmm we'll worry about that later, so what were you gonna tell me in class?")
    $setWait(11.759,15.262)
    $speak(JEFFERY, "Oh about how nail polish remover can melt styrofoam.")
    $setWait(15.262,19.266)
    $speak(NICOLE, "No before that... the girls in your favorite animes?")
    $setWait(19.266,28.442)
    $speak(JEFFERY, "Oh yeah um... well I think they're really really cute... but sometimes more than cute?")
    $setWait(28.442,31.612)
    $speak(NICOLE, "Like... like all the way?")
    $setWait(31.612,40.746)
    $speak(JEFFERY, "Um, well a promise is a promise... I think some of them are very sexy.")
    $setWait(40.746,42.54)
    $speak(NICOLE, "Oh, you like 'em that way, huh?")
    $setWait(42.54,47.044)
    $speak(JEFFERY, "Yeah cause their bodies are just so... perfect.")
    $setWait(47.044,50.923)
    $speak(NICOLE, "Uh huh totally. They are drawn so perfect.")
    $setWait(50.923,53.634)
    $speak(JEFFERY, "Y-you don't think that's weird, right?")
    $setWait(53.634,57.972)
    $speak(NICOLE, "No it's perfectly normal... I think, can't really check right now.")
    $setWait(57.972,68.733)
    $speak(JEFFERY, "Thanks. And sometimes when I'm... pent up I... pause the anime at certain frames and I... y'know?")
    $setWait(68.733,71.318)
    $speak(NICOLE, "No I don't know, tell me.")
    $setWait(71.318,77.408)
    $speak(JEFFERY, "I kinda like.. y'know, use my hand.")
    $setWait(77.408,81.412)
    $speak(NICOLE, "Oh.. like to completion?")
    $setWait(81.412,82.747)
    $speak(JEFFERY, "Yeah...")
    $setWait(82.747,85.75)
    $speak(NICOLE, "I think that's awesome, it's so great that you do that.")
    $setWait(85.75,94.008)
    $speak(JEFFERY, "Oh thanks... you're the first girl I ever told that to. I like you, Nicole. Can we talk tomorrow?")
    $setWait(94.008,97.428)
    $speak(NICOLE, "...Yeah, fuck it. Hey tonight, tell those girls I said hi.")
    $setWait(97.428,100.0)
    $speak(JEFFERY, "Okay, anything for you, Nicole.")
    stop ambient fadeout 1
    
    jump END_OF_DEMO
label scene_0017:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0
        

    $setVoiceTrack("audio/Scenes/0017.mp3")
    scene cafeteria int
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1
    
    show jecka flipped:
        rightstage
        
    show nicole:
        off_left
        linear 1.5 leftcenterstage
    
    $setWait(0.496,3.499)

    $speak(NICOLE, "God damn this school's nothing but rapists and pedophiles.")
    
    show jecka:
        rightstage
        linear 0.6 rightcenterstage
    
    $setWait(3.499,4.834)

    $speak(JECKA, "Tell me about it.")
    $setWait(4.834,7.753)
    $speak(NICOLE, "Oh sorry, if you're sitting here I can go somewhere else.")
    $setWait(7.753,10.256)
    $speak(JECKA, "Nah I don't think anyone's showing up, go ahead.")
    $setWait(10.256,12.174)
    $speak(NICOLE, "Thanks. What's your name?")
    $setWait(12.174,22.059)
    $speak(JECKA, "Jecka. Now before I ask your name, I just wanna ask what happened to you. Like it took me 2 years to figure out this school sucks, you did it on your first day, what's up?")
    $setWait(22.059,24.228)
    $speak(NICOLE, "...A lacrosse player wanted me to get high.")
    $setWait(24.228,27.189)
    $speak(JECKA, "Like Benadryl or a prescription high?")
    $setWait(27.189,28.774)
    $speak(NICOLE, "Full on Percocet, dude.")
    $setWait(28.774,35.114)
    $speak(JECKA, "Oh that's um... fuck what was his name? Kylar yeah! Yeah he's a bit of a benzosexual.")
    $setWait(35.114,37.408)
    $speak(NICOLE, "What the fuck's a benzosexual?")
    $setWait(37.408,39.827)
    $speak(JECKA, "Attracted to the unconscious.")
    $setWait(39.827,43.164)
    $speak(NICOLE, "Oh... well hi I'm Nicole I just dodged a bullet.")
    $setWait(43.164,49.336)
    $speak(JECKA, "Cool hey. Um, so the other guys you gotta watch out for are usually into some form of feet.")
    
    stop ambient fadeout 1
    jump END_OF_DEMO
label scene_0018:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $setVoiceTrack("audio/Scenes/0018.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show jecka:
        rightstage
        
    show nicole:
        off_left
        linear 3.2 leftcenterstage
    
    $setWait(0.702,3.789)

    $speak(NICOLE, "That was the ultimate win-win...")
    
    show jecka:
        rightstage
        linear 0.65 rightcenterstage
    $setWait(3.789,6.375)

    $speak(JECKA, "Hey uh, are you okay?")
    
    show nicole:
        leftcenterstage
    
    $setWait(6.375,12.672)
    $speak(NICOLE, "What? --Oh no I'm good as shit, dude. I don't feel great, just nice.")
    $setWait(12.672,15.967)
    $speak(JECKA, "So is anyone else gonna be sitting here or?")
    $setWait(15.967,19.721)
    $speak(NICOLE, "Oh sit here all you want, I'm new here I have no say.")
    $setWait(19.721,24.643)
    $speak(JECKA, "Cool thanks... Um, I'm just gonna say it, are you fucked up?")
    $setWait(24.643,25.727)
    $speak(NICOLE, "Are you?")
    $setWait(25.727,27.938)
    $speak(JECKA, "Emotionally, absolutely.")
    $setWait(27.938,31.525)
    $speak(NICOLE, "I'm not rich enough to turn down free Percocet.")
    $setWait(31.525,36.196)
    $speak(JECKA, "Yeah that lacrosse guy loves the new girls. Did you pocket any, can I have one?")
    $setWait(36.196,40.409)
    $speak(NICOLE, "No it got broken up real quick, a teacher caught us and I just pinned it on him.")
    $setWait(40.409,43.078)
    $speak(JECKA, "That's fucking bad ass, what's your name?")
    $setWait(43.078,47.707)
    $speak(NICOLE, "I'm Nicole, but don't say that really loud I don't want these people to know me.")
    $setWait(47.707,51.878)
    $speak(JECKA, "Don't worry, I know... So what electives are you taking?")
    $setWait(51.878,56.133)
    $speak(NICOLE, "Like uh.. is English an elective?")
    $setWait(56.133,58.218)
    $speak(JECKA, "It should be, but no.")
    $setWait(58.218,60.512)
    $speak(NICOLE, "Okay then it was photography.")
    $setWait(60.512,63.807)
    $speak(JECKA, "Me too, We might be in the same class!")
    $setWait(63.807,67.519)
    $speak(NICOLE, "If you'd.. like to get that excited about it-- yeah we might be.")
    $setWait(67.519,69.187)
    $speak(JECKA, "Oh you're too cool for school?")
    $setWait(69.187,75.152)
    $speak(NICOLE, "Well no, right now I feel warm as hell, have you popped perc? It's a blanket in a pill.")
    $setWait(75.152,78.155)
    $speak(JECKA, "Yeah I've popped perc, how the fuck is it a blanket in a pill?")
    $setWait(78.155,82.367)
    $speak(NICOLE, "It turns off all the coldness sensors, you just feel nice and cozy.")
    $setWait(82.367,83.91)
    $speak(JECKA, "You're fun.")
    
    stop ambient fadeout 1
    jump END_OF_DEMO
label scene_0019:
    $setVoiceTrack("audio/Scenes/0019.mp3") 
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene
    show black
    show home nicole ext night with Pause(2.038):
        truecenter zoom 0.5
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.038 truecenter zoom .6
    

    
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"    
  
    show nicole shirt:
        leftcenterstage
        
    show mom:
        rightstage
        linear 4.2 rightcenterstage


    $setWait(2.038,7.794)
    $speak(MOM, "Honey... what the fuck is wrong with you? A 2-day suspension on the first day of school?")
    $setWait(7.794,12.381)
    $speak(NICOLE, "It was like one pill, he's just mad I made him feel insecure so he threw the book at me!")
    $setWait(12.381,15.092)
    $speak(MOM, "Look I know you're acting out because of your father--")
    $setWait(15.092,24.602)
    $speak(NICOLE, "Mom, literally no one ever has actively thought \"I'm gonna act out today!\" What does that even mean? \"I'm gonna look cool by disrespecting my parents!\" this is a world you and everyone who crochets created.")
    show gamer_brother:
        off_right
        linear 2.0 rightstage
    
    $setWait(24.602,26.521)
    $speak(GAMER_BROTHER, "She kinda has a point with that, Mom.")
    
    show mom flipped:
        rightcenterstage
    $setWait(26.521,29.19)
    $speak(MOM, "You kinda need to get a fucking job, you're 26.")
    $setWait(29.19,35.822)
    $speak(GAMER_BROTHER, "I told you the economy's bad, blame Bush! And these girls I chat with online fully agree!")
    $setWait(35.822,41.953)
    $speak(NICOLE, "Mom, still, I can't believe you're taking the school's side with this. It's totally against all my citizen rights!")
    show mom:
        rightcenterstage
    $setWait(41.953,46.999)
    $speak(MOM, "They had you sign something that waives those rights-- you're 16 you don't even have rights.")
    $setWait(46.999,50.086)
    $speak(NICOLE, "Well you do, right? Sue the school or something!")
    $setWait(50.086,59.47)
    $speak(MOM, "You're at the only public school for miles and miles. What happens if you're gone for good, huh? I'm not moving again, I'm not paying for private school, and I'm definitely not homeschooling.")
    
    show gamer_brother flipped:
        rightstage
        linear 3.6 off_farright
    
    $setWait(59.47,66.811)
    $speak(NICOLE, "Fine I won't blow it then, I won't squeal a bit. A teacher could just rape the shit out of me but I won't say a word cause we gotta stay in this shit hole!")
    $setWait(66.811,69.146)
    $speak(MOM, "Good, I'm glad we understand each other.")
    $setWait(69.146,71.899)
    $speak(NICOLE, "Mom! I could just get assaulted, you wouldn't care?")
    $setWait(71.899,76.32)
    $speak(MOM, "You've been pulling the sexual assault card since you were 12, hasn't happened yet, has it?")
    $setWait(76.32,78.155)
    $speak(NICOLE, "That's not the fucking point!")
    $setWait(78.155,82.66)
    $speak(MOM, "Well you can figure out a new excuse locked in your bedroom for the next 2 days.")
    
    show nicole shirt flipped:
        leftcenterstage
        linear 3.5 off_left
    $setWait(82.66,86.497)
    $speak(NICOLE, "Fine! I have my own computer, grounding doesn't do shit anymore.")
    
    stop ambient fadeout 1
    jump scene_0020
label scene_0020:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $setVoiceTrack("audio/Scenes/0020.mp3")
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 1
    
    show gamer_brother flipped:
        rightcenterstage

    $setWait(1.095,6.976)

    $speak(GAMER_BROTHER, "Yeah baby you hear this!? This is some real music! Now join my party chat and we can game!")
    
    show nicole tanktop:
        off_left
        linear 3 leftcenterstage
        
    show gamer_brother:
        rightcenterstage
        
    $setWait(6.976,10.647)
    $speak(NICOLE, "What the fuck are you doing? It's 1am I go back to school tomorrow!")
    $setWait(10.647,13.816)
    $speak(GAMER_BROTHER, "Bro you're being seriously fail right now.")
    $setWait(13.816,17.779)
    $speak(NICOLE, "\"Seriously fail\".. those words don't even go together you sound like an idiot.")
    $setWait(17.779,23.409)
    $speak(GAMER_BROTHER, "Look I'm just recording a little voice message for this hottie I met online then I'm done okay?")
    $setWait(23.409,27.914)
    $speak(NICOLE, "This is like the 5th \"hottie\" in 2 days. Do you know how old any of these girls are?")
    $setWait(27.914,31.125)
    $speak(GAMER_BROTHER, "Like, legal in her country don't worry about it.")
    
    show nicole tanktop flipped:
        leftcenterstage
        
    $setWait(31.125,32.877)
    $speak(NICOLE, "Oh my god, this is bad.")
    $setWait(32.877,37.423)
    $speak(GAMER_BROTHER, "I'm just trying to score some 15-year old Canadian ass, hop off it.")
    
    show nicole tanktop:
        leftcenterstage
    $setWait(37.423,41.761)
    $speak(NICOLE, "15 isn't legal anywhere, calling her Canadian ass doesn't make that better.")
    $setWait(41.761,49.852)
    $speak(GAMER_BROTHER, "Well no, y'know how like Canadian bacon is just ham? Canadian ass is just a mature 15 year old. See? Same thing.")
    
    
    $setWait(49.852,52.105)
    $speak(NICOLE, "You're.. Oh my god..")
    $setWait(52.105,55.984)
    $speak(GAMER_BROTHER, "Could you just help me record this message so we can both go to bed quicker?")

menu:
        "DISTRACT HIM INTO DOING SOMETHING ELSE":
            jump scene_0021
        "MAKE HIM GONE FOR GOOD":
            jump scene_0022
label scene_0021:

    $setVoiceTrack("audio/Scenes/0021.mp3")
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    
    show nicole tanktop:
        leftcenterstage
        
    show gamer_brother:
        rightcenterstage
    
    $setWait(0.339,6.846)

    $speak(NICOLE, "Hey um.. did you get that new shooter game? The one where you're a white guy shooting brown people in a non-racist way?")
    $setWait(6.846,13.227)

    $speak(GAMER_BROTHER, "Oh Warfare? Yeah hell yeah I got it. Had to steal out of Mom's purse but it's get paid or get played, y'know what I mean?")
    $setWait(13.227,17.106)
    $speak(NICOLE, "Uh yeah I guess. Can I play with you?")
    $setWait(17.106,19.776)
    $speak(GAMER_BROTHER, "I thought you didn't like video games anymore.")
    $setWait(19.776,22.987)
    $speak(NICOLE, "I started using an anti-aging cream so my hobbies should match my skin.")
    
    show gamer_brother flipped:
        rightcenterstage
        linear 6.6 off_farright
    
    $setWait(22.987,26.324)
    $speak(GAMER_BROTHER, "Works for me, but you're player 2, bitch.")
    
    show nicole tanktop: 
        leftcenterstage
        linear 6 off_right
    
    $setWait(26.324,29.076)
    $speak(NICOLE, "How could any adult woman not like video games?")
    
    stop ambient fadeout 1
    jump END_OF_DEMO

label scene_0022:

    $setVoiceTrack("audio/Scenes/0022.mp3")
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    
    show nicole tanktop:
        leftcenterstage
        
    show gamer_brother:
        rightcenterstage
    
    $setWait(0.213,4.717)
    $speak(NICOLE, "What's the point? Whatever girl you're hitting up's probably ugly compared to what I could find.")
    
    $setWait(4.717,7.678)
    $speak(GAMER_BROTHER, "You haven't even seen her avatar she's like so hot.")
    
    $setWait(7.678,10.64)
    $speak(NICOLE, "Where are you logged in at? I bet I could find a better one.")
    
    show black onlayer screens:
        alpha 0.0
        linear 1.5 alpha 1.0
        1.7
        linear 0.88 alpha 0.0
        
    stop ambient fadeout 1.6
    
    $setWait(10.64,13.684)
    $speak(GAMER_BROTHER, "You're on.")
    
    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 1
    
    $setWait(13.684,22.818)
    $speak(NICOLE, "See? This girl right here. KinkyKenzie93, her bio's like \"only interested in older guys so hit me up whenever, up for anything\".")
    
    show black onlayer screens:
        alpha 0.0
    
    $setWait(22.818,24.487)
    $speak(GAMER_BROTHER, "Man she's sexy.")
    
    $setWait(24.487,25.821)
    $speak(NICOLE, "She's also 14.")
    
    $setWait(25.821,32.495)
    $speak(GAMER_BROTHER, "Shut up with that ageist, bullshit. Oh man she's just a town over too, I'm gonna message her what should I say?")
    
    $setWait(32.495,35.289)
    $speak(NICOLE, "You're like a legal adult, shouldn't you know how to do this by now?")
    
    $setWait(35.289,39.335)
    $speak(GAMER_BROTHER, "Yeah but you're a girl, you know what girls wanna hear, come on.")
    
    $setWait(39.335,46.759)
    $speak(NICOLE, "Alright fine. Um, first tell her you're 26. Girls who like older men are all about that age difference.")
    
    $setWait(46.759,48.052)
    $speak(GAMER_BROTHER, "Okay, what else?")
    
    $setWait(48.052,52.556)
    $speak(NICOLE, "Say you wanna buy her drugs and alcohol, and no pussy shit. Like full on heroin.")
    
    $setWait(52.556,58.771)
    $speak(GAMER_BROTHER, "I'm sure other guys promised that too though, right? When guys hit you up, what do they never do?")
    
    $setWait(58.771,64.527)
    $speak(NICOLE, "Hmm.. Oh! At the bottom, type an acrostic poem using your driver's license number.")
    
    $setWait(64.527,65.903)
    $speak(GAMER_BROTHER, "I don't know...")
    
    $setWait(65.903,70.032)
    $speak(NICOLE, "But like, have the message of the poem be about how you don't wanna use a condom.")
    
    show black onlayer screens:
        alpha 0.0
        3.2
        linear 1.5 alpha 1.0
        7.4
        linear 0.15 alpha 0.0
        
    stop ambient fadeout 6.5
    
    $setWait(70.032,82.044)
    $speak(GAMER_BROTHER, "Dude! ...That's like genius! She's gonna so want the D.") 
    
    show nicole tanktop:
        off_left
        
    show gamer_brother flipped:
        off_left
        linear 0.3 leftcenterstage
        
    show cop:
        off_right
        linear 0.6 rightstage
        
    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 0.3
    
    $setWait(82.044,84.046)
    $speak(GAMER_BROTHER, "Whoa what do you want!?")
    
    show black onlayer screens:
        alpha 0.0
    
    
    $setWait(84.046,86.882)    
    $speak(COP, "Are you dating site user \"Heavy D no MC\"?")
    
    $setWait(86.882,92.847)
    $speak(GAMER_BROTHER, "Yeah but I don't know what that has to do with you busting in here! By the way that's like a sick user name, right--")
    
    show cop:
        rightstage
        linear 0.2 rightcenterstage
        
    show gamer_brother flipped:
        leftcenterstage
        pause 1
        linear 0.6 leftstage
    
    $setWait(92.847,96.6)
    $speak(COP, "You're under arrest for digital misconduct with a minor!")
    
    show cop:
        rightcenterstage
        
    show gamer_brother flipped:
        leftstage
        linear 0.8 leftcenterstage

    $setWait(96.6,99.812)    
    $speak(GAMER_BROTHER, "Aw that Kenzie bitch snitched me out, god dammit!")
    
    show cop:
        rightcenterstage
        pause 6.1
        linear 0.1 xalign 0.5
        
    show gamer_brother flipped:
        leftcenterstage
    
    $setWait(99.812,106.527)
    $speak(COP, "Rest assured, there was no Kenzie. We can talk all about how you fell for a sting operation downtown!")
    
    show gamer_brother:
        leftcenterstage
        linear 7 off_farright
        
        
    show cop:
        xalign 0.5
        linear 6 off_farright
    
    $setWait(106.527,114.869)
    $speak(GAMER_BROTHER, "I was set up! Fuckin' Nicole you bitch, my first phone call's gonna be a bomb threat to your friends!")
    stop ambient fadeout 1
    jump END_OF_DEMO

label END_OF_DEMO:
    window hide

    show black onlayer overlay with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer overlay:
        alpha 1.0
        linear 1 alpha 0.0

    show demo end

    $renpy.pause(20.0)