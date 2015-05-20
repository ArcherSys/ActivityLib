import externalized.dropbox.activitykernel.DropboxActivityKernel

'''
Created on May 20, 2015

@author: Weldon Henson
'''
from externalized.dropbox.activitykernel import DropboxActivityKernel

class DropboxActivity(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        DropboxActivityKernel.__init__(params["api_key"],params["api_secret"],params["activity_name"])
        '''
        Constructor
        '''
        