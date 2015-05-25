# Arduino library for 4D Systems's uCam-II TTL Camera

This is an Arduino library for 4D System's uCam-II http://4dsystems.com.au/product/uCAM_II/

**NOTE!** This library assumes your camera is on the hardware UART connection and you will debug via the softwareSerial connection

## Todo 
- Checksum check on each received packet
- More error detection and termination
- Timeout/return if no response received
- Perhaps there's a way to not require the memory buffer and simply stream from the camera, unsure. Seems to be a performance tradeoff
- Pass a pointer for the waitBytes instead of a copy of the bytes

## Tune it
- uCamII.h ```#define UCAMII_BUF_SIZE 24``` , change this on larger processors or smaller on memory lacking processors (this is the size without the packet headers)
- uCamII.cpp set the various #define's for what you require, such as _INITIAL_COMMAND


### Overview

The library communicates with the µCam-II and sets all parameters, each chunk of data is returned via UCAMII::getData and waits in a memory buffer, ICAMII:getData returns the number of bytes that are in the buffer (maximum of UCAMII_BUF_SIZE)

This library built from the official datasheet http://www.4dsystems.com.au/productpages/uCAM-II/downloads/uCAM-II_datasheet_R_1_4.pdf


### Example code 

Code that outputs the hex bytes to a debug interface on SoftwareSerial (SoftwareSerial not required, example only)

```
#include <uCamII.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(3, 2); // RX, TX (or tx on the end and rx on the end)

void setup() {
  mySerial.begin(57600);
  Serial.begin(57600);
  mySerial.println("trying ..");


  UCAMII camera;
  short x = 0;
  int bytes;

  // unComment the #define cameraDebugSerial in uCamII.cpp 
  // and set the debug output interface below
  // camera.setDebug(&mySerial);

  if (camera.init()) {
    camera.takePicture();
    mySerial.print("Image size: ");
    mySerial.println(camera.imageSize, DEC);
    mySerial.print("number of packages: ");
    mySerial.println(camera.numberOfPackages(), DEC);

    while ( bytes = camera.getData() ) {
      for (x = 0; x < bytes; x++) {
        mySerial.print("0x");
        mySerial.print(camera.imgBuffer[x], HEX);
        mySerial.print(" ");
      }
      mySerial.println("");
    }
    mySerial.println("done downloading");

  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
```

Included also is a python script to convert the dbeug output bytes back to a JPEG, save the output of the terminal (make sure no pieces are missing, compare last byte values etc) to a text file, then
```
python ./hex-to-bytes.py < output.txt
``` 
and you should have a output.jpeg file

or for example
```
echo "0x01 0x02 0x03"| python ./hex-to-bytes.py
```

