//Libraries
#include <Wire.h>
#include <string.h>
#include <Adafruit_PWMServoDriver.h>

//weight sensor
#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

// Create a PWM driver object
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define LED_PIN 8
#define LED1_PIN 9

//Define the pins
#define S0 2
#define S1 3
#define S2 4
#define S3 5
#define sensorOut 6

//buzzer to arduino pin 7
const int buzzer =7;

//weight sensor pin:
const int HX711_dout = 11; //mcu > HX711 dout pin
const int HX711_sck = 10; //mcu > HX711 sck pin

// Define the number of servos connected to the PCA9685 driver
const int numServos = 3;

//weight sensor stuff
//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

// Define thresholds for each color
//const int redThreshold = 140;  // Adjust as needed
//const int greenThreshold = 140;  // Adjust as needed
//const int blueThreshold = 140;  // Adjust as needed
//const int yellowThreshold = 10000;  // Adjust as needed

// Define the servo details (channel, min pulse width, max pulse width)
const int servoChannels[numServos] = {0, 1, 2}; // Change this to match the channels connected to your servos
const int servoMin[numServos] = {150, 150, 150}; // Adjust according to your servo's min pulse width
const int servoMax[numServos] = {600, 600, 600}; // Adjust according to your servo's max pulse width

//Inputs
int x = 0;
int y = 0;
int z = 0;
int alarm = 0;
char colour;
char right_colour = 'R'; //starting colour is red

void setup() 
{
  Serial.begin(9600);
  // Initialize the PWM driver
  pwm.begin();

  // Set PWM frequency (default is 50Hz)
  pwm.setPWMFreq(60);  // Analog servos typically operate at 50Hz or 60Hz

  //Pin mode
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED1_PIN, OUTPUT);
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED_PIN, LOW);

  //Pins for TCS3200
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);

  // Set buzzer - pin 9 as an output
  pinMode(buzzer, OUTPUT);
  
  // Setting frequency-scaling to 20%
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);
  
  Serial.begin(9600);

  Serial.begin(9600); delay(10);
  Serial.println();
  Serial.println("Starting...");


  LoadCell.begin();
 // LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
  float calibrationValue; // calibration value (see example file "Calibration.ino")
  //calibrationValue = 696.0; // uncomment this if you want to set the calibration value in the sketch
#if defined(ESP8266)|| defined(ESP32)
  //EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
#endif
  EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom

  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
    Serial.println("Startup is complete");
    
  }
  
  

}

//weight sensor int
const float thresholdWeight = -0.1;
bool thresholdExceeded = false;
int N = 0;
int Y = 0;
int Z = 0;
int T = 0;

