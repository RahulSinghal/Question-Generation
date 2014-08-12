def angle_between_lines(pt1, pt2,pt3,pt4):
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]
    x3 = pt3[0]
    y3 = pt3[1]
    x4 = pt4[0]
    y4 = pt4[1]
    #TODO
    return 10
#End Of Function

def slope(pt1, pt2):
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]
    
    xslope = x2 - x1
    if xslope == 0 : return math.pi/2
    yslope = y2 - y1
    return math.atan(yslope/xslope)
#End Of Function

temp1 = [0, 0]
cord1 = [0, 1]
ang = slope(temp1,cord1)*180/math.pi
#print (ang)

