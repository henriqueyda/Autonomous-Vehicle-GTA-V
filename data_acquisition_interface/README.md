# Data Acquisition Interface

This folder contains the source code and instructions to run the interface developed to collect training data inside GTA V game. This interface captures real-time images displayed on screen at 10 fps rate using the ImageGrab module from Python library Pillow. Driving data is collected with the PyGame library that reads the joystick and triggers commands from a controller handled by a human driver. In-game modifications named ScriptHookV and Native TrainerSpeed are used to collect speed data. A diagram of the system is shown below:

<img src="https://github.com/henriqueyda/Autonomous-Vehicle-GTA-V/blob/master/images/data_acquisition_interface.png" width=600>

Instructions to run this program are the following:

**Preparing System**
- Create file Speed.txt in (D:) directory
- Insert Speed.asi file in GTA V folder (in Steam usually is: C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V)
- Download ScriptHookV.dll mod library and follow instructions in http://www.dev-c.com/gtav/scripthookv
- Insert x360ce in GTA V folder
- Create a folder named "Data" in same directory of "acquisition_interface.py" file

**Starting Mod**
- Get into a car inside game
- Press F4 to execute program 
- The text "Starting" will appear on screen
- Press key NUM_9 to enable speed values recording 
- The text "Speed values recording enabled" will appear on screen

**Data Acquisition Interface Execution**
- Each key execute the described function
    - Keys:
        - o: Starts recording
        - p: Stops current recording and save data
        - z: Stops program execution
        - 9: Stops recording without saving data
- Mod configuration:
    - Keys:
        - NUM_1: Decreases counter that fast-foward time in one second
        - NUM_2: Increases counter that fast-foward time in one second
        - NUM_8: Turns on/off speed values printing on screen
        - NUM_9: Turns on/off speed recording in Speed.txt file