from geopy.distance import geodesic #pip install geopy
 
def test():
    origin = (30.172705, 31.526725)  # (latitude, longitude) don't confuse
    dist = (30.288281, 31.732326)

    # print(geodesic(origin, dist).meters,'meters')  # 23576.805481751613
    # print(geodesic(origin, dist).kilometers,'kilometers')  # 23.576805481751613
    # print(geodesic(origin, dist).miles,'miles')  # 14.64994773134371

    # print('inter=',geodesic((1,1),(1.01,1)).meters,'meters') #1 110km  #0.1 11km #0.01 1.1km
    
    pts = [[-36.854265, 174.766519],
           [-36.850265, 174.762519],
           [-36.848265, 174.748519]]
    
    pts1 = (pts[0][0], pts[0][1])
    pts2 = (pts[1][0], pts[1][1])
    pts3 = (pts[2][0], pts[2][1])
    
    print(geoDistance(pts1,pts2))
    print(geoDistance(pts1,pts3))
    
def geoDistance(origin,dst):
    return geodesic(origin, dst).meters
    #return geodesic(origin, dst).kilometers
    #return geodesic(origin, dst).miles

if __name__=='__main__':
    test()
