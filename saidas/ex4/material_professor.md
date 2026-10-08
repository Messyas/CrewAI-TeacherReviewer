```markdown
# Interrupções no ESP32

## 1. Introdução às Interrupções

Interrupções, também conhecidas como exceções de hardware, são eventos que interrompem o fluxo normal de execução de uma aplicação para permitir a execução de um código específico. No ESP32, elas são usadas amplamente para otimizar o uso do processador, permitindo que o microcontrolador execute tarefas em segundo plano.

## 2. Tipos de Interrupções no ESP32

O ESP32 suporta várias fontes de interrupções, incluindo:
- **Interrupções de Periféricos**: Gerenciadas pelos periféricos interconectados (ex. GPIO, ADC, PWM, UARTs, SPI, I2C, etc.).
- **Interrupções de Software**: Estão associadas a eventos programados pelo software (ex. tempo real, temporizadores).

## 3. Estrutura da Função de Interrupção no ESP32

Uma função de interrupção no ESP32 deve atender aos seguintes requisitos:
- Deve ser declarada com o modificador `IRQ ISR(void)` (especificador de interrupção).
- Deve ser invocada apenas do modo de interrupção, e não do modo de programa.
- Deve ter o menor tempo de execução possível, para permitir que o processador retorne rapidamente para a execução normal.

Exemplo:
```c
void IRQ ISR(interruptHandler) {
    // Código da interrupção
}
```

## 4. Configuração das Interrupções

Para configurar uma interrupção no ESP32, é necessário:
- Ajustar os interrupts control registers (ICSRs) das configurações de periféricos.
- Programar as rotinas de interrupção (ISR) para manipular os eventos específicos.

Exemplo para Configurar um GPIO:
```c
void setup() {
  // Estabelecer o pino GPIO como interruptante
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(2, interruptHandler, FALLING);
}

void interruptHandler() {
  // Código para lidar com a interrupção
  Serial.println("Interrupção detectada!");
}
```

### Exemplo Prático

Suponha que queremos controlar um LED a partir de um interruptor. O interruptor aciona uma interrupção que apaga o LED a cada clique.

```c
const int buttonPin = 2;
const int ledPin = 13;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  attachInterrupt(buttonPin, blinkLED, FALLING);

  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Código para loop principal, sem interferência
}

void blinkLED() {
  digitalWrite(ledPin, !digitalRead(ledPin));
}
```

### Atividade

Implemente um sistema que ligue e desligue um LED com base em duas teclas. A primeira tecla aciona a interrupção para ligar o LED, e a segunda tecla aciona a interrupção para desligar o LED.
```c
const int button1Pin = 2;
const int button2Pin = 3;
const int ledPin = 13;

void setup() {
  pinMode(button1Pin, INPUT_PULLUP);
  attachInterrupt(button1Pin, switchOnLED, FALLING);

  pinMode(button2Pin, INPUT_PULLUP);
  attachInterrupt(button2Pin, switchOffLED, FALLING);

  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Código para loop principal, sem interferência
}

void switchOnLED() {
  digitalWrite(ledPin, HIGH);
}

void switchOffLED() {
  digitalWrite(ledPin, LOW);
}
```

**Nota:** Certifique-se de testar seus códigos no ambiente de desenvolvimento correspondente antes de carregá-los no ESP32.**
```