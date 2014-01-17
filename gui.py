#!/usr/bin/python

import wx
from generalFunctions import generateQuestion
#from testing import passArg

class Example(wx.Frame):
           
    geom_object = None
    geom_concept = None
    geom_theorem = None
    geom_num_of_ques = None

    #def setObject(self, obj):
#	global geom_object 
#	geom_object = obj

 #   def getObject(self):
#	return geom_object

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        
        self.InitUI()
        
    def InitUI(self):   
        pnl = wx.Panel(self)
        geomObjects = ['Triangle', 'Line', 'Equilateral Triangle']
        geomConcepts = ['Perpendicular', 'Median', 'Parallel Lines']
        geomTheorems = ['Pythagoras', 'Angle sum property', 'Trigonometry']
        geomQuestionNums = ['1', '2', '3']
        
	cb = wx.ComboBox(pnl, pos=(50, 30), choices=geomObjects, 
            style=wx.CB_READONLY)
        self.st = wx.StaticText(pnl, label='object', pos=(50, 10))
        cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        
	cb1 = wx.ComboBox(pnl, pos=(300, 30), choices=geomConcepts, 
            style=wx.CB_READONLY)
        self.st = wx.StaticText(pnl, label='concept', pos=(300, 10))
        cb1.Bind(wx.EVT_COMBOBOX, self.OnSelect_concept)
        
	cb2 = wx.ComboBox(pnl, pos=(550, 30), choices=geomTheorems, 
            style=wx.CB_READONLY)
        self.st = wx.StaticText(pnl, label='theorem', pos=(550, 10))
        cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect_theorem)
	
	cb3 = wx.ComboBox(pnl, pos=(800, 30), choices=geomQuestionNums, 
            style=wx.CB_READONLY)
        self.st = wx.StaticText(pnl, label='num of questions', pos=(800, 10))
        cb3.Bind(wx.EVT_COMBOBOX, self.OnSelect_numQuestions)
       
	cbtn = wx.Button(pnl, label='Close', pos=(20, 230))
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

	cbtn_quesGen = wx.Button(pnl, label='Generate Question', pos=(20, 130))
        cbtn_quesGen.Bind(wx.EVT_BUTTON, self.OnQuesGen)
        
 
	self.SetSize((1000, 600))
        self.SetTitle('wx.ComboBox')
        self.Centre()
        self.Show(True)          
        
    def OnSelect(self, e):
        i = e.GetString()
	global geom_object
	geom_object = i
        print("inside Onselect object, object selected is " + geom_object)
        #self.st.SetLabel(i)
        #self.st = wx.StaticText(pnl, label='', pos=(100, 140))
        
    def OnSelect_concept(self, e):
        i = e.GetString()
	global geom_concept
	geom_concept = i
        print("inside Onselect_concept, conept slected is  "+ geom_concept)
        #self.st.SetLabel(i)
        #self.st = wx.StaticText(pnl, label='', pos=(400, 140))

    def OnSelect_theorem(self, e):
        print("inside Onselect_theorem ")
        i = e.GetString()
	global geom_theorem
	geom_theorem = i
        #self.st.SetLabel(i)
        #self.st = wx.StaticText(pnl, label='', pos=(400, 140))


    def OnSelect_numQuestions(self, e):
        print("inside Onselect_numQuestions ")
        i = e.GetString()
	global geom_num_of_ques
	geom_num_of_ques = i
        #self.st.SetLabel(i)
        #self.st = wx.StaticText(pnl, label='', pos=(400, 140))

    def OnClose(self, e):
        print("inside OnClose ")
        self.Close(True) 

    def OnQuesGen(self, e):
        print("inside OnGenerateQuestion ")
	dc = wx.PaintDC(e.GetEventObject())
        #dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(200, 200, 500, 500) 

	#Calling this function to start algorithm for question generation
	generateQuestion(geom_object, geom_concept, geom_theorem, geom_num_of_ques)
	#passArg(geom_object, geom_concept, geom_theorem, geom_num_of_ques)

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()   
