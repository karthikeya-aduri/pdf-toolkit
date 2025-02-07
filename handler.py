from constants import hoverColor, backgroundColor, eventMap

def onEnter(element):
    element.widget['background'] = hoverColor

def onLeave(element):
    element.widget['background'] = backgroundColor

def handleHover(button):
    button.bind("<Enter>", onEnter)
    button.bind("<Leave>", onLeave)

def callEventListener(displayContainer, index):
    func = eventMap[index]
    if func:
        func(displayContainer)
