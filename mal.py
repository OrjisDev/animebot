from deep_translator import GoogleTranslator
import requests
#Import des deux bibliotheques pour traduire et faire des requêtes à l'API Myanimelist

Header = {"X-MAL-CLIENT-ID" : "VOTRE TOKEN D'API MAL" #Header pour authentifier la requête 
    }

def get_anime(Anime):
    """
    Entrée : str
    Sortie : Liste de tuples
    But : Utiliser l'api de MyAnimeList pour obtenir une liste de tuple qui représente un couple (Id de l'anime, nom de l'anime)
    en fonction du nom rentré en entrée pour obtenir une liste possible de pages représentant l'anime en question
    """
    animelist = "https://api.myanimelist.net/v2/anime?q="+str(Anime)+"&limit=5"
    response = requests.get(animelist,headers=Header)
    body = response.json()
    lenlist = len(body['data'])
    newanimelist = []
    for i in range(lenlist):
        list = body['data'][i]['node']['id'],body['data'][i]['node']['title']
        newanimelist.append(list)
    return newanimelist

def get_resume(anime_id):
    """
    Entrée : Int
    Sortie : Tuple
    But : Utiliser l'API de MyAnimeList pour obtenir des variables qui repésenent plusieurs choses sur un anime
    en fonction de l'id entré comme : Sa date de parution, sa date de fin, le synopsis (traduit de l'anglais en français grâce à deep_translator)
    ,sa note, son statut et le nombre d'épisodes et une image dans un tuple
    """
    animedetails = "https://api.myanimelist.net/v2/anime/"+str(anime_id)+"?fields=start_date,end_date,synopsis,mean,status,num_episodes"
    animedet = requests.get(animedetails,headers=Header)
    bodydetails = animedet.json()
    title = bodydetails['title']
    start_date = bodydetails['start_date']
    if 'end_date' in bodydetails:
        end_date = bodydetails['end_date']
    else:
        end_date = "Anime non fini"
    synopsisen = bodydetails['synopsis']
    synopsisfr = GoogleTranslator(source='en',target='fr').translate(synopsisen)
    synopsisfr = synopsisfr.replace("[Écrit par MAL Rewrite]","")
    note = str(bodydetails['mean'])
    if bodydetails['status'] == 'currently_airing':
        statut = "En cours"
    elif bodydetails['status'] =='finished_airing':
        statut = "Terminé"
    else:
        statut = "Pas commencé"
    if bodydetails['num_episodes'] == 0:
        ep = "Non défini"
    else:
        ep = str(bodydetails['num_episodes'])
    image = (bodydetails['main_picture']['large'])
    retour = (title,start_date,end_date,synopsisfr,note,statut,ep,image)
    return(retour)
