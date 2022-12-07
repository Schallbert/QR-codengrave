# QR-codengrave

This is a small python application that takes a string, converts
it into a QR-code (with help of @nayuki 's excellent QR-code generator)
and then allows to create CNC toolpaths that enables efficient and quick engraving.

The project is written in Python. The program is not very fast or creates super elegant tool paths,
but special care has to be taken to get the machining time as low as possible.

## Code modules
The application consists of three modules:
- vectorize_qr
- gui
- cam

### vectorize_qr
Contains all classes and helper functions to create a QR-code and convert it into vectors of "black" and "white" fields.
It also defines the machining strategy by selecting the toolpath.
Current implementation only supports inwards-spiral paths.

### gui
The interface of the application to the user. Offers fields to enter the string to convert to QR-code, manages tools for the CAM module,
and displays toolpaths and QR parameters (size, dimensions, etc).

### CAM
TODO