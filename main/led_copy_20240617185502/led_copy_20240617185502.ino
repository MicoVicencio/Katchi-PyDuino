// Define pin numbers for buttons
#define BUTTON_PIN_1 6
#define BUTTON_PIN_2 7

// Include the Wire library for I2C communication
#include <Wire.h>

// Include the LiquidCrystal_I2C library for LCD display
#include <LiquidCrystal_I2C.h>

// Initialize the LCD with I2C address 0x27 and dimensions 16x2
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Initialize a string to hold the song title
String songTitle = "Song Title";

void setup() {
  // Begin serial communication at a baud rate of 9600
  Serial.begin(9600);
  
  // Initialize the LCD
  lcd.init();
  
  // Turn on the backlight of the LCD
  lcd.backlight();
  
  // Set BUTTON_PIN_1 as an input
  pinMode(BUTTON_PIN_1, INPUT);
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming data until newline character
    String received = Serial.readStringUntil('\n');
    
    // Clear the LCD screen
    lcd.clear();
    
    // Set the cursor to the first line (0,0) and print the song title
    lcd.setCursor(0, 0);
    lcd.print(songTitle);
    
    // Set the cursor to the second line (0,1) and print the received data
    lcd.setCursor(0, 1);
    lcd.print(received);
  }
  
  // Read the state of BUTTON_PIN_1
  byte buttonState1 = digitalRead(BUTTON_PIN_1);
  
  // Check if BUTTON_PIN_1 is pressed
  if (buttonState1 == HIGH) {
    // Send "1" to the serial port if the button is pressed
    Serial.println("1");
  }
  
  // Delay to debounce the button press
  delay(100);
}
