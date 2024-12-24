import consts

def getPosFromMouseCords(mouse_x, mouse_y):
    row = (mouse_y - consts.Y_CENTER_OFFSET) // consts.SQUARE_SIZE
    col = (mouse_x - consts.X_CENTER_OFFSET) // consts.SQUARE_SIZE
    return int(row), int(col)  
