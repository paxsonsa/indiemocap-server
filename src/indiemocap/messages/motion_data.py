# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" motion_data.py
MotionData Message Handler

Author: Andrew Paxson
"""
from indiemocap import messaging
from indiemocap import message_types

class MotionDataMessage(messaging.Message):

    mtype = message_types.MotionData

    def __init__(self, yaw, pitch, roll, accX, accY, accZ):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.accX = accX
        self.accY = accY
        self.accZ = accZ

class MotionDataHandler(messaging.MessageHandler):

    mtype = message_types.MotionData
    messageKlass = MotionDataMessage


    # The byte structure for the 'struct' module
    # 6 Doubles (8 bytes each) representing: yaw, pitch, roll, x, y, z
    byte_structure = '6d'
    name_byte_mapping = [
        "yaw",
        "pitch",
        "roll",
        "accX",
        "accY",
        "accZ"
    ]
