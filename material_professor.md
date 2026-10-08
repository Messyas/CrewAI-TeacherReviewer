# Interrupções no ESP32: Implementação e Uso

## Objetivos
Ao final desta sessão didática, os estudantes de graduação conseguirão compreender e implementar a prática de utilização de interrupções no sistema ESP32. Eles serão capazes de escrever códigos que utilizam interrupções para realizar tarefas que devem ser executadas com maior prioridade ou com maior frequência do que o processamento principal do ESP32.

## Conceitos

### 1. Introdução às Interrupções
Interrupções em microcontroladores, como o ESP32, ocorrem quando um determinado evento externo ou interno requer a imediata execução de um código específico, interrompendo o fluxo de instruções principais. No ESP32, essas interrupções são implementadas através de bibliotecas e funções internas que permitem a implementação eficaz de tarefas como leituras rápidas de sensores ou manipulações frequentes de pinos.

### 2. Tipos de Interrupções
No ESP32, existem vários tipos de interrupções, incluindo, mas não limitado a, interrupções de timer, interrupções de pinos GPIO, entre outras. Cada tipo de interrupção é ligada a um evento específico, como a detecção de um pulso na linha de um sensor ou a contagem de tempo em um timer.

### 3. Biblioteca de Interrupções no ESP32
O ESP32 utiliza a biblioteca `espInterrupts.h` para definir e acionar interrupções. Essa biblioteca fornece funções essenciais para a implementação de interrupções, incluindo a criação de uma rotina de callback que será executada assim que a interrupção é acionada.

### 4. Estrutura de Trabalho das Interrupções
Ao criar uma interrupção, o usuário define sua callback function, o evento que disparará a interrupção e o estado das registradoras e pinos que precisam ser alterados. Quando o evento ocorre, a execução da main loop do ESP32 é pausada para que a função de callback seja executada, normalmente para leituras e processamentos rápidos.

### 5. Exemplo Prático

```cpp
#include "esp中断处理.h"

void setup() {
  pinMode(4, INPUT);   // Configura o pin 4 como entrada
  attachInterrupt(digitalPinToInterrupt(4), pin4Interrupt, FALLING); // Configura a interrupção
}

void loop() {
  delay(1000);         // Espera 1 segundo
}

// Função de callback para interrupção
void pin4Interrupt() {
  Serial.println("Pin 4 was clicked");
}
```

No exemplo acima, o interruptor ligado ao pin 4 gera uma interrupção quando o seu estado muda (FALLING), iniciando a execução da função de callback `pin4Interrupt`.

### 6. Uso das Interrupções em Projetos Realísticos
Uma situação comum para usar interrupções no ESP32 é em aplicações de sensores, onde uma ação rápida e eficiente é necessária sem interromper a execução principal. Por exemplo, um barômetro de chuva pode acionar uma interrupção que disparará um alerta de chuva rápida, sem comprometer a tarefa principal de rastreamento de nível de chuva.

## Exemplo

Implemente um código que use a interrupção para ler a tensão em um pin GPIO, com a tensão variando a cada meio segundo e o relógio interno (RTC) do ESP32.

### Código

```cpp
#define INPUT_PIN 5
uint16_t sensorValue;

void setup() {
  Serial.begin(115200);
  pinMode(INPUT_PIN, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(INPUT_PIN), readSensor, RISING);
  sensorValue = 0;
}

void loop() {
  delay(500);          // Ajusta a leitura ao meio segundo
}

void readSensor() {
  sensorValue = analogRead(INPUT_PIN);
  Serial.println("sensorValue: " + String(sensorValue));
}
```

Neste código, ao detectar um pulso na linha `INPUT_PIN` (RISING edge), a função `readSensor` será chamada, imprimindo o valor do sensor.

## Atividade
Implemente uma pequena aplicação no ESP32 que utilize interpolação em um pino GPIO ou qualquer interruptor ligado a um sensor. A interpolação de valores deve ser realizada no interruptor.

### Dicas
- Use um interruptor para disparar uma leitura em um pino GPIO.
- Apresente uma sequência de valores de 0 a 1023 (considerando o GPIO como um pin analógico) de maneira intermitente.

## Síntese
O uso de interrupções no ESP32 é uma técnica essencial para implementar ações rápidas e precisas sem interromper o fluxo principal do código. A definição de uma interrupção envolve a inicialização de um pin GPIO ou componente interno, a definição da função de callback que será executada quando a interrupção ocorrer, e a especificação do eventType que acionará a interrupção (subida, descida, etc.).