

import sys
import cv2
import os
import numpy as np
import time

from LibDriver.Interface import *

if __name__ == '__main__':
    print(cv2.__version__)
    print(os.getcwd())

    AsmFileName = b"ScriptFreeModel.txt"
    SimWindowText = b"GL Exam1"
    InitSimulation(AsmFileName, SimWindowText)

    Color_width = 1280
    Color_Height = 720
    Color_image = np.zeros((Color_Height, Color_width, 3), np.uint8)

    im_width = 300
    im_height = 300
    Depth_Mask = np.zeros((im_height, im_width, 3), np.uint8)
    Depth_Map = np.zeros((im_height, im_width), np.float32)
    Color_Img = np.zeros((im_height, im_width, 3), np.uint8)
    SingleMask = np.zeros((im_height, im_width), np.uint8)

    PosTest_x = 0
    AttTest_x = 0

    TypeIndex = 1;
    while(True):
        GetColorImage(Color_image.ctypes, Color_width, Color_Height)
        cv2.imshow("Color Image", Color_image);

        k = cv2.waitKey(30) & 0xFF

        if k == 100: #ASICC 'd' Depth
            print("depth map")

            t0 = time.monotonic()
            GetDepthMap(Depth_Map.ctypes, Depth_Mask.ctypes, im_width, im_height, 12, 0, 0, 1280, 720)
            t1 = time.monotonic() - t0
            print("Time elapsed: ", t1)

            ObjIDMask, FaceIDMask, EdgeMask = cv2.split(Depth_Mask)

            Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
            cv2.imshow("Depth Map", Depth_Map);
            cv2.imshow("Depth Mask", EdgeMask);

        if k == ord('l'): #Load Binary DepthMap
            if 0 != LoadBinDepthMapPnt("DepthPnt.txt", im_width, im_height, 600, 6000, Depth_Map.ctypes, SingleMask.ctypes):
                Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
                cv2.imshow("Depth Map", Depth_Map);
                cv2.imshow("Depth Mask", SingleMask);
            else:
                print("Loading Error")

        if k == ord('m'):  # Mesh Up
            MeshUpObjID = 4     #FREEMODEL Type ID
            MeshInterval = 10   #Interval for making triangles
            ret = ObjMeshUp(im_width, im_height, MeshUpObjID, MeshInterval)
            print(ret)

        if k == ord('g'):  #get vetex
            print(GetVisibleFacetPnt(0, 0))

        elif k == ord('f'):  # f : Get Facet Vertex

            VisibleFacet = RetrunVisibleFacet(7)

            for Facet in VisibleFacet:
                print("FacetID : ", Facet.FacetID)
                for vertex in Facet.Vertex:
                    print(vertex[0], vertex[1], vertex[2])
                for px in Facet.Pixel:
                    print(px[0], px[1])

        elif k == ord('s'):  # s : Shade Object
            Shade_Mask = np.zeros((im_height, im_width, 3), np.uint8)
            Shade_Img = np.zeros((im_height, im_width,3), np.uint8)

            GetShadeImage(Shade_Img.ctypes, Shade_Mask.ctypes, im_width, im_height, 12, 0, 0, 1280, 720)
            cv2.imshow("Shade_Img", Shade_Img);

        if k == ord('j'):  #j
            print("Color map")

            t0 = time.monotonic()
            GetColorImageNoShade(Color_Img.ctypes, Depth_Mask.ctypes, im_width, im_height, 12, 0, 0, 1280, 720)
            t1 = time.monotonic() - t0
            print("Time elapsed: ", t1)

            cv2.imshow("Color_Img", Color_Img);
            ObjIDMask, FaceIDMask, EdgeMask = cv2.split(Depth_Mask)
            cv2.imshow("Depth Mask", EdgeMask);

        elif k == ord('a'): #a : SetObject
            TypeIndex += 1
            TypeIndex = TypeIndex % 3 + 1
            print("TypeIndex : " + str(TypeIndex))
            SetObject(1, TypeIndex,
                          0.,0.,4000.,
                          0., 0., 0.,
                          1., 1., 0,
                          1000., 1000., 1000.)

        elif k == ord('b'): #b : Get BoundBox
            print("Bound Box")
            MaxBoundBoxNum = 128
            BoundBox = np.zeros(MaxBoundBoxNum*4, np.int32)
            BoundBoxNum = GetBoundBox(BoundBox.ctypes)
            print("BBNum " + str(BoundBoxNum))

            BoundBoxImg = Color_image.copy();
            for i in range(BoundBoxNum):
                x1 = BoundBox[4 * i + 0]
                y1 = BoundBox[4 * i + 1]
                x2 = BoundBox[4 * i + 2]
                y2 = BoundBox[4 * i + 3]
                print("BoundBox : {0} {1} {2} {3}".format(x1, y1, x2, y2))
                cv2.rectangle(BoundBoxImg, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=1, lineType=cv2.LINE_4,  shift=0)
            cv2.imshow("BoundBox", BoundBoxImg);

        elif k == ord('c'):  # c : Set Pos
            PosTest_x += 10
            PosTest_x %= 500
            SetGlobalPosition(PosTest_x,0,0)

        elif k == ord('e'):  # e : Set Att
            AttTest_x += 3
            AttTest_x %= 30
            SetGlobalAttitude(AttTest_x,0,0)

        elif k == ord('f'):  # f : Set Att
            HighlightedID = GetHighLightedObj()
            print("Highlited Obj " + str(HighlightedID))

            if 0 <= HighlightedID:
                print("Att : " + str(GetObjAtt(HighlightedID)))
                print("Color : " + str(GetObjClr(HighlightedID)))
                print("Amp : " + str(GetObjAmp(HighlightedID)))
                print("Pos : " + str(GetObjPos(HighlightedID)))

        elif k == ord('g'): #g
            print("Global Pos:" + str(GetGlobalPos()))
            print("Global Att:" + str(GetGlobalAtt()))
        elif k == ord('h'):  # h
            r,o,f = ReturnDistance(Color_width / 2, Color_Height / 2)
            print("ReturnDistance {0}, {1} , {2}".format(r,o,f) )

        elif k == ord('i'): #i
            SeableObject = np.zeros(128, np.uint8)
            MaskNum = GetSeableObjMask(SeableObject.ctypes)
            for i in range(MaskNum):
                print(SeableObject[i], end=" ")
            print("\n");




        if k == ord('q'):
            break

    cv2.destroyAllWindows()