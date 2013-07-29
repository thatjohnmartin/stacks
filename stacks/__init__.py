# Initialize global namespace
# -------------------------

from stacks.www.namespace import NameSpace, WikipediaNameSpace, MountainProjectNameSpace, FlickrNameSpace
directory = NameSpace()
directory['wikipedia'] = WikipediaNameSpace()
directory['mountain_project'] = MountainProjectNameSpace()
# directory['users.johnm.flickr'] = FlickrNameSpace(FLICKR_API_KEY, flickr_username='johnmartin78')