void loop() 
{

  char RxedByte = 0;

 if (Serial.available()) 
    {
      
      RxedByte = Serial.read();    
       
      switch(RxedByte)
      {
        case 'A':  digitalWrite(8,HIGH);
                   delay(2000);
                   digitalWrite(8,LOW);
                   delay(2000);
    while(y < 4)
    {
      int redFrequency = readFrequency(LOW, LOW);   // Red filtered photodiodes
      int greenFrequency = readFrequency(HIGH, HIGH); // Green filtered photodiodes
      int blueFrequency = readFrequency(LOW, HIGH);  // Blue filtered photodiodes
      int clearFrequency = readFrequency(HIGH, LOW); // Clear (no filter) photodiodes

      // Print frequencies for debugging
      Serial.print("Red: ");
      Serial.print(redFrequency);
      Serial.print(" Green: ");
      Serial.print(greenFrequency);
      Serial.print(" Blue: ");
      Serial.print(blueFrequency);
      Serial.print(" Clear: ");
      Serial.println(clearFrequency);

      // Classify colors based on frequencies
      colour = detectColor(redFrequency, greenFrequency, blueFrequency, clearFrequency);
      delay(1000); // Delay for stability

      while(colour == 'U')
      {
      int redFrequency = readFrequency(LOW, LOW);   // Red filtered photodiodes
      int greenFrequency = readFrequency(HIGH, HIGH); // Green filtered photodiodes
      int blueFrequency = readFrequency(LOW, HIGH);  // Blue filtered photodiodes
      int clearFrequency = readFrequency(HIGH, LOW); // Clear (no filter) photodiodes

      // Print frequencies for debugging
      Serial.print("Red: ");
      Serial.print(redFrequency);
      Serial.print(" Green: ");
      Serial.print(greenFrequency);
      Serial.print(" Blue: ");
      Serial.print(blueFrequency);
      Serial.print(" Clear: ");
      Serial.println(clearFrequency);

      // Classify colors based on frequencies
      colour = detectColor(redFrequency, greenFrequency, blueFrequency, clearFrequency);
      delay(1000); // Delay for stability
      }

      //red, yellow, green, blue
      if(colour == right_colour)
      {
        digitalWrite(LED1_PIN, HIGH);
        digitalWrite(LED_PIN, LOW);
        moveServo(2,110);
        delay(1500);
        moveServo(2,0);
        tone(buzzer, 1000); // Send 1KHz sound signal...
        delay(500);        // ...for 1 sec
        noTone(buzzer);     // Stop sound...
        delay(500); 
         y = y + 1;
        if(right_colour == 'R')
        {
          right_colour = 'Y';
        }
        else if(right_colour == 'Y')
        {
          right_colour = 'G';
        }
        else if(right_colour == 'G')
        {
          right_colour = 'B';
        }
        else if(right_colour == 'B')
        {
          right_colour = 'R';
        }
      }
      else if(colour != right_colour)
      {
        digitalWrite(LED1_PIN, LOW);
        digitalWrite(LED_PIN, HIGH);
        alarm = 0;
        while (alarm < 3)
        {
          tone(buzzer, 1000); // Send 1KHz sound signal...
          delay(500);        // ...for 1 sec
          noTone(buzzer);     // Stop sound...
          delay(500); // Send 1KHz sound signal...
          alarm = alarm + 1;
        }
 
        delay(3000); //for user to take out capsule
        digitalWrite(LED_PIN, LOW);
        delay(3000); //for user to put in the capsule
        int redFrequency = readFrequency(LOW, LOW);   // Red filtered photodiodes
        int greenFrequency = readFrequency(HIGH, HIGH); // Green filtered photodiodes
        int blueFrequency = readFrequency(LOW, HIGH);  // Blue filtered photodiodes
        int clearFrequency = readFrequency(HIGH, LOW); // Clear (no filter) photodiodes

        // Print frequencies for debugging
        Serial.print("Red: ");
        Serial.print(redFrequency);
        Serial.print(" Green: ");
        Serial.print(greenFrequency);
        Serial.print(" Blue: ");
        Serial.print(blueFrequency);
        Serial.print(" Clear: ");
        Serial.println(clearFrequency);

        // Classify colors based on frequencies
        colour = detectColor(redFrequency, greenFrequency, blueFrequency, clearFrequency);
        delay(1000); // Delay for stability

      if(colour == right_colour)
      {
        digitalWrite(LED1_PIN, HIGH);
        digitalWrite(LED_PIN, LOW);
        moveServo(2,110);
        delay(1500);
        moveServo(2,0);
        tone(buzzer, 1000); // Send 1KHz sound signal...
        delay(500);        // ...for 1 sec
        noTone(buzzer);     // Stop sound...
        delay(500); 
         y = y + 1;
        if(right_colour == 'R')
        {
          right_colour = 'Y';
        }
        else if(right_colour == 'Y')
        {
          right_colour = 'G';
        }
        else if(right_colour == 'G')
        {
          right_colour = 'B';
        }
        else if(right_colour == 'B')
        {
          right_colour = 'R';
        }
      }
     }
    
    }
    digitalWrite(LED1_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    y = 0;
    break;
//----------------------------------------------------------------------------
        case 'B':  digitalWrite(8,HIGH);
                   delay(2000);
                   digitalWrite(8,LOW);
                   delay(2000);
    // Move servo 1 to 0 degrees
    moveServos(0, 180);
    delay(700); // Wait for 1 second
    // Move servo 1 to 180 degrees
    moveServos(0, 0);
    delay(1000); // Wait for 1 second
  
    // Move servo 2 to 0 degrees
    moveServos(1, 180);
    delay(700); // Wait for 1 second
    // Move servo 2 to 180 degrees
    moveServos(1, 0);
    delay(700); // Wait for 1 second
    //Change State
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(LED1_PIN, HIGH);
    alarm = 0;
    
    while(alarm < 2)
    {
      tone(buzzer, 1000); // Send 1KHz sound signal...
      delay(1000);        // ...for 1 sec
      noTone(buzzer);     // Stop sound...
      delay(1000);        // ...for 1sec
      alarm ++;
    }
    x=1;
                   break;
        default:
                   break;
      }//end of switch()
    }//endof if 

 

  //weight sensor code
  static boolean newDataReady = 0;
  const int serialPrintInterval = 2000; //increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;

  // get smoothed value from the dataset:
 
  if (newDataReady && x==1) {    
    if (millis() > t + serialPrintInterval && Z==0) {
      
      float i = LoadCell.getData();
      Serial.print("Load cell output val: ");
      Serial.println(i);
      newDataReady = 0;
      t = millis();

      if (i >= thresholdWeight && T==0  ) {
        digitalWrite(8,HIGH);
        delay(500);
        digitalWrite(8,LOW);
        delay(500);

        N += 1;
        if (N == 5)
        {
          Serial.println("Not eaten");
          N = 0;
          alarm = 0;
          while(alarm < 3)
          {
            tone(buzzer, 1000); // Send 1KHz sound signal...
            delay(1000);        // ...for 1 sec
            noTone(buzzer);     // Stop sound...
            delay(1000);        // ...for 1sec
            alarm ++;
          }
          
        }
      }
      else if (i < -42 && !thresholdExceeded) {
        Serial.println("Eaten");
        digitalWrite(8,HIGH);
        delay(500);
        digitalWrite(8,LOW);
        delay(500);
        digitalWrite(8,HIGH);
        delay(500);
        digitalWrite(8,LOW);
        delay(500);


        
        thresholdExceeded = true;
        T=1;
      
        }
      else if (i < -42 && T==1  ) {
         Y += 1;
        if (Y == 10){
        Serial.println("put the cup back");
        Y=0;
        alarm = 0;
        
        while(alarm < 2)

          {
            tone(buzzer, 1000); // Send 1KHz sound signal...
            delay(1000);        // ...for 1 sec
            noTone(buzzer);     // Stop sound...
            delay(1000);        // ...for 1sec
            alarm ++;
          }
          
        }
      }

      
      if ( i < 0 && i > -5 && T==1 ) {
        Serial.println("Eaten");
        digitalWrite(8,HIGH);
        delay(500);
        digitalWrite(8,LOW);
        delay(500);
        digitalWrite(8,HIGH);
        delay(500);
        digitalWrite(8,LOW);
        delay(500);
        digitalWrite(8,HIGH);
        delay(500);
        digitalWrite(8,LOW);
        delay(500);
        
          Serial.println("cup placed back");
          Z=1;
          x=0;
          digitalWrite(LED1_PIN, LOW);
          digitalWrite(LED_PIN, LOW);
        }

    
    }
    
  



  // receive command from serial terminal, send 't' to initiate tare operation:
  if (Serial.available() > 0 ) {
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay();
  }

  // check if last tare operation is complete:
  if (LoadCell.getTareStatus() == true) {
    Serial.println("Tare complete");
  }

  }
  
}

// ---------------------------------------------


void moveServos(int servoIndex, int degrees) 
{
  int pulseWidth = map(degrees, 0, 180, servoMin[servoIndex], servoMax[servoIndex]);
  pwm.setPWM(servoChannels[servoIndex], 0, pulseWidth);
}

void moveServo(int servoIndex, int degrees) 
{
  pwm.setPWM(servoChannels[servoIndex], 0, map(degrees, 0, 180, servoMin[servoIndex], servoMax[servoIndex]));
}

int readFrequency(int s2, int s3) 
{
  // Setting the filter
  digitalWrite(S2, s2);
  digitalWrite(S3, s3);
  
  // Reading the output frequency
  return pulseIn(sensorOut, LOW);
}
/*
char detectColor(int red, int green, int blue, int clear) 
{
  // Check for red color
  if (red >= 65 && red <= 100 && green >= 120 && green <= 180 && blue >= 95 && blue <= 145 && clear >= 30 && clear <= 65)
  {
    Serial.println("Red Ball Detected");
    colour = 'R';
  }
  // Check for green color
  else if (red >= 95 && red <= 125 && green >= 70 && green <= 95 && blue >= 70 && blue <= 95 && clear >= 30 && clear <= 55) 
  {
    Serial.println("Green Ball Detected");
    colour = 'G';
  }
  // Check for blue color
  else if (red >= 115 && red <= 135 && green >= 60 && green <= 85 && blue >= 45 && blue <= 70 && clear >= 25 && clear <= 55) 
  {
    Serial.println("Blue Ball Detected");
    colour = 'B';
  }
  // Check for yellow color (red + green)
  else if (red >= 30 && red <= 64 && green >= 45 && green <= 65 && blue >= 40 && blue <= 60 && clear >= 10 && clear <= 40)
  {
    Serial.println("Yellow Ball Detected");
    colour = 'Y';
  }
  */
char detectColor(int red, int green, int blue, int clear)   
{ 
  if (red >= 65 && red <= 100 && green >= 120 && green <= 180 && blue >= 95 && blue <= 145 && clear >= 30 && clear <= 65) 
  { 
    Serial.println("Red Ball Detected"); 
    colour = 'R'; 
  } 
  // Check for green color 
  else if (red >= 95 && red <= 125 && green >= 70 && green <= 95 && blue >= 70 && blue <= 95 && clear >= 30 && clear <= 55)  
  { 
    Serial.println("Green Ball Detected"); 
    colour = 'G'; 
  } 
  // Check for blue color 
  else if (red >= 126 && red <= 150 && green >= 60 && green <= 95 && blue >= 45 && blue <= 80 && clear >= 25 && clear <= 55)  
  { 
    Serial.println("Blue Ball Detected"); 
    colour = 'B'; 
  } 
  // Check for yellow color (red + green) 
  else if (red >= 30 && red <= 64 && green >= 45 && green <= 80 && blue >= 40 && blue <= 80 && clear >= 10 && clear <= 40) 
  { 
    Serial.println("Yellow Ball Detected"); 
    colour = 'Y'; 
  }

  // If none of the above colors are detected
  else 
  {
    Serial.println("Unknown Ball, please remove");
    colour = 'U';
  }
  return colour;
}
