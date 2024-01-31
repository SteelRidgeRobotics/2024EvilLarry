from commands2 import Command
from constants import *
from math import fabs
from subsystems.swerve import Swerve
from wpilib import SmartDashboard, XboxController
from wpimath.filter import SlewRateLimiter
from wpimath.kinematics import ChassisSpeeds

class DriveByController(Command):
    trans_x_slew = SlewRateLimiter(15)
    trans_y_slew = SlewRateLimiter(15)
    rot_slew = SlewRateLimiter(15)

    def __init__(self, swerve: Swerve, controller: XboxController) -> None:
        super().__init__()

        self.swerve = swerve
        self.addRequirements(self.swerve)

        self.controller = controller

    def initialize(self) -> None:
        self.swerve.initialize()        
    
    def execute(self) -> None:
        translation_x = self.controller.getLeftY()
        translation_y = self.controller.getLeftX()
        rotation = self.controller.getRightX()

        translation_y = -self.trans_x_slew.calculate(deadband(translation_y, DriverController.deadband) ** 3)
        translation_x = -self.trans_y_slew.calculate(deadband(translation_x, DriverController.deadband) ** 3)
        rotation = -self.rot_slew.calculate(deadband(rotation, DriverController.deadband) ** 3)

        if self.controller.getBButtonPressed():
            self.swerve.hockey_stop()
            return
        self.swerve.drive(ChassisSpeeds(translation_x * Waffles.k_max_speed, translation_y * Waffles.k_max_speed, rotation * Waffles.k_max_rot_rate), field_relative=True)
    
    def end(self, interrupted: bool) -> None:
        return super().end(interrupted)
    
    def isFinished(self) -> bool:
        return False
    
def deadband(value: float, band: float):
    """
    value is the value we want to deadband
    the band is the abs value the value can not be less than
    """
    # this makes sure that joystick drifting is not an issue.
    # It takes the small values and forces it to be zero if smaller than the 
    # band value
    if fabs(value) <= band:
        return 0
    else:
        return value
