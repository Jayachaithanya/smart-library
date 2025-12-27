const int ledShelf1 = 3;
const int ledShelf2 = 4;
const int ledShelf3 = 5;
const int ledStatus = 8;
const int buzzer = 11;

// tones for each book
const int toneKrsna = 500;
const int toneGK = 900;1
const int toneYodaiyar = 1100;

void setup() {
  Serial.begin(9600);

  pinMode(ledShelf1, OUTPUT);
  pinMode(ledShelf2, OUTPUT);
  pinMode(ledShelf3, OUTPUT);
  pinMode(ledStatus, OUTPUT);
  pinMode(buzzer, OUTPUT);

  digitalWrite(ledStatus, HIGH);

  printMenu();
}

void loop() {
  if (Serial.available()) {

    char option = Serial.read();

    switch (option) {
      case '1':
        Serial.println("Book Selected: youdaiyar");
        Serial.println("Shelf Activated: A");
        blinkLED(ledShelf1, toneKrsna);
        break;

      case '2':
        Serial.println("Book Selected: KRSNA");
        Serial.println("Shelf Activated: B");
        blinkLED(ledShelf2, toneGK);
        break;

      case '3':
        Serial.println("Book Selected: GK");
        Serial.println("Shelf Activated: C");
        blinkLED(ledShelf3, toneYodaiyar);
        break;

      default:
        Serial.println("Invalid option. Enter 1, 2, or 3.");
        break;
    }

    printMenu();
  }
}

void blinkLED(int pin, int toneFreq) {
  for (int i = 0; i < 6; i++) {
    digitalWrite(pin, HIGH);
    tone(buzzer, toneFreq);
    delay(300);

    digitalWrite(pin, LOW);
    noTone(buzzer);
    delay(300);
  }
}

void printMenu() {
  Serial.println();
  Serial.println("Smart Library Assistant");
  Serial.println("------------------------");
  Serial.println("Choose a book:");
  Serial.println("1 - YOUDAIYAR");
  Serial.println("2 - KRSNA");
  Serial.println("3 - GK");
  Serial.println("------------------------");
}
