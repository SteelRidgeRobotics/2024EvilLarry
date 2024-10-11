from commands2 import Subsystem
from constants import Constants
import ntcore
import math
from subsystems.drivetrain import Drivetrain
from wpimath.kinematics import ChassisSpeeds
from wpilib import DriverStation
import wpilib

class AutoAlign(Subsystem):

    def __init__(self):

        self.ntInstance = ntcore.NetworkTableInstance.getDefault()
        # self.addRequirements(self.drivetrain)

    def calculateDegrees(self):

        # read from LimeLight
        # know which alliance
        # confirm correct tag
        # calculate the angle to speaker
        # ! calculate the hypot for distance
        # convert degrees to rotations per constant of gear ratio
        # return number of rotations
        # ! calculate the rev speed

        """
        To do

        Set id priority on LimeLight (In progress)

        """
        table = self.ntInstance.getTable("limelight")
        # NetworkTables.getTable("LimeLight").putNumber('priorityid',4) I have a topic on this pending in Chief Delphi so I'll know how to write this.
        targetOffsetAngle = table.getNumber("ty",0.0)
        tagId = table.getNumber("tid", 0)
        wpilib.SmartDashboard.putNumber("ID", tagId)
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            self.ntInstance.getTable("LimeLight").putNumber('priorityid', Constants.LimeLight.REDSPEAKERID)

            wpilib.SmartDashboard.putString("ID Priority", "Red (4)")
            if tagId != Constants.LimeLight.REDSPEAKERID: #need ids for blue or red and also check that
                return 0 
            

        elif DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            self.ntInstance.getTable("LimeLight").putNumber('priorityid', Constants.LimeLight.BLUESPEAKERID)
            wpilib.SmartDashboard.putString("ID Priority", "Blue (7)")

            if tagId != Constants.LimeLight.BLUESPEAKERID: #need ids for blue or red and also check that
                return 0
        
        
       
        angleToTargetRadians = self.getAngleToTargetInRadians(targetOffsetAngle)
        distanceToGoal = self.getDistanceToTargetInches(angleToTargetRadians)
        degrees = self.getDegreesToSpeaker(distanceToGoal)
        rotations = (degrees * Constants.Swivel.GEAR_RATIO) / 360

        wpilib.SmartDashboard.putNumber("rotations", rotations)
        #return rotations

    def getAngleToTargetInRadians(self, targetOffsetAngle):
        angleToGoalDegrees = Constants.LimeLight.k_mount_angle  + targetOffsetAngle
        angleToGoalRadians = angleToGoalDegrees * (3.14159 / 180.0)

        wpilib.SmartDashboard.putNumber("angle to target (rad)", angleToGoalRadians)
        return angleToGoalRadians
    
    # Would only be used if we want to adjust velocity of launcher or determine if we are too close or far
    def getDistanceToTargetInches(self, angleToTargetRadians):
        distanceToTargetInches=(Constants.LimeLight.k_tag_height - Constants.LimeLight.k_mount_height)/math.tan(angleToTargetRadians)

        wpilib.SmartDashboard.putNumber("D", distanceToTargetInches)
        return distanceToTargetInches
    
    def getDegreesToSpeaker(self, distance):
        if distance <= 0.0:
            return Constants.Swivel.MAX_ANGLE
        degrees = math.degrees(math.atan(Constants.LimeLight.k_target_height/distance))
        if degrees > Constants.Swivel.MAX_ANGLE:
            return Constants.Swivel.MAX_ANGLE
        
        wpilib.SmartDashboard.putNumber("Degrees to speaker", degrees)
        return degrees


    def isFinished(self):

        return False
