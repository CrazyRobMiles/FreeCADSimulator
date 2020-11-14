from tkinter import *

class TKDisplay(object):
    def __init__(self, width, height):
        self.message = ""
        self.drawObjects = []   

        self.root = Tk()

        self.root.title("FakeFreeCAD - Rob Miles")

        self.xOffset = 20
        self.yOffset = 20

        self.width = width
        self.height = height

        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.grid(row=0, column=0)

        self.output_Text = Text(self.root, height=5)
        self.output_Text.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        output_Scrollbar = Scrollbar(self.root, command=self.output_Text.yview)
        output_Scrollbar.grid(row=1, column=1, sticky='nsew')
        self.output_Text['yscrollcommand'] = output_Scrollbar.set

        self.root.update()

    def zoomIn(self,amount):
        self.canvas.scale(ALL, 0, 0, amount, amount)

    def mainloop(self):
        self.root.mainloop()    

    def addMessageLine(self, text):
        text = text + "\n"
        self.output_Text.insert(END,text)
        self.output_Text.see(END)

    def addDrawelement(self,item):
        self.drawObjects.append(item)

    def drawRectangle(self,x1,y1,x2,y2,fill, outline):
        x1 = x1+self.xOffset
        x2 = x2+self.xOffset
        y1 = self.height-(y1+self.yOffset)
        y2 = self.height-(y2+self.yOffset)
        print("draw rectangle: ", fill)
        self.canvas.create_rectangle(x1,y1,x2,y2,fill=fill, outline=outline)

    def drawCircle(self,x,y,r,fill, outline):
        x = x+self.xOffset
        y = self.height-(y+self.yOffset)
        print("draw circle: ", fill)
        self.canvas.create_oval(x-r, y-r, x+r, y+r,fill=fill, outline=outline)


class Display(object):
    message = ""
    drawObjects = []
    imageCanvas = None

    @staticmethod
    def addMessageLine(text):
        print(text)
        if Display.imageCanvas!=None:
            Display.imageCanvas.addMessageLine(text)

    @staticmethod
    def addDrawelement(item):
        if Display.imageCanvas!=None:
            Display.imageCanvas.addDrawelement(item)

    scalefactor = 1

    @staticmethod
    def setCanvas(c):
        Display.imageCanvas = c

    @staticmethod
    def drawRectangle(x1,y1,x2,y2,fill, outline):
        if Display.imageCanvas!=None:
            Display.imageCanvas.drawRectangle(x1,y1,x2,y2,fill,outline)
    
    @staticmethod
    def drawCircle(x,y,r,fill, outline):
        if Display.imageCanvas!=None:
            Display.imageCanvas.drawCircle(x,y,r,fill,outline)

class FreeCadView(object):
    @staticmethod 
    def viewAxometric():
        Display.addMessageLine("Freecad Axiometric view selected")

class FreeCadDocument(object):

    @staticmethod
    def activeView():
        return FreeCadView()

class Gui(object):
    
    @staticmethod
    def SendMsgToActiveView(message):
        Display.addMessageLine(message)
  
    @staticmethod
    def activeDocument():
        return FreeCadDocument()
   
class FreeCAD(object):
    @staticmethod
    def newDocument():
        print("New Document")
        return "New Document"

class Base(object):
    class Vector:
        x=0
        y=0
        z=0
        def __init__(self, x,y,z):
            self.x=x
            self.y=y
            self.z=z

class Component(object):

    drawAction = "none"

    componentList = []

    position=Base.Vector(0,0,0)

    def __init__(self, position):
        self.position = position

    def fuse(self, component):
        selfCopy = self.copy()
        fuseCopy = component.copy()
        fuseCopy.drawAction="fuse"
        selfCopy.componentList.append(fuseCopy)
        return selfCopy

    def cut(self, component):
        selfCopy = self.copy()
        fuseCopy = component.copy()
        fuseCopy.drawAction="cut"
        selfCopy.componentList.append(fuseCopy)
        return selfCopy

    def copy(self):
        result = Component(self.position)
        result.componentList = list(self.componentList)
        result.drawAction = self.drawAction
        return result

    def translate(self,vector):
        pass

    def show(self):
        message = "Component "+self.drawAction+" at (" + str(self.position.x) + ","+str(self.position.y)+","+str(self.position.y) + ")"
        Display.addMessageLine(message)
        for c in self.componentList:
            c.show()

    def drawColour(self):
        colour = "cyan"
        if self.drawAction == "fuse":
            colour="blue"
        else: 
            if self.drawAction == "cut":
                colour="red"
            else:
                colour = "yellow"
        return colour

class Box(Component):
    width=0
    height=0
    depth=0
    def __init__(self, width,height,depth,position):
        super(Box,self).__init__(position)
        self.width=width
        self.height=height
        self.depth=depth

    def copy(self):
        result = Box(self.width, self.height, self.depth,self.position)
        result.componentList = list(self.componentList)
        return result

    def show(self):
        message = "Box "+self.drawAction+" at (" + str(self.position.x) + ","+str(self.position.y)+","+str(self.position.y) + ") W:"+str(self.width) + " H:"+str(self.height)+" D:"+str(self.depth)
        Display.addMessageLine(message)
        x1=self.position.x
        y1=self.position.y
        x2=x1+self.width
        y2=y1+self.height
        colour = self.drawColour()
        Display.drawRectangle(x1,y1,x2,y2,colour,colour)
        for c in self.componentList:
            c.show()

class Cylinder(Component):
    radius=0
    height=0
    dir = Base.Vector(0,0,1)

    def __init__(self, radius,height,position, dir=Base.Vector(0,0,1)):
        super(Cylinder,self).__init__(position)
        self.radius=radius
        self.height=height
        self.dir = dir

    def copy(self):
        result = Cylinder(self.radius, self.height, self.position, self.dir)
        result.componentList = list(self.componentList)
        return result

    def show(self):
        message = "Cylinder "+self.drawAction+" at (" + str(self.position.x) + ","+str(self.position.y)+","+str(self.position.y) + ")"
        Display.addMessageLine(message)
        colour = self.drawColour()
        Display.drawCircle(self.position.x, self.position.y, self.radius, colour, colour)
        for c in self.componentList:
            c.show()

    def rotate(self,origin, axis, amount):
        pass

class Part(object):
    @staticmethod
    def makeBox(width, height, depth, position=Base.Vector(0,0,0)):
        return Box(width,height,depth,position)
    @staticmethod
    def makeCylinder(radius,height,position=Base.Vector(0,0,0),dir=Base.Vector(0,0,1)):
        return Cylinder(radius,height,position)
    @staticmethod
    def show(component):
        component.show()
