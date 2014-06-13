import wx
import wx.lib.imagebrowser as imagebrowser

class ImageDialogApp(wx.App):
    def OnInit(self):
        self.frame = ImageDialogFrame(None, title = "ImageDialog")
        self.frame.Show()
        return True
class ImageDialogFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ImageDialogFrame, self).__init__(*args, **kwargs)

        self.panel = ImageDialogPanel(self)

class ImageDialogPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ImageDialogPanel, self).__init__(*args, **kwargs)

        self.lastpath = None
        self.bmp = wx.StaticBitmap(self)
        self.btn = wx.Button(self, label = "Choose Image")

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.Add(self.bmp, 0, wx.ALIGN_CENTER)
        vsizer.AddSpacer((5,5))
        vsizer.Add(self.btn, 0, wx.ALIGN_CENTER)
        hsizer.AddStretchSpacer()
        hsizer.Add(vsizer, 0, wx.ALIGN_CENTER)
        hsizer.AddStretchSpacer()
        self.SetSizer(hsizer)


        self.Bind(wx.EVT_BUTTON, self.OnShowDialog, self.btn)

    def OnShowDialog(self, event):
        dlg = imagebrowser.ImageDialog(self, self.lastpath)
        if dlg.ShowModal() == wx.ID_OK:
            self.lastpath = dlg.GetDirectory()
            imgpath = dlg.GetFile()
            bitmap = wx.Bitmap(imgpath)

            if bitmap.IsOk():
                self.bmp.SetBitmap(bitmap)
                self.Layout()
                self.bmp.Refresh()
        dlg.Destroy()
if __name__ == '__main__':
    app = ImageDialogApp(False)
    app.MainLoop()

