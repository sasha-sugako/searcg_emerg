def spn_func(coord_top, org_point):
    d1 = coord_top.split(',')
    d2 = org_point.split(',')
    d11= d1[0]
    d21 = d2[0]
    d12 = d1[1]
    d22 = d2[1]
    if float(d21) > float(d11):
        d11, d21 = d21, d11
    if float(d22) > float(d12):
        d12, d22 = d22, d12
    deltax, deltay = str(float(d11) - float(d21) + 0.0025), str(float(d12) - float(d22) + 0.0025)
    return[deltax, deltay]