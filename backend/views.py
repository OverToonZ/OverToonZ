from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.db.models import F,Q
from django.http import HttpResponse
from backend.context_processors import user_details
import json,pytz


def err_msg(msg1=" ",msg2=" "):
   
    Content = {
                        "err_msg1" : msg1,
                        "err_msg2" : msg2
                    }
    return Content

def isemptydata(data):
    for key, value in data.items():
        if value == [None] or value == ['']:
            return False
    return True

def getuser(user):
    userdata = User.objects.filter(email = user).values()
    userinfo = {}
    for info in userdata:
        userinfo['username'] = info['username']
        userinfo['email'] = info['email']
        userinfo['favourite_anime'] = info['favourite_anime']
        userinfo['date_joined'] = info['date_joined']
        userinfo['last_login'] = info['last_login']
        userinfo['login_count'] = info['login_count']
        userinfo['superuser'] = info['is_superuser']
    return userinfo

def index(request):
    return render(request, 'index.html')

def accountsetup(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
                if request.POST.get('purpose') == 'accountsetup':
                    editinfo = json.loads(request.POST.get('editinfo'))
                    OrgUser = User.objects.filter(Q(email = request.user) & Q(username = user_details(request)['userinfo']['username']) )
                    for user in OrgUser:
                        if editinfo.get('pass') != "********":
                            user.set_password(editinfo.get("pass"))
                        user.username = editinfo.get("username")
                        user.email = editinfo.get("email")
                        user.favourite_anime = editinfo.get("favourite")
                        user.save()

                elif request.POST.get('purpose') == 'passcodesetup':
                    codeinfo = json.loads(request.POST.get('codeinfo'))
                    user = authenticate(request, email=request.user, password=codeinfo.get("oldpasscode"))
                    if user is not None:
                        if codeinfo.get("passcode") == codeinfo.get("confirm_passcode") and codeinfo.get("passcode") != " " and codeinfo.get("passcode") != None and len(codeinfo.get("passcode")) > 7 :
                            OrgUser = User.objects.filter(Q(email = request.user) & Q(username = user_details(request)['userinfo']['username']) )
                            for user in OrgUser:
                                if codeinfo.get("passcode"):
                                    user.set_password(codeinfo.get("passcode"))
                                    user.save()
                    else:
                        return HttpResponse(status=400)
                    
                elif request.POST.get('purpose') == 'deletesetup':
                    delinfo = json.loads(request.POST.get('delinfo'))
                    user = authenticate(request, email=delinfo.get("email"), password=delinfo.get("passcode"))
                    if user is not None:
                        if request.user:
                            deluser = request.user
                            deluser.delete()
                            logout(request)
                            return HttpResponse(status=204)
                        else:
                            return HttpResponse(status=400)
                        
                    else:
                        return HttpResponse(status=400)

                else:
                    return HttpResponse(status=400)
                    
                return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)

def signup(request):
    

    if request.method == 'POST':
        user_check = User.objects.filter(username=request.POST.get('username'))
        email_check = User.objects.filter(email=request.POST.get('email'))

        if len(user_check)>0 and len(email_check)>0:
            return render(request, 'signup.html',err_msg(msg1=" * Username already exists",msg2=" * Email already exists"))
        elif len(user_check)>0:
            return render(request, 'signup.html',err_msg(msg1=" * Username already exists"))
        elif len(email_check)>0 :
            return render(request, 'signup.html',err_msg(msg2=" * Email already exists"))
        else:
            CTime = str(datetime.now()).split('.')[0]
            new_user = User( username = request.POST.get('username'),email = request.POST.get('email'),favourite_anime = request.POST.get('fanime'),last_login = CTime )
            new_user.set_password(request.POST.get('password'))
            new_user.save()
            return redirect('loginUser')
    return render(request, 'signup.html')

