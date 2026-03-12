# Drona 🚁

Drona is a customized, open-source [ROS](https://www.ros.org)-based framework designed to provide user-friendly tools for controlling [PX4](https://px4.io)-powered drones. 

Built as a specialized fork of the powerful [Clover platform](https://github.com/CopterExpress/clover), Drona is optimized for custom hardware integrations and edge-computing applications. It can be installed as a standard ROS Noetic package or run via our preconfigured Raspberry Pi image.

## Features
* **ROS Noetic** integration out-of-the-box.
* **Computer Vision Ready:** Pre-configured with OpenCV and `aruco_pose` for marker-assisted indoor navigation.
* **Hardware Interfacing:** Built-in periphery drivers for GPIO, LED strips, and additional sensors.
* **Autonomous Flight API:** Simplified Python wrappers for offboard MAVLink control.

## Getting Started
*(Add your own instructions here later on how users can install Drona onto their Raspberry Pi or Jetson, or how to connect it to your specific Arduino hardware package).*

## Acknowledgements & Attribution
Drona is a modified fork of the **[COEX Clover](https://github.com/CopterExpress/clover)** project. We are incredibly grateful to the COEX team and the open-source robotics community for building the robust foundation that makes this project possible.

## License
* **Source Code:** The Drona framework source code (derived from Clover) is released under the **MIT License**. You are free to use, modify, and distribute this software in both commercial and non-commercial projects, provided the original copyright notice is included.
* **Documentation:** Any inherited documentation located in the `docs/` directory is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).