//Arduino Thermistor
//Author: CircuitBasics.com
//Modifications by Yale Empie
//Company: Team Snooze @ University of North Texas

int ThermistorPin = 0;    //A0 Pin - Arduino Nano
int Vo;                   //Nominal Voltage (5V)
float R1 = 10000;         //Pad Resistor Value
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;   //Steinhart-Hart Environmental Values

void setup() {
Serial.begin(9600);
}

void loop() {

  Vo = analogRead(ThermistorPin);

  //Steinhart-Hart
  R2 = R1 * (1024.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;
  T = (T * 9.0)/ 5.0 + 32.0; 

  Serial.print("# "); 
  Serial.print(T);    //Temperature in Fahrenheit
  Serial.print(" "); 

  delay(500);         //2 Samples per Second
}

