from externalized.contrib.core import AbstractActivityKernel

import dropbox, sys
import webbrowser
class DropboxActivityKernel(AbstractActivityKernel):
    def __init__(self,api_key,api_secret,activity_name):
        AbstractActivityKernel.__init__(self, api_key, api_secret)
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
        print('Linked Dropbox ArcherDrive: ', self.client.account_info())
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
        