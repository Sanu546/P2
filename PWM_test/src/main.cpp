#include <Arduino.h>
#include <PWM.h>
int pwmVal = 230;
String str;

int openCellPos = 207;
int closeCellPos = 204;
int openLidPos = 206;
int closeLidPos = 204;

bool debug = false; // put false !!!!!!!!!!!!!!!!!!!

void setup()
{
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  Serial.begin(9600);
  // initialize all timers except for 0, to save time keeping functions
  InitTimersSafe();

  bool success = SetPinFrequencySafe(10, 100);

  // if the pin frequency was set successfully, turn pin 13 on
  if (success)
  {
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH);
  }
}

void loop()
{
  if (debug)
  {

    if (Serial.available())
    {
      char c = Serial.read();
      str += c;
      if (c == '\n')
      {
        pwmVal = str.toInt();
        Serial.print("PWM Value: ");
        Serial.println(pwmVal);
        str = ""; // Clear the string after printing
      }
    }
    pwmWrite(10, pwmVal);
  }

  else
  {
    if (digitalRead(A0) == HIGH)
    {
      pwmWrite(10, openLidPos);
    }

    if (digitalRead(A1) == HIGH)
    {
      pwmWrite(10, closeLidPos);
    }

    if (digitalRead(A2) == HIGH)
    {
      pwmWrite(10, openCellPos);
    }

    if (digitalRead(A3) == HIGH)
    {
      pwmWrite(10, closeCellPos);
    }
  }
}
