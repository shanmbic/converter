#Author: Shantanu Srivastava
#Version : 1.0
#A simple video converter to convert files to 320p and 640p in mpeg4 resolution.
#Built in python requires wxPython and FFMPEG for full functionality. 
#Tested on x-86 machine running Ubuntu 13.10-64bit

import wx
import os
import subprocess

class MainWindow(wx.Frame):
   def __init__(self, parent, title):
      self.dirname='Please select an input directory'
      self.outdirname='Please select output directory'
      
      wx.Frame.__init__(self, parent, title=title, size=(400,-1))
      self.CreateStatusBar() 

      # Setting up the menubar
      filemenu= wx.Menu()
      menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
      menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
      menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
      menuBar = wx.MenuBar()
      menuBar.Append(filemenu,"&File")
      self.SetMenuBar(menuBar)

      #Setting the input and output path labels for the UI 
      self.inputquote = wx.StaticText(self, label="Source Input :", pos=(10, 0))
      self.outputquote = wx.StaticText(self, label="Output Path :", pos=(10, 0))
      self.inputlabel = wx.TextCtrl(self, value=self.dirname, pos=(0, 0), size=(300,-1))
      self.outputlabel = wx.TextCtrl(self, value=self.outdirname, pos=(0, 0), size=(300,-1))
      
      self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
      self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
      self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
   
      #Buttons for UI
      self.openvideo = wx.Button(self, -1, "Open Video")
      self.Bind(wx.EVT_BUTTON, self.OnOpen, self.openvideo)
      self.convertvideo = wx.Button(self, -1, "Convert Video")
      self.Bind(wx.EVT_BUTTON, self.Process, self.convertvideo)
      self.outputfolder = wx.Button(self, -1, "Set output folder")
      self.Bind(wx.EVT_BUTTON, self.OnOpenFolder, self.outputfolder)

      #Sizers for relative layouts
      self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
      self.sizer1.Add(self.openvideo, 1, wx.EXPAND)
      self.sizer1.Add(self.convertvideo, 2, wx.EXPAND)
      self.sizer1.Add(self.outputfolder, 3, wx.EXPAND)

      self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
      self.sizer2.Add(self.inputquote, 1, wx.EXPAND)
      self.sizer2.Add(self.inputlabel, 2, wx.EXPAND)

      self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
      self.sizer3.Add(self.outputquote, 1, wx.EXPAND)
      self.sizer3.Add(self.outputlabel, 2, wx.EXPAND)

      # Vertical sizer
      self.sizer = wx.BoxSizer(wx.VERTICAL)
      self.sizer.Add(self.sizer1, 0, wx.EXPAND)
      self.sizer.Add(self.sizer2, 1, wx.EXPAND)
      self.sizer.Add(self.sizer3, 2, wx.EXPAND)

      #Layout sizers
      self.SetSizer(self.sizer)
      self.SetAutoLayout(1)
      self.sizer.Fit(self)
      self.Show()

   def OnAbout(self,e):
      # Create a message dialog box which displays the about information.
      dlg = wx.MessageDialog(self, "Converts any video files to mp4(320p and 640p)", "About Video Editor", wx.OK)
      dlg.ShowModal() 
      dlg.Destroy()

   def OnExit(self,e):
      # Close the application.
      self.Close(True) 

   def OnOpen(self,e):
      #Dialogue to select an input video file
      dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
      if dlg.ShowModal() == wx.ID_OK:
         self.filename = dlg.GetFilename()
         self.dirname = dlg.GetDirectory()
         self.inputlabel.ChangeValue(self.dirname+"/"+self.filename)
      dlg.Destroy()

   def OnOpenFolder(self,e):
      #Dialogue to select an output directory
      dlg = wx.DirDialog(self, "Choose a folder")
      if dlg.ShowModal() == wx.ID_OK:
         self.outdirname = dlg.GetPath()
         self.outputlabel.ChangeValue(self.outdirname)
      dlg.Destroy()

   def Process(self, e):
      #Checks if output directory has been selected or not
      if(self.outdirname=='Please select output directory'):
         dlg1 = wx.MessageDialog(self, "Please select an output directory.", "Error", wx.OK)
         dlg1.ShowModal()
         dlg1.Destroy()
         return
      self.createfolders() #Calls the method for creating directories 
      self.inputfile = self.dirname+ "/" + self.filename #File location string for commandline
      x=list(self.filename)
      x=x[:len(x)-4]
      s=""
      for i in x:
         s=s+str(i)
      #Output commands
      self.outputfile1 = self.outdirname + "/" + self.filename + "/320p" + "/" + s + ".mp4"
      self.outputfile2 = self.outdirname + "/" + self.filename + "/640p" + "/" + s + ".mp4"
      self.commandstring1 = "ffmpeg -i " + self.inputfile + " -s 320x240 -vcodec mpeg4 -acodec ac3 -ar 48000 -ab 192k " +  self.outputfile1
      self.commandstring2 = "ffmpeg -i " + self.inputfile + " -s 640x480 -vcodec mpeg4 -acodec ac3 -ar 48000 -ab 192k " +  self.outputfile2

      self.SetStatusText("Converting to 320*240. Please wait !") 

      m=subprocess.call(['ffmpeg', '-i', self.inputfile, '-s', '320x240', '-vcodec', 'mpeg4', '-acodec', 'ac3', '-ar', '48000', '-ab', '192k',   self.outputfile1]) #os.system(self.commandstring1)
      if(m==0): #checks if the conversion is successful or not 
         dlg1 = wx.MessageDialog(self, "Converted 320*240. Check file in " + self.outdirname, "Finished", wx.OK)
         dlg1.ShowModal()
         dlg1.Destroy()
      else:
         dlg1 = wx.MessageDialog(self, "Conversion Unsuccessful for 320p. Some codecs are missing ", "Failed", wx.OK)
         dlg1.ShowModal()
         dlg1.Destroy()

      self.SetStatusText("Converting to 640*480. Please wait !")
      n=subprocess.call(['ffmpeg', '-i', self.inputfile, '-s', '640x480', '-vcodec', 'mpeg4', '-acodec', 'ac3', '-ar', '48000', '-ab', '192k',   self.outputfile2]) #os.system(self.commandstring2)
      if(n==0):
         dlg1 = wx.MessageDialog(self, "Converted 640*480. Check file in " + self.outdirname, "Finished", wx.OK)
         dlg1.ShowModal()
         dlg1.Destroy()
      else:
         dlg1 = wx.MessageDialog(self, "Conversion Unsuccessful for 640p. Some codecs are missing.", "Finished", wx.OK)
         dlg1.ShowModal()
         dlg1.Destroy()
      if(m!=0 or n!=0):
         self.SetStatusText("Not all videos were successfully converted ! Please try again.")
      else:
         self.SetStatusText("All videos successfully converted")

   def createfolders(self):
      #Create the sub directories 
      self.path=self.outdirname+"/"+self.filename
      if not os.path.exists(self.path):
         self.outputlabel.ChangeValue(self.path)
         os.makedirs(self.path)
         os.makedirs(self.path+"/320p")
         os.makedirs(self.path+"/640p")
      subprocess.call(['cp', self.dirname + "/" + self.filename, self.path])#Copy of the original file into the new directory

   


app = wx.App(False)
frame = MainWindow(None, "Video Converter")
app.MainLoop()
