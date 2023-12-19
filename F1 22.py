if starting:    
    system.setThreadTiming(TimingTypes.HighresSystemTimer) 
    system.threadExecutionInterval = 5	
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max

    #Range of 32-bit integers
    int32_max = (2 ** 14) - 1
    int32_min = (( 2** 14) * -1) + 1

    #8-axis configuration on vJoy (virtual joystick)
    #Initialized to minimum possible value of 32-bit integer
    v = vJoy[0]
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min,) * 8

    #Global Vars 	
    #Models various steering and throttle dimensions	
    global mouse_sensitivity, mouse_throttle_sensitivity
    mouse_throttle_sensitivity = 50 #This can be altered for input: Throttle Sensitivity
    mouse_sensitivity = 10 #This can be altered for input: Steering Sensitivity
    global throttle, throttle_max, throttle_min
    throttle_max = int32_max
    throttle_min = int32_min
    throttle = throttle_min 
    global steering, steering_max, steering_min, steering_center_reduction   
	
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = 1.0

#Reset conditions for steering and throttle values
if mouse.wheelUp:
	steering = 0.0
	throttle = 0
if keyboard.getKeyDown(Key.Return):
	steering = 0.0
	throttle = 0

#Registers X and Y movements from the mouse to manipulate steering and throttle values
#The min to max range is determined as per game requirements to scale movements accordingly

#X direction of movement controls steering wheel left and right
steering = steering + (float(mouse.deltaX) * mouse_sensitivity)
if steering > steering_max:
    steering = steering_max
elif steering < steering_min:
    steering = steering_min
v.x = int(round(steering)) #value is mapped to x-axis on virtual controller

#Y direction of movement controls gradual application of gas pedal or brake pedal
throttle = throttle + (float(-mouse.deltaY) * mouse_throttle_sensitivity)
if throttle > throttle_max:
    throttle = throttle_max
elif throttle < steering_min:
    throttle = throttle_min
v.y = int(round(throttle)) #value is mapped to y-axis on virtual controller

#Mapping mouse buttons to buttons on the virtual controller
v.setButton(0,int(mouse.leftButton))
v.setButton(1,int(mouse.rightButton))
v.setButton(2,int(mouse.middleButton))

#Outputs values to console to test if mouse movement changes values as expected
diagnostics.watch(v.x)
diagnostics.watch(v.y)
