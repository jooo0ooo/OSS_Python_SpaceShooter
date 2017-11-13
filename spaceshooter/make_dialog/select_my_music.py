#Write txt file to save user's music path
import wx
from os import path

text_dir = path.join(path.abspath(path.join(path.dirname(__file__),"..")), 'text')

app = wx.App()
frame = wx.Frame(None, -1, 'test')
frame.SetSize(0, 0, 200, 50)
# Create open file dialog
openFileDialog = wx.FileDialog(frame, "Open", "", "",
                                   "mp3 files (*.mp3)|*.mp3",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
openFileDialog.ShowModal()
openFileDialog.Destroy()
f = open(path.join(text_dir, 'user_music_location.txt'), 'w')
f.write(openFileDialog.GetPath())
f.close
