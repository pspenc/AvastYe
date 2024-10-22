import maya.cmds as cmds

import maya.mel as mel

import os

import ART_rigUtils as utils

reload(utils)





class RigCore():



    #RigCore builds up our core components needed to start the rig build. This includes setting up the driver skeleton and building things like the rig settings, and master rig grps

    #These are components that will be needed for every rig



    def __init__(self):



        #create the rig settings node

        self.rigSettings = cmds.group(empty = True, name = "Rig_Settings")

        cmds.setAttr(self.rigSettings + ".tx", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".ty", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".tz", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".rx", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".ry", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".rz", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".sx", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".sy", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".sz", lock = True, keyable = False)

        cmds.setAttr(self.rigSettings + ".v", lock = True, keyable = False)





        #Setup the driver skeleton

        self.createDriverSkeleton()



        #build the core rig components

        self.buildCoreComponents()







    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     

    def createDriverSkeleton(self):



        #there will always be a root bone, so let's duplicate that

        dupe = cmds.duplicate("root", rc = True)[0]

        cmds.select("root", hi = True)

        joints = cmds.ls(sl = True)



        cmds.select(dupe, hi = True)

        dupeJoints = cmds.ls(sl = True)



        driverJoints = []

        for i in range(int(len(dupeJoints))):



            if cmds.objExists(dupeJoints[i]):

                driverJoint = cmds.rename(dupeJoints[i], "driver_" + joints[i])

                driverJoints.append(driverJoint)





        #create a direct connection between the driver and the export joints	

        for joint in driverJoints:

            exportJoint = joint.partition("_")[2]



            try:
                cmds.connectAttr(joint + ".translate", exportJoint + ".translate")
            except:
                print "could not connect translate to driver joint on " + str(exportJoint)

            try:
                cmds.orientConstraint(joint, exportJoint)
            except:
                print "could not orient constrain " + str(exportJoint) + " to driver joint"

            try:
                cmds.connectAttr(joint + ".scale", exportJoint + ".scale")
            except:
                print "could not connect scale to driver joint on " + str(exportJoint)







    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def buildCoreComponents(self):



        #builds the master, the root, and the core rig groups

        #MASTER CONTROL

        masterControl = utils.createControl("circle", 150, "master_anim")



        constraint = cmds.pointConstraint("root", masterControl)[0]

        cmds.delete(constraint)



        cmds.makeIdentity(masterControl, apply = True)

        cmds.setAttr(masterControl + ".overrideEnabled", 1)

        cmds.setAttr(masterControl + ".overrideColor", 18)



        spaceSwitchFollow = cmds.group(empty = True, name = masterControl + "_space_switcher_follow")

        constraint = cmds.parentConstraint("root", spaceSwitchFollow)[0]

        cmds.delete(constraint)



        spaceSwitcher = cmds.group(empty = True, name = masterControl + "_space_switcher")

        constraint = cmds.parentConstraint("root", spaceSwitcher)[0]

        cmds.delete(constraint)	

        cmds.parent(spaceSwitcher, spaceSwitchFollow)

        cmds.parent(masterControl, spaceSwitcher)

        cmds.makeIdentity(masterControl, apply = True)





        #OFFSET CONTROL

        offsetControl = utils.createControl("square", 140, "offset_anim")

        constraint = cmds.pointConstraint("root", offsetControl)[0]

        cmds.delete(constraint)



        cmds.parent(offsetControl, masterControl)

        cmds.makeIdentity(offsetControl, apply = True)

        cmds.setAttr(offsetControl + ".overrideEnabled", 1)

        cmds.setAttr(offsetControl + ".overrideColor", 17)





        #ROOT ANIM

        rootControl = utils.createControl("sphere", 10, "root_anim")

        constraint = cmds.parentConstraint("driver_root", rootControl)[0]

        cmds.delete(constraint)

        cmds.parent(rootControl, masterControl)

        cmds.makeIdentity(rootControl, apply = True)

        cmds.parentConstraint(rootControl, "driver_root")

        cmds.setAttr(rootControl + ".overrideEnabled", 1)

        cmds.setAttr(rootControl + ".overrideColor", 30)



        for attr in [".sx", ".sy", ".sz", ".v"]:

            cmds.setAttr(masterControl + attr, lock = True, keyable = False)

            cmds.setAttr(offsetControl + attr, lock = True, keyable = False)

            cmds.setAttr(rootControl + attr, lock = True, keyable = False)





        #Create the group that will hold all of the control rig components

        rigGrp = cmds.group(empty = True, name = "ctrl_rig")

        cmds.parent(rigGrp, "offset_anim")





        #finish grouping everything under 1 character grp

        controlRigGrp = cmds.group(empty = True, name = "rig_grp")

        cmds.parent(["driver_root", "master_anim_space_switcher_follow"], controlRigGrp)

        cmds.parent("Rig_Settings", controlRigGrp)



        if cmds.objExists("Proxy_Geo_Skin_Grp"):

            cmds.parent("Proxy_Geo_Skin_Grp", controlRigGrp)







        returnNodes = [rigGrp, offsetControl]

        return returnNodes