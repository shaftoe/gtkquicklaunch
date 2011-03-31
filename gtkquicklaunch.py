#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import subprocess
import ConfigParser

class QuickLaunch():
    def __init__(self):
        self.fetchParametersFromFile()
        return None

    def fetchParametersFromFile(self, configFileName='gtkquicklaunch.config'):
        configPath = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0],configFileName)        
        config = ConfigParser.RawConfigParser() # fetch parameters from a config file
        config.read(configPath)
        self.programsToRun = config.defaults().values() # set those parameters as the actual programs to run

    def setProgramsToRun(self, programsToRun):
        self.programsToRun = programsToRun
        return None

    def getProgramsToRun(self):
        return self.programsToRun

    def actuallyRunPrograms(self):
        if self.programsToRun:
            for i in self.programsToRun:
                try:
                    subprocess.Popen(i) # actually run program via subprocess
                except OSError:
                    print "Something wrong with %s. Double check path and permissions" % i
        else: print("nothing to do")
        return None

class GtkQuickLaunch():
    def __init__(self, cliobject):
        '''Main class to handle all the grafical GUI'''        
        self.cliobject = cliobject # this is the QuickLaunch object who does the job
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_NONE)
        self.window.set_title("QuickLaunch")
        self.window.set_border_width(20)
        self.window.connect("destroy", self.destroy)
        
        self.verticalBox = gtk.VBox(False, 0)

        self.createCheckButtons()
        self.createOkButton()
        self.createCloseButton()

        self.window.add(self.verticalBox)

        self.verticalBox.show()        
        self.window.show()

    def createCheckButtons(self):
        self.checkButtonList = self.cliobject.getProgramsToRun()
        counter = 0
        self.checkButtons = []
        for i in self.checkButtonList:
            self.checkButtons.append(gtk.CheckButton(i, False))
            self.checkButtons[counter].set_active(True)
            self.checkButtons[counter].show()
            self.verticalBox.pack_start(self.checkButtons[counter], True, True, 0)
            counter += 1

    def getCheckedButtonsNames(self):
        checkedButtons = []     
        for i in self.checkButtons:
           if i.get_active():
                checkedButtons.append(i.get_label())
        return checkedButtons
        
    def createOkButton(self):
        button = gtk.Button('Run!')
        button.connect_object("clicked", self.okButtonCallback, None)
        self.verticalBox.pack_start(button, True, True, 0)
        button.show()

    def createCloseButton(self):
        button = gtk.Button('Exit')
        button.connect_object("clicked", self.destroy, None)
        self.verticalBox.pack_start(button, True, True, 0)
        button.show()

    def okButtonCallback(self, widget, data=None):
        self.cliobject.setProgramsToRun(self.getCheckedButtonsNames())
        self.cliobject.actuallyRunPrograms()
        gtk.main_quit()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == '__main__':
    base = QuickLaunch()
    gui = GtkQuickLaunch(base)
    gui.main()
