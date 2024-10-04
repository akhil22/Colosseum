import setup_path
import airsim

import time
import numpy as np
import os
import tempfile
import pprint

# Use below in settings.json with Blocks environment
"""
{
    "SettingsVersion": 1.2,
    "SimMode": "Both",

    "Vehicles": {
        "Car1": {
          "VehicleType": "PhysXCar",
          "X": 0, "Y": 0, "Z": -2
        },
        "Drone1": {
          "VehicleType": "SimpleFlight",
          "X": 0, "Y": 0, "Z": -5,
      "Yaw": 90
        }
  }
}

"""
war_controls = airsim.WarthogControls()

# connect to the AirSim simulator
client_1 = airsim.MultirotorClient(port=41451)
client_1.confirmConnection()
client_1.enableApiControl(True, "Drone1")
client_1.enableApiControl(True, "Drone2")
client_1.armDisarm(True, "Drone1")

client_2 = airsim.WarthogClient(port=41452)
client_2.confirmConnection()
client_2.enableApiControl(True, "Warthog1")
client_2.enableApiControl(True, "Warthog2")
war_controls1 = airsim.WarthogControls()

f1 = client_1.takeoffAsync(vehicle_name="Drone1").join()
f2 = client_1.takeoffAsync(vehicle_name="Drone2").join()
#car_state1 = client_2.getWarthogState(vehicle_name ="Warthog1")
#car_state1 = client_2.getWarthogState()
#print("Car1: Speed %f, Gear %f" % (car_state1.linear_vel, car_state1.angular_vel))

#state1 = client_1.getMultirotorState(vehicle_name="Drone1")
#s = pprint.pformat(state1)
#print("Drone1: State: %s" % s)

# f1 = client_1.moveToPositionAsync(-5, 5, -10, 5, vehicle_name="Drone1")
# car_controls1.throttle = 0.5
# car_controls1.steering = 0.5
# client_2.setCarControls(car_controls1, "Car1")
# print("Car1: Go Forward")
# f1.join()

# time.sleep(2)
"""
airsim.wait_key('Press any key to take images')
# get camera images from the car
responses1 = client_1.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
    airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)], vehicle_name="Drone1")  #scene vision image in uncompressed RGBA array
print('Drone1: Retrieved images: %d' % len(responses1))
responses2 = client_2.simGetImages([
	airsim.ImageRequest("0", airsim.ImageType.Segmentation),  #depth visualization image
	airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)], "Car1")  #scene vision image in uncompressed RGBA array
print('Car1: Retrieved images: %d' % (len(responses2)))


tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

for idx, response in enumerate(responses1 + responses2):
    filename = os.path.join(tmp_dir, str(idx))

    if response.pixels_as_float:
        print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
        airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
    elif response.compress: #png format
        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
    else: #uncompressed array
        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
        img_rgba = img1d.reshape(response.height, response.width, 4) #reshape array to 4 channel image array H X W X 4
        img_rgba = np.flipud(img_rgba) #original image is flipped vertically
        img_rgba[:,:,1:2] = 100 #just for fun add little bit of green in all pixels
        airsim.write_png(os.path.normpath(filename + '.greener.png'), img_rgba) #write to png

airsim.wait_key('Press any key to reset to original state')
"""
#client_1.moveToPositionAsync(0, 0, -10, 5, vehicle_name="Drone1").join()
f3 = client_1.moveByRollPitchYawrateZAsync(0, 0, 3.0, -3, 200, vehicle_name="Drone1")
f4 = client_1.moveByRollPitchYawrateZAsync(0, 0, -3.0, -3, 200, vehicle_name="Drone2")
#client_1.moveToPositionAsync(0, 1, -10, 5, vehicle_name="Drone2").join()
war_controls.angular_vel = 1
client_2.setWarthogControls(war_controls, vehicle_name="Warthog1")
client_2.setWarthogControls(war_controls, vehicle_name="Warthog2")
while True:
    # get state of the car
    #car_state = client_2.getWarthogState(vhicle_name="Warthog1")
    #print("Speed %d, Gear %d" % (car_state.linear_vel, car_state.angular_vel))
    war_controls.linear_vel = 1
    war_controls.angular_vel = 1
    client_2.setWarthogControls(war_controls, vehicle_name="Warthog1")
    client_2.setWarthogControls(war_controls, vehicle_name="Warthog2")
    # set the controls for car
   # car_controls.throttle = 0.2
   # car_controls.steering = 1
   # client_2.setCarControls(car_controls)

    # let car drive a bit
    time.sleep(100)

client_1.armDisarm(False, "Drone1")
client_1.reset()
client_2.reset()

# that's enough fun for now. let's quit cleanly
client_1.enableApiControl(False, "Drone1")
client_2.enableApiControl(False, "Warthog1")
