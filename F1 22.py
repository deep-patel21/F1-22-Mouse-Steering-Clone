"""     F1 22 Script
	Original: Berkay Topuz (open-sourced on Steam workshop)
	Edited: Deep Patel (for personal usage)
	Usage: enables virtual game controller software to emulate a physical controller through a PC mouse,
       	       rendering the mouse a capable input device to steer a car in the F1 racing video game.
	       
	Adjustments: If sensitivity needs to be adjusted, locate the mouse_sensitivity and mouse_throttle_sensitivity
             	     in 'Global Vars' or use input DPI adjustments on your gaming mouse.
		   
	Prerequisites: Download vJoy (virtual joystick) and copy the settings in README.md. 
               	       Also download FreePIE to run the Python script.                            """

if starting:  
    #Range of 32-bit integers
    int32_max = (2 ** 14) - 1
    int32_min = (( 2** 14) * -1) + 1
	
    #Definition of CONSTANTS
    thread_exe_interval = 5
    user_throttle_sens = 50
    user_steering_sens = 10
    user_deadzone_value = 0.2  #to simulate controller deadzone (area of zero input)
    user_center_reduction = 1.0 #scales down inputs to a percentage of max range
	
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = user_center_reduction #no reduction is applied, values between [0.01 (HI reduction), 1.00 (LO reduction)] accepted	

    #DO NOT TOUCH. These are essential to access vJoy even if all axes are not in use.
    #8-axis configuration on vJoy (virtual joystick)
    #Initialized to minimum possible value of 32-bit integer
    v = vJoy[0]
    vjoy_axes_instances = 8
    #Offers roll, pitch, and yaw functionality	
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min) * vjoy_axes_instances

    #Global Vars 	
    #Models various steering and throttle dimensions	
    global mouse_sensitivity, mouse_throttle_sensitivity
    mouse_throttle_sensitivity = user_throttle_sens #This can be altered at top for input: Throttle Sensitivity
    mouse_sensitivity = user_steering_sens #This can be altered at top for input: Steering Sensitivity
    global throttle, throttle_max, throttle_min
    throttle_max = int32_max
    throttle_min = int32_min
    throttle = throttle_min 
    global steering, steering_max, steering_min, steering_center_reduction   
		
    system.setThreadTiming(TimingTypes.HighresSystemTimer) 
    system.threadExecutionInterval = thread_exe_interval	
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max

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
deadzone = user_deadzone_value
if abs(mouse.deltaX) > deadzone:
	steering = steering + (float(mouse.deltaX) * mouse_sensitivity * steering_center_reduction)
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
