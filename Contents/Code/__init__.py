import putio2


NAME = 'Put.io'

ART = 'art-default.jpg'
ICON = 'icon-default.png'


def Start():
    Plugin.AddViewGroup('InfoList', viewMode = 'InfoList', mediaType = 'items')
    Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')
    Plugin.AddViewGroup('Photos', viewMode = 'List', mediaType = 'photos')
    
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = NAME
    
    DirectoryItem.thumb = R(ICON)


@handler('/video/putio', NAME, art = ART, thumb = ICON)
def MainMenu():
    return ParseDirectory(0, NAME)


@route('/video/putio/directory/{id}')
def ParseDirectory(id, name):
    Log.Info("**************kedilerimiz")

    oc = ObjectContainer(title1 = name, view_group = 'InfoList')


    oc.add(PrefsObject(title = L('Preferences')))


    client = putio2.Client(Prefs['access_token'])

    Log.Info("*********kopeklerimiz")

    try:
        for f in client.File.list(id):
            Log.Info("*********aha fora girdik")

            if f.content_type == 'application/x-directory':
                oc.add(DirectoryObject(
                    key = Callback(ParseDirectory, id = f.id, name = f.name),
                    title = f.name))
            
            elif f.content_type.startswith('video/'):
                oc.add(VideoClipObject(
                    key = Callback(Lookup, id = f.id),
                    items = [ MediaObject(parts = [ PartObject(key = Callback(PlayMedia, url = f.stream_url)) ]) ],
                    rating_key = f.id,
                    title = f.name,
                    thumb = f.screenshot))
            
            elif f.content_type.startswith('audio/'):
                oc.add(TrackObject(
                    key = Callback(Lookup, id = f.id),
                    items = [ MediaObject(parts = [ PartObject(key = Callback(PlayMedia, url = f.stream_url)) ]) ],
                    rating_key = f.id,
                    title = f.name,
                    thumb = f.screenshot))
            
            else:
                Log.Info("Unsupported content type '%s'" % f.content_type)

    except:
        pass
    
    Log.Info("****** oc yi return edicem")
    return oc


@route('/video/putio/lookup')
def Lookup(id):
    oc = ObjectContainer()
    id = int(id)
    
    client = putio2.Client(Prefs['access_token'])
    f = client.File.get(id)
    
    if f.content_type.startswith('video/'):
        oc.add(VideoClipObject(
            key = Callback(Lookup, id = f.id),
            items = [ MediaObject(parts = [ PartObject(key = Callback(PlayMedia, url = f.stream_url)) ]) ],
            rating_key = f.id,
            title = f.name,
            thumb = f.screenshot))
    
    elif f.content_type.startswith('audio/'):
        oc.add(TrackObject(
            key = Callback(Lookup, id = f.id),
            items = [ MediaObject(parts = [ PartObject(key = Callback(PlayMedia, url = f.stream_url)) ]) ],
            rating_key = f.id,
            title = f.name,
            thumb = f.screenshot))
    
    else:
        Log.Info("Unsupported content type '%s'" % f.content_type)
    
    return oc


@route('/video/putio/play')
def PlayMedia(url):
    return Redirect(url)
