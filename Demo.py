from FakeFreeCad import *

### code from FreeCad starts here
### Make it into a function that can be called to make the part

def makePlate():

    plate = Part.makeBox(800,600,100)
    hole = Part.makeCylinder(200,200,Base.Vector(400,300,0))
    plate = plate.cut(hole)

    Part.show(plate)
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewAxometric()

### End of the FreeCad code

# Open the display

tk_display = TKDisplay(1000,600)

Display.setCanvas(tk_display)

Display.addMessageLine("Gadgetmaker 1.0 by Rob Miles")

# Call the FreeCad function to design the part

makePlate()

# Display the output

tk_display.mainloop()