def write_json(file_path,data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    

def open_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def update_and_sort(data):
    deldata = {}
    timezone = pytz.timezone("Asia/Kolkata")  # or another timezone
    threshold_time = timezone.localize(datetime.now() - timedelta(days=60))
    for timestamp, details in data.items():
        entry_time = datetime.fromisoformat(timestamp)
        # If entry_time is timezone-naive, make it aware
        if entry_time.tzinfo is None:
            entry_time = timezone.localize(entry_time)
        # Only keep entries newer than the threshold time
        if entry_time > threshold_time:
            deldata[timestamp] = details
    # Sort the data by timestamp in descending order
    sorted_data = dict(sorted(deldata.items(), key=lambda item: item[0], reverse=True))
    return sorted_data

def home(request):
    
    data = open_json("./static/json/home.json")
    data = update_and_sort(data)
    write_json("./static/json/home.json",data)
    
    top_anime = AnimeInfo.objects.order_by('-rating')[:15]
    Top_picks.objects.all().delete()
    for rank, anime in enumerate(top_anime, start=1):
        Top_picks.objects.create(anime = anime, place=rank)
    Toppicks = Top_picks.objects.all()

    content={"data": data, "toppicks":Toppicks}
    return render(request, 'home.html',content)

def loginUser(request):
    sessionData = Session.objects.filter(session_key =request.session.session_key)
    sessionData.delete()
   
    if request.method == 'POST':

        users = authenticate(email = request.POST.get('email'), password = request.POST.get('password'))
        if users is not None:
            login(request,users)
            user = User.objects.get(email=request.POST.get('email'))
            count = user.login_count 
            user.login_count= count + 1
            user.save()
            return redirect('home')
        else:
             return render(request, 'login.html',err_msg("* Email or Password are invalid, Please try again."))

    return render(request, 'login.html',err_msg(" "))

def logoutUser(request):
    if request.user:
        ist = pytz.timezone('Asia/Kolkata')
        user = User.objects.get(email=request.user)
        user.last_login = timezone.now().astimezone(ist)
        user.save()
      
    logout(request)
    return render(request, 'login.html',err_msg())

def get_anime_list(animes):
    animegroup = {}
    for anime in animes:
        first_letter = anime.title[0].upper()
        if first_letter not in animegroup:
            animegroup[first_letter] = []
        animegroup[first_letter].append(anime)
    # print(animegroup)
    List = {
        "animes":animegroup
    }
    return List

def anime(request):
  
    
    animes = AnimeInfo.objects.all().order_by("title")
    if request.method == "POST":
        search = request.POST.get("search")
        if search == "":
            animes = AnimeInfo.objects.all().order_by("title")
        else:
            query = search.lower().split(" ")
            for i in range(len(query)): 
               query[i] = query[i].capitalize()
            search = " ".join(query)
            animes = AnimeInfo.objects.filter(title=search).order_by("title")
            return render(request, 'anime.html',get_anime_list(animes))


    else:
        animes = AnimeInfo.objects.all().order_by("title")
    
    
    return render(request, 'anime.html',get_anime_list(animes))

def seasons(request,title):
    Anime = AnimeInfo.objects.filter(title = title.replace('-',' ')).first()
    data = SeasonInfo.objects.filter(anime_id = Anime.id )
    if len(data) <= 0:
        season = False
    else:
        season = True
        
    content={"is_season":season,
             "Season":data,
             "title":title.replace('-',' '),
             "AnimeData":Anime
             }
  
    return render(request, 'season.html',content)

def episodes(request,title,seasons):
    AnimeId = AnimeInfo.objects.get(title = title.replace('-',' ')).id
    Seasondata = SeasonInfo.objects.filter(anime_id = AnimeId , season_count = seasons )
    data = EpisodesInfo.objects.filter(anime_id = AnimeId , season_id = Seasondata.first().id )
    
    TotalEpisode = len(data)
    if TotalEpisode <= 0:
        episode = False
    else:
        episode = True
    content = {
        "is_episodes":episode,
        "title":title,
        "season":seasons,
        "banner": Seasondata.first().season_banner,
        "episodes_list":data,
        
    }

    if request.method == 'POST':
        info = request.POST.get('info')
        AnimeID = AnimeInfo.objects.get(title = title.replace('-',' ')).id
        if info == "EpisodeViews":
            Codes = request.POST.get('Id_Code')
            Code = Codes.split("_")
            Code[0] = Code[0].replace('-'," ")
            
            EpisodesInfo.objects.filter(anime_id = AnimeID, code = Code[1]).update(views = F('views')+1 )
            epidata = EpisodesInfo.objects.filter(anime_id = AnimeID, code = Code[1]).values()[0]
            data = {
            "EpisodeNo" : epidata.get("episode"),
            "EpisodeName" : epidata.get("episode_title"),
            "Views" : epidata.get("views")
            }
            return JsonResponse({'EpisodeData': data,})
        
        elif info == "NextEpisode":
            Codes = request.POST.get('CurrentVideo')
           
            Code = Codes.split("_")
            reuseTitle = Code[0]
            Code[0] = Code[0].replace('-'," ")
            Code[1] = Code[1][:-2] + f"{(int(Code[1][-2:]) + 1):02}"
            
            exist = EpisodesInfo.objects.filter(anime_id = AnimeID, code = Code[1]).exists()
            if exist:
                err = False
            else:
                Code[1] = Code[1][:-2] + f"{(int(1)):02}"
                err = True
            EpisodesInfo.objects.filter(anime_id = AnimeID, code = Code[1]).update(views = F('views')+1 )
            epidata = EpisodesInfo.objects.filter(anime_id = AnimeID, code = Code[1]).values()[0]
            newCur = reuseTitle + "_" + Code[1]
            
            data = {
            "EpisodeNo" : epidata.get("episode"),
            "EpisodeName" : epidata.get("episode_title"),
            "Views" : epidata.get("views"),
            "src":epidata.get("episode_link"),
            "curData":newCur,
            "err":err
            }
            return JsonResponse({'NextData': data,})
        
        elif info == "PrevEpisode":
            Codes = request.POST.get('CurVideo')
            
            Code = Codes.split("_")
            reuseTitle = Code[0]
            Code[0] = Code[0].replace('-'," ")
            if Code[1] == "S01EP00" or Code[1] == "S01EP01":
                err = True
                Code[1] = Code[1][:-2] + f"{(int(TotalEpisode)):02}"
                

            else:
                err = False
                Code[1] = Code[1][:-2] + f"{(int(Code[1][-2:]) - 1):02}"
            EpisodesInfo.objects.filter(anime_id =AnimeID, code = Code[1]).update(views = F('views')+1 )
            epidata = EpisodesInfo.objects.filter(anime_id = AnimeID, code = Code[1]).values()[0]
            newCur = reuseTitle + "_" + Code[1]
           
            data = {
            "EpisodeNo" : epidata.get("episode"),
            "EpisodeName" : epidata.get("episode_title"),
            "Views" : epidata.get("views"),
            "src":epidata.get("episode_link"),
            "curData":newCur,
            "err":err
            }
            return JsonResponse({'PrevData': data,})
    

    
    return render(request, 'episodes.html',content)

def operations(request):

    if request.user.is_superuser:

        if request.method == 'POST':
            homejson = open_json("./static/json/home.json")
            if "AddAnime" in request.POST:
                GenreList = request.POST.get('genre').split(',')
                new_anime = AnimeInfo(
                    title=request.POST.get('title'),
                    img_src=request.POST.get('img_url'),
                    banner=request.POST.get('img_banner'),
                    studio = request.POST.get('studio'),
                    seasons = request.POST.get('seasons'),
                    episodes = request.POST.get('episodes'),
                    avail_lang = request.POST.get('avail_lang'),
                    rating =  request.POST.get('rating'),
                    status = request.POST.get('status'),
                    description =  request.POST.get('description'),
                    genre = GenreList
                )
                new_anime.save()
                new_data = {
                        timezone.now().isoformat(): {
                            "Name": request.POST.get('title'),
                            "Type": "Anime",
                            "Img": request.POST.get('img_url')
                        }
                     }
                homejson.update(new_data)
                write_json("./static/json/home.json",homejson)

            elif "AddSeason" in request.POST:
                Anime = AnimeInfo.objects.get(title = request.POST.get('title'))
                new_season = SeasonInfo(
                    anime_id= Anime.id,
                    season_count=request.POST.get('seasons'),
                    episode_count = request.POST.get('episodes'),
                    season_title = request.POST.get('seasonname'),
                    season_cover = request.POST.get('img_url'),
                    season_banner = request.POST.get('img_ban_url'),
                    
                    status = request.POST.get('status'),
                )
                new_season.save()
                new_data = {
                        timezone.now().isoformat(): {
                            "Name": request.POST.get('title'),
                            "Type": "Season",
                            "Img": request.POST.get('img_url')
                        }
                     }
                homejson.update(new_data)
                write_json("./static/json/home.json",homejson)
                
            elif "AddEpisode" in request.POST:
                code = 'S' + str(request.POST["seasons"].zfill(2)) + 'EP' +str(request.POST["episodes"].zfill(2))
                views = 0
                count = EpisodesInfo.objects.filter(anime_id__title = request.POST.get('title')).count()
                Anime = AnimeInfo.objects.get(title = request.POST.get('title'))
                Season = SeasonInfo.objects.filter( anime_id__title =  request.POST.get('title') ,season_count = request.POST.get('seasons')).first()
                new_episode = EpisodesInfo( anime_id = Anime.id,
                                        season_id = Season.id ,
                                        static_count = count + 1,
                                        episode = request.POST.get('episodes'),
                                        code = code,
                                        episode_title = request.POST.get('episode_title'),
                                        episode_cover = request.POST.get('episode_cover_url'),
                                        views = views,
                                        episode_link = request.POST.get('episode_url'))
                new_episode.save()
                new_data = {
                        timezone.now().isoformat(): {
                            "Name": request.POST.get('title'),
                            "Type": "Episode",
                            "Season": request.POST.get('seasons'),
                            "Img": Season.season_cover
                        }
                     }
                homejson.update(new_data)
                write_json("./static/json/home.json",homejson)

            elif "BulkUpdate" in request.POST:
                if 'jsonfile' in request.FILES:
                    jsonfile = request.FILES['jsonfile']
                    file_data = jsonfile.read().decode('utf-8')
                    json_data = json.loads(file_data)
                    Anime = AnimeInfo.objects.get(title = request.POST.get('anime'))
                    if request.POST.get('BulkFor') =='Episodes':
                        views = 0
                        count = EpisodesInfo.objects.filter(anime_id__title = request.POST.get('anime')).count()
                        for epidata in json_data:
                            code = 'S' + str(epidata.get('season')).zfill(2) + 'EP' +str(epidata.get('episode')).zfill(2)
                            count = count + 1
                            Season = SeasonInfo.objects.filter( anime_id__title =  request.POST.get('anime') ,season_count = epidata.get('season')).first()
                            new_episode = EpisodesInfo(anime_id = Anime.id,
                                                    season_id = Season.id ,
                                                    static_count = count,
                                                    episode = epidata.get('episode'),
                                                    code = code,
                                                    episode_title = epidata.get('episode_title'),
                                                    episode_cover = epidata.get('episode_cover'),
                                                    views = views,
                                                    episode_link = epidata.get('episode_link'))
                            new_episode.save()
                           
                    elif request.POST.get('BulkFor') =='Seasons':
                        for epidata in json_data:
                            new_season = SeasonInfo(
                                            anime_id= Anime,
                                            season_count=epidata.get('season'),
                                            episode_count = epidata.get('totalepisode'),
                                            season_title = epidata.get('season_title'),
                                            season_cover = epidata.get('season_cover'),
                                            season_banner = epidata.get('season_banner'),
                                            status = epidata.get('status'),
                                        )
                            new_season.save()
                    
                        
                   
               
            
            elif "ModifyAnime" in request.POST:
                
                animelist = AnimeInfo.objects.get(title=request.POST.get('title'))
                animelist.title = request.POST.get('title')
                animelist.img_src = request.POST.get('img_url')
                animelist.banner = request.POST.get('img_banner')
                animelist.studio = request.POST.get('studio')
                animelist.seasons = request.POST.get('seasons')
                animelist.episodes = request.POST.get('episodes')
                animelist.avail_lang = request.POST.get('avail_lang')
                animelist.rating = request.POST.get('rating')
                animelist.status = request.POST.get('status')
                animelist.description = request.POST.get('description'),
                animelist.genre = request.POST.get('genre')
                animelist.save()

            elif "ModifySeason" in request.POST:
                SeasonInfo.objects.filter(anime_id__title = request.POST.get('title') , season_count = request.POST.get('seasons') ).update(
                    status = request.POST.get('status'),  
                    episode_count = request.POST.get('episodes'),
                    season_title = request.POST.get('seasonname'),
                    season_cover = request.POST.get('img_url'),
                    season_banner = request.POST.get('img_ban_url')
                )

            elif "ModifyEpisode" in request.POST:
    
                queryCode = request.POST.get('Episode Code').split('-')[1]
                EpisodesInfo.objects.filter(anime_id__title = request.POST.get('title') , code = queryCode ).update(
                anime = request.POST.get('title'),
                season = request.POST.get('seasons'),
                episode = request.POST.get('episodes'),
                episode_title = request.POST.get('episode_title'),
                episode_cover = request.POST.get('episode_cover_url')
                )
            
            elif "RemoveAnime" in request.POST:
                data = AnimeInfo.objects.filter(title = request.POST.get('title'))
                data.delete()

            elif "RemoveSeason" in request.POST:
                data = SeasonInfo.objects.filter(anime_id__title = request.POST.get('title'), season_count = request.POST.get('seasons'))
                data.delete()

            elif "RemoveEpisode" in request.POST:
                data = SeasonInfo.objects.filter(anime_id__title = request.POST.get('title'), season_id__season_count = request.POST.get('seasons'),episode = request.POST.get('episodes'))
                data.delete()

            else:
                
                Mform = request.POST.get('formuse')
                if Mform == "ModifyAnimeInfo":
                    selected_anime = request.POST.get('selected_anime')
                    animedata = AnimeInfo.objects.filter(title=selected_anime).values()
                    for data in animedata:
                        retvalue = {
                            "img_src": data.get('img_src'),
                            "img_banner": data.get('banner'),
                            "studio" : data.get('studio'),
                            "seasons": data.get('seasons'),
                            "episodes" : data.get('episodes'),
                            "avail_lang": data.get('avail_lang'),
                            "rating" : data.get('rating'),
                            "status": data.get('status'),
                            "MS_desp": data.get('description'),
                            "genre" : data.get('genre')
                        }
                        break
                    return JsonResponse({'updated_value': retvalue})
                
                elif Mform == "ModifyEpisodeInfo":
                    Coden = request.POST.get('Selected_Code').split("-")
                    animeName = Coden[0]
                    codes = Coden[1]
                    epidata = EpisodesInfo.objects.get(Q(anime_id__title = animeName) and Q(code = codes))
                    
                    retdata = {
                            "animename":epidata.anime.title,
                            "episodes_no" : epidata.episode,
                            "seasons_no": epidata.season.season_count ,
                            "episode_name": epidata.episode_title ,
                            "episode_cover" : epidata.episode_cover ,
                            "episode_link" : epidata.episode_link 
                        }
                    print(retdata)
                   
                    return JsonResponse({'updated_value': retdata})
                
                elif Mform == "getModifyEpisode":
                    anime = request.POST.get('selected_anime')
                    Episode = EpisodesInfo.objects.filter(anime_id__title = anime).values()
                    Epilist = []
                    for data in Episode:
                        Epilist.append(data.get('code'))
                    return JsonResponse({'updated_value': Epilist})

                elif Mform == "getModifySeason":
                    anime = request.POST.get('selected_anime')
                    Anime = AnimeInfo.objects.filter(title=anime).values()[0]
                    TotalSeason = Anime.get('seasons')
                    seasons = list(range(1,TotalSeason+1))
                    return JsonResponse({'updated_value': seasons})
                
                elif Mform == "ModifySeasonInfo":
                    animeName = request.POST.get('selected_anime')
                    animeSeason = request.POST.get('selected_season')
                    epidata = SeasonInfo.objects.filter(anime_id__title = animeName, season_count = animeSeason).values()
                    for data in epidata:
                        retdata = {
                            "MS_status":data.get('status'),
                            "MS_episodes" : data.get('episode_count'),
                            
                            "MS_seasonname": data.get('season_title'),
                            "MS_AnimeImage" : data.get('season_cover'),
                            "MS_seasonbanner" : data.get('season_banner')
                        }
                        break
                    return JsonResponse({'updated_value': retdata})
            
            return render(request, 'operation.html',get_list())
        
        return render(request, 'operation.html',get_list())
        
    else:
        return render(request, 'err404.html')

def get_list():
    animedata = AnimeInfo.objects.all().values()
    epidata = EpisodesInfo.objects.all().values()
    content = {}
    anime = []
    code = []
    for animelist in animedata:
        anime.append(animelist.get('title'))
    anime.sort()
    content['animelist'] = anime
    for codes in epidata:
        code.append(str(codes.get('anime'))+"-"+str(codes.get('code')))
        content['EpiCodelist'] = code
    return content

def err404(request,exception):
    return render(request,'err404.html',status=404)


def community(request):
    Discuss = Comment.objects.filter(commenttype = "Discussion")
    Issues = Comment.objects.filter(commenttype = "Issues")
    Others = Comment.objects.filter(commenttype = "Others")
            
    content={ "DiscussMsg":Discuss,
              "IssuesMsg":Issues ,
              "OthersMsg":Others }
    
    if request.method == "POST":
        if request.POST.get('purpose') == "sendreply":
            utc_time = timezone.now()
            ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
            current_datetime_ist = ist_time.isoformat()
            info = json.loads(request.POST.get('data'))
            if info["reply"] is not None and info["reply"] != "":
                obj = Comment.objects.get(id = int(info["msgid"]))
                obj.reply = {
                    "msg":info["reply"],
                    "time":current_datetime_ist
                }
                obj.save()
        elif request.POST.get('purpose') == "discussmodify":
            info = json.loads(request.POST.get('data'))
            if info["reply"] is not None and info["reply"] != "":
                obj = Comment.objects.get(id = int(info["msgid"]))
                if info['act'] == "UserEdit": 
                    obj.comment = info["reply"]
                else:
                    obj.reply["msg"] = info["reply"]
                obj.save()

        elif request.POST.get('purpose') == "delReply" or request.POST.get('purpose') == "delComment":
            msgid = request.POST.get('data')
            obj = Comment.objects.get(id = int(msgid))
            if request.POST.get('purpose') == "delComment": 
                obj.delete()
            else:
                obj.reply = {}
                obj.save()

       
        else:
            userid = User.objects.get(username = request.POST.get('User')).id
            print(request.POST)
            if "Supports" in request.POST:
                Commentstype = "Others"
            elif "Issuesweb" in request.POST:
                Commentstype = "Issues"
            elif "DissComment" in request.POST:
                Commentstype = "Discussion"
            obj = Comment.objects.filter(user_id = userid ,
                commenttype = Commentstype,
                visibility = request.POST.get('View'),
                comment = request.POST.get('Comments'))
            
            if (len(obj)<=0):
                Comment.objects.create(
                    user_id = userid ,
                    commenttype = Commentstype,
                    visibility = request.POST.get('View'),
                    comment = request.POST.get('Comments')
                )
      
        return redirect('community')
            
    return render(request,'community.html',content)

def storage(request):
    storage = Storages.objects.all().values()
    ids=[]
    totalsize = 0
    occupiedsize = 0
    for i in storage:
        ids.append(i["id"])
        totalsize = totalsize + i["totalsize"]
        occupiedsize = occupiedsize + i["occupiedsize"]
    
    content = {
        "storage" : storage,
        "ids": ids,
        "totalsize": totalsize,
        "occupiedsize": occupiedsize,
        "free": totalsize - occupiedsize,
        "accounts":len(ids)
            
        }
    
    if request.user.is_superuser:
        if request.method == 'POST':
            if "add" in request.POST:
                if request.POST.get('Storage_Type') == "MEGA":
                    size = 20.0
                elif request.POST.get('Storage_Type') == "G-Drive":
                    size = 15.0
                else:
                    size = 0.0
                file = request.POST.get('Contain_file').split(",")
                files = {}
                if request.POST.get('Contain_file') != '':
                    for file in file:
                        data = file.split(":")
                        files[data[0]] = data[1]
        
                data = Storages.objects.create(
                    username = request.POST.get('User'),
                    email = request.POST.get('Email'),
                    passkey = request.POST.get('PassKey'),
                    recoverykey = request.POST.get('RecoverKey'),
                    storagetype = request.POST.get('Storage_Type'),
                    files = files,
                    occupiedsize = float(request.POST.get('Size')),
                    totalsize = size,
                    availsize = size - float(request.POST.get('Size')) ,
                )
                data.save()
                return redirect('storage')
                
            elif "modify" in request.POST:
                if request.POST.get('Storage_Type') == "MEGA":
                    size = 20.0
                elif request.POST.get('Storage_Type') == "G-Drive":
                    size = 15.0
                else:
                    size = 0.0
                file = request.POST.get('Contain_file').split(",")
                files = {}
                if request.POST.get('Contain_file') != '':
                    for file in file:
                        data = file.split(":")
                        files[data[0]] = data[1]
                Storages.objects.filter(id = request.POST.get('Storage_id') ).update(
                username = request.POST.get('User'),
                    email = request.POST.get('Email'),
                    passkey = request.POST.get('PassKey'),
                    recoverykey = request.POST.get('RecoverKey'),
                    storagetype = request.POST.get('Storage_Type'),
                    files = files,
                    occupiedsize = float(request.POST.get('Size')),
                    totalsize = size,
                    availsize = size - float(request.POST.get('Size')) ,
                )
                return redirect('storage')
               
            else:
                Mform = request.POST.get('formuse')
                if Mform == "ModifyStorage":
                    selected_ids = request.POST.get('selected_ids')
                    storage = Storages.objects.filter(id=selected_ids).values()
                    for data in storage:
                        files = ", ".join(f"{key}:{value}" for key, value in data.get('files', {}).items())
                        retvalue = {
                            "UserID1": data.get('username'),
                            "EmailID1": data.get('email'),
                            "Passkey1" : data.get('passkey'),
                            "Recovery1" : data.get('recoverykey'),
                            "storage1": data.get('storagetype'),
                            "size1" : data.get('occupiedsize'),
                            "Contains1": files,
                           
                        }
                        break
                    return JsonResponse({'updated_value': retvalue})
        
    return render(request,'storageinfo.html',content)
    
def analytics(request):
    user = User.objects.all()
    anime = AnimeInfo.objects.all()
    season = SeasonInfo.objects.all()
    episode = EpisodesInfo.objects.all()
   
    
    data = {}
    Total = 0
    for anime in season:
        anim = anime.anime.title       
        season = anime.season_title  
        Total += 1
        episode = EpisodesInfo.objects.filter(anime_id__title = anim, season_id = anime.id ).count()
        if anim not in data:
            data[anim] = {}
        data[anim][season] = episode 
    print(data)
    anime = get_list()
    print(anime["animelist"])
    content = {
        "UserCount":user.count() - 1,
        "Anime":anime["animelist"],
       "TotalSeason": Total,
        "Season":dict(sorted(data.items())),  
    }
    return render(request,'analytics.html',content)