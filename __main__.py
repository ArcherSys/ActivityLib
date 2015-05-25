#!/usr/local/bin/python2.7
# encoding: utf-8
import turtle
'''
ActivityLib.__main__ -- shortdesc

ActivityLib.__main__ is a CLI Version of the ActivityLib

It defines classes_and_methods for activity

@author:     Weldon Henson

@copyright:  2015 ArcherSys OS Foundation. All rights reserved.

@license:    MIT

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


import cmd, dropbox, webbrowser



__version__ = 0.1
__date__ = '2015-05-22'
__updated__ = '2015-05-22'

DEBUG = 0
TESTRUN = 0
PROFILE = 0
class AbstractActivityKernel(cmd.Cmd):
    def __init__(self,api_key,api_secret):
        cmd.Cmd.__init__(self)
        self.api_key = api_key
        self.api_secret = api_secret
class Activity(object):
    def __init__(self,activity_name):
        pass
    def __call___(self):
        pass
    

class DropboxActivityKernel(AbstractActivityKernel):
    def __init__(self,api_key,api_secret,activity_name):
        AbstractActivityKernel.__init__(self, api_key, api_secret)
        self.app_key = api_key
        self.app_secret = api_secret
        self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        self.authorize_url = self.flow.start()
        print ('1. Go to: ' + self.authorize_url)
        print ('2. Click "Allow" (you might have to log in first)')
        print ('3. Copy the authorization code.')
        self.open_url()
        self.code = input("Enter the authorization code here: ").strip()
        self.intro = "ArcherBash v2.0.0 for ArcherSys OS 3.4.1 - " + activity_name
        self.access_token, self.user_id = self.flow.finish(self.code)
        self.prompt = activity_name + ">>"
        self.client = dropbox.client.DropboxClient(self.access_token)
        print('Linked Dropbox ArcherDrive for ', self.client.account_info())
    def open_url(self):
        webbrowser.open_new_tab(self.authorize_url)
    def do_upload(self, arg):
        f = open(input("File to upload:"), 'rb')
        response = self.client.put_file(input("Filename:"), f)
        print("="*41)
        print("Uploaded file from ArcherVM:", response)
        print("="*41)
    def do_getfolders(self,arg):
        folder_metadata = self.client.metadata(input("Path:"))
        print("="*41)

        print ("My Metadata:", folder_metadata)
        print("="*41)

    def do_download_files(self,arg):
        '''
        Downloads a file using user input from Dropbox
        '''
        filename = input("File to upload")
        f, metadata = self.client.get_file_and_metadata(filename)
        out = open(filename, 'wb')
        out.write(f.read())
        out.close()
        print("="*41)
        print(metadata)
        print("="*41)

    def do_EOF(self):
        sys.exit()
    def __call__(self):
        self.cmdloop()
        
class DropboxActivity(object):
    '''
    classdocs
    '''


    def __init__(self, activity_name):
        '''
        Constructor
        '''
        self.activity_name = activity_name
        self.cli = DropboxActivityKernel('brwekpcno93vtpz','np5coz7g4nzp9og',activity_name)
    def __call__(self):
        self.cli.cmdloop()        
class TurtleistActivityKernel(AbstractActivityKernel):
    def __init__(self,activity_name,api_key,api_secret):
        AbstractActivityKernel.__init__(self, api_key, api_secret)
        self.title = activity_name
        self.screen = turtle.Screen()
        self.turt = turtle.Turtle()
        self.prompt = "Turtleist:"+activity_name+">>"
    def do_forward(self,arg):
        self.turt.forward(int(arg))
    def do_right(self,arg):
        self.turt.right(int(arg))
    def do_left(self, arg):
        self.turt.left(int(arg))
    def do_backwards(self, arg):
        self.turt.back(int(arg))
    def do_penup(self,arg):
        self.turt.penup()
    def do_pendown(self, arg):
        self.turt.pendown()
    def do_EOF(self,line):
        pass
    def do_clear(self,arg):
        self.turt.clear()
    def do_home(self,arg):
        self.turt.home()
    def do_go_home(self,arg):
        self.turt.penup()
        self.turt.home()
    def do_killscreen(self, arg):
        self.screen.exitonclick()
    def do_rebirth(self, arg):
        self.screen = turtle.Screen()
        self.turt = turtle.Turtle()
class TurtleistActivity(Activity):
    def __init__(self,activity_name):
        self.cli = TurtleistActivityKernel(activity_name,None,None)
    def __call__(self):
        self.cli.cmdloop()
        
class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__
    program_license = '''%s

  Created by Weldon Henson on %s.
  Copyright 2015 ArcherSys OS Foundation. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-a',"--activity",required=True, dest="activity", help='Activity Name')
        
        # Process arguments
        args = parser.parse_args()

       
       
        activity = args.activity
        if activity == "DropboxActivity":
            activity_verbose = DropboxActivity(input("Activity Name:"))
            activity_verbose()
        elif activity == "TurtleistActivity":
            activity = TurtleistActivity(input("Activity Name:"))
            activity()
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0





if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'ActivityLib.__main___profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
main()