from gpiozero import Button

def checkCallBell():
    button = Button(2)
    if button.is_pressed:
        return True
    else: return False
