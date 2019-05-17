from pyrobot.brain import Brain

import math

import cv2
from matplotlib import pyplot as plt
import numpy as np
import config
import setup
#import imutils
import segmentLinesAndSymbolsFromImage
import consignaFromSegmentation


# Autores:
# Luciano Garcia Giordano - 150245
# Gonzalo Florez Arias - 150048
# Salvador Gonzalez Gerpe - 150044

# Record video
# outIm = cv2.VideoWriter('./videos/demoBolaImagen.mp4', cv2.VideoWriter_fourcc(*'XVID'), 25, (320, 240))
# outSeg = cv2.VideoWriter('./videos/demoBolaSegm.mp4', cv2.VideoWriter_fourcc(*'XVID'), 25, (320/4, 240/4))


class BrainTestNavigator(
    Brain
    ):

    NO_FORWARD = 0
    SLOW_FORWARD = 0.1
    MED_FORWARD = 0.5
    FULL_FORWARD = 1.0

    NO_TURN = 0
    MED_LEFT = 0.5
    HARD_LEFT = 1.0
    MED_RIGHT = -0.5
    HARD_RIGHT = -1.0
    
    NO_ERROR = 0

    # def move(self,a,b):
	#     pass
    
    def setup(self):
        print 'setup'

        self.targetDistance = 40.0
        self.targetX = setup.imageWidth // 2
        self.targetY = 120
        self.angularKp = 3.0 # turns more the higher
        self.angularKd = 15.0 # turns more slowly the lower

        self.linearKp = 0.08
        self.linearKd = 0.05

        self.state = 'findBall'

        self.states = {
            'findBall': {
                'action': self.waitStopped
            },
            'followBall': {
                'action': self.followBall
            }
        }

        self.ballPosition = {}

        self.previousData = {
            "angle": 0,
            "distance": 0
        }

    def waitStopped(self, hasBall, ballDistance, ballPosition):
        self.move(0.0, 0.0)

    def followBall(self, hasBall, ballDistance, ballPosition):
        angularDeviation = (ballPosition['x'] - self.targetX)/self.imageWidth

        # linearDeviation = ballDistance - self.targetDistance
        # print angularDeviation

        turn = 0.0
        speed = 0.6
        if (hasBall):
            # if math.fabs(angularDeviation) > 0.2:
            # turn = -self.Kp*angularDeviation
            diffAngularDev = math.fabs(angularDeviation) - math.fabs(self.prevAngularDeviation)
            if diffAngularDev == 0.0:
                diffAngularDev = 1.1
            turn = (-self.angularKp*angularDeviation)/math.fabs(self.angularKd*diffAngularDev)
            # self.Kp += 0.1
            # print "Kp is:", self.Kp
            # print "turn is:", turn
            if (turn < -2.0): 
                turn = -2.0
            elif (turn > 2.0):
                turn = 2.0
            # else:
            #     turn = 0.0

            # if math.fabs(linearDeviation) > 5.0:
            #     diffLinearDeviation = math.fabs(linearDeviation) - math.fabs(self.prevLinearDeviation)
            #     if diffLinearDeviation == 0.0:
            #         diffLinearDeviation = 5.0
            #     speed = (self.linearKp*linearDeviation)/math.fabs(self.linearKd*diffLinearDeviation)
            #     # speed = (self.linearKp*linearDeviation)
            #     # print speed
            #     if (speed < -1.0): 
            #         speed = -1.0
            #     elif (speed > 1.0):
            #         speed = 1.0
            # else:
            #     speed = 0.0
            
        
        # if ballPosition['x'] > self.targetX:
        #     # Go right
        #     turn = -1.5
        # elif ballPosition['x'] < self.targetX:
        #     # go left
        #     turn = 1.5

        # speed = 0.0
        # turn = 0.0
        # if ballDistance < self.targetDistance:
        #     speed = -0.7
        # elif ballDistance > self.targetDistance:
        #     speed = 0.7


        self.prevAngularDeviation = angularDeviation

        self.move(speed, turn)

    def followLine(self, hasBall, ballDistance, ballPosition):
        if (hasLine):
            Kp = 0.6*math.fabs(lineDistance)
            Kd = (math.fabs(lineDistance) - math.fabs(self.prevDistance))
            # print "Kd sale: ",Kd

            # self.Ki = self.Ki + lineDistance
            if Kd == 0:
                turnSpeed = self.previousTurn
            else:
                turnSpeed =  5*((Kp * lineDistance)/((searchRange - math.fabs(Kd)) * searchRange))
            
            turnSpeed = min(turnSpeed, 1)

            # The sharper the turn, the slower the robot advances forward
            # forwardVelocity = min(((searchRange - math.fabs(Kd)) * searchRange) / 180, 1)
            parNormalizacion = 100
            parA = 3.5
            parB = -2.8
            # Kd = Kd*5
            forwardVelocity = max(min(parA*((searchRange - 0.99*math.fabs(Kd)) * searchRange)**2 / (parNormalizacion**2) + parB*((searchRange - 0.99*math.fabs(Kd)) * searchRange) / (parNormalizacion), 1),0)

            maxSpeed = 1.0 if (front > 1.0 and left > 0.5 and right > 0.5) else 0.2
            if forwardVelocity > maxSpeed:
                forwardVelocity = maxSpeed

            self.previousTurn = turnSpeed

            # print "vel:",forwardVelocity,"turn:",turnSpeed, "Kd:",Kd
            self.move(forwardVelocity,turnSpeed)

        # elif self.firstStep:
        #     self.firstStep = False
        else:

            # if we can't find the line we just go back, this isn't very smart (but definitely better than just stopping
            turnSpeed = 0.8 if self.previousTurn > 0 else -0.8
            if self.lastTurn != 0:
                self.move(-0.2, -(self.lastTurn))
                self.lastTurn = 0
            else:
                self.move(-0.2,turnSpeed)
                self.lastTurn = turnSpeed

        self.prevDistance = lineDistance

    def transitionState(self, hasBall, ballDistance, ballPosition):

        previousState = self.state
        
        if self.state is 'findBall':
            if hasBall:
                self.prevAngularDeviation = 20.0
                # self.prevLinearDeviation = 10.0
                self.state = 'followBall'

        elif self.state is 'followBall':
            if not hasBall:
                self.state = 'findBall'


        # if previousState != self.state:
        #     print "new state:", self.state
        #     self.printSummary(previousState, hasBall, ballDistance, ballPosition)
            
    def printSummary(self, previousState, hasBall, ballDistance, ballPosition):
        print "Data for new state decision is", previousState, hasBall, ballDistance, ballPosition        
    
    def evaluateBall(self):
        #print 'Sigo vivo'
        ret, im = setup.capture.read()

        imHSV = im[0::setup.shrinkFactor,0::setup.shrinkFactor,:]
        imHSV = cv2.cvtColor(imHSV, cv2.COLOR_BGR2HSV)
        imHS = imHSV[:,:,(0,1)]

        paleta = setup.paleta
        segImg = setup.segImg

        def predictRow(i):
            segImg[i] = setup.segmenter.predict(imHS[i])[:, np.newaxis]

        [predictRow(i) for i in range(imHS.shape[0])]
        
        showImage = np.zeros(segImg.shape, dtype='uint8')
        showImage[segImg==0] = 1

        # print showImage.shape
        segImg1 = cv2.erode(showImage, None, dst=showImage, iterations=1) # don't touch this
        # print showImage.shape
        # print segImg1.shape
        # segImg1 = cv2.dilate(segImg1, None, iterations=2)
        # segImg1 = cv2.dilate(showImage, None, dst=showImage, iterations=2)

        # whereIsObject = np.all(segImg1 == 2, axis=-1)
        # print segImg1.shape
        segImgLine = segImg1[int(self.imageHeight*0.8),:]
        whereIsObject = np.all(segImgLine == 1, axis=-1)
        # print whereIsObject
        whereIsObjectPositions = np.where(whereIsObject==True)
        # print whereIsObjectPositions[0]
        
        if whereIsObjectPositions[0].shape[0] != 0:
            minx = np.min(whereIsObjectPositions)
            maxx = np.max(whereIsObjectPositions)
            self.size = maxx - minx
            self.ballPosition['x'] = (maxx + minx) / 2.0
            if self.size == 0:
                self.size = 1.0
            hasBall = True

            dist0 = 20.0 # put fixed distance to the object here
            # diameter = 6.8 # put size of object here
            # paramF = 279.26
            # paramF = 64.0

            # dist = (paramF*diameter) / self.size

            size0 = 26

            dist = (size0*dist0)/self.size

            # print "minmax", minx, maxx, dist


            # print "paramF should be: ", (dist1*self.size)/diameter, "distance is: ", dist
        else:
            hasBall = False
            self.size = 30.0
            dist = -1.0

        

	    # print "imagen", segImg
        # cv2.imshow("Segmentacion Euclid",cv2.cvtColor(segImg,cv2.COLOR_RGB2BGR))
        # cv2.imshow("Segmentacion Euclid",showImage*255)
        
        
        # # Record video
        # outFrame = np.repeat((showImage*255)[:, :, np.newaxis], 3, axis=2)[:,:,:,0]
        # outSeg.write(outFrame)
	    
        
        
        # print outFrame.shape
        
        #print segImg[0][0][0]
    
        # cv2.waitKey(1)

        ballPosition = self.ballPosition


        return hasBall, dist, ballPosition


    def step(self):
        arrow, line, imageOnPaleta = segmentLinesAndSymbolsFromImage.fetchImageAndSegment(setup)

        speed, rotation, numberOfExits = consignaFromSegmentation.calculateConsignaFullProcess(line, arrow, imageOnPaleta, self.previousData, setup)
        # print speed, rotation
        if speed != None and rotation != None:
            # print 'sending command', speed, rotation
            self.move(speed, rotation)
        else:
            self.move(0,0)

        shapeName = consignaFromSegmentation.predictShapeIfShape(arrow, setup)
        if (not (shapeName == None or shapeName == 'touches edges' or shapeName == 'nothing')) and numberOfExits <= 1:
            print(shapeName)
            cv2.putText(imageOnPaleta,shapeName,(10,160//setup.segmentedImageShrinkFactor), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255,255,255),1,cv2.LINE_AA)

        # # Changes of state
        # self.transitionState(arrow, line, shapeName, numberOfExits)

        # # Follow state
        # self.states[self.state]['action'](arrow, line, shapeName, numberOfExits)

        if setup.drawAndRecordSchematicSegmentation:
            setup.schematicsVideoOutput.write(cv2.cvtColor(imageOnPaleta, cv2.COLOR_RGB2BGR))
    
def INIT(engine):
    assert (engine.robot.requires("range-sensor") and engine.robot.requires("continuous-movement"))
    return BrainTestNavigator('BrainTestNavigator', engine)




# brain = BrainTestNavigator()
# brain.setup()
# while(True):
#    brain.step()
