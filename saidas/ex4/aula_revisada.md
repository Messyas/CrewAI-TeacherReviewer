# Interrupções no ESP32

## Conceitos Essenciais

### **1. O que são Interrupções no ESP32?**
Interrupções são eventos que interrompem o fluxo normal de instruções do microcontrolador, permitindo a execução de códigos específicos em resposta a esses eventos.

### **2. Tipos de Interrupções no ESP32?**
- **Interrupções por Pinos:** Usadas para processar eventos de mudança no nível do pin.
- **Interrupções por Software:** Disparadas pelo usuário para executar códigos específicos.
- **Interrupções por Hardware:** Gerenciadas pelos controladores de hardware.

### **3. Usos Comuns das Interrupções?**
- **Leitura de Sensores:** Processar dados sem interromper o programa principal.
- **Comunicação Sincronizada:** Manter a comunicação em ritmos diferentes.
- **Execução de Código em Tempo Real:** Executar códigos que precisam ser executados rapidamente.

### **4. Como Configurar Interrupções no ESP32?**
- **Definindo a Função ISR:** Exemplo em C:

  ```c
  void setup() {
    pinMode(22, INPUT);
    attachInterrupt(22, interrupcao, RISING);
  }
  
  void interrupcao() {
    // Código que será executado
  }
  ```

### **5. Limitações das Interrupções no ESP32?**
- **Tempo de Retorno:** O microcontrolador pode demorar para retornar ao código principal.
- **Uso de Recursos:** Podem consumir mais energia e recursos.
- **Complexidade:** Programação por interrupção pode ser mais complexa.

## Exemplos Práticos

### **Exemplo 1 - Desligar um LED ao Inverter o Nível de um Pino**
```c
void setup() {
  pinMode(22, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  attachInterrupt(22, inverteLED, CHANGE);
}

void loop() {
  // Código principal do programa
}

void inverteLED() {
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
}
```

### **Exemplo 2 - Responder ao Tocador de Sonar**
```c
const int TRIGGER_PIN = 33;
const int ECHO_PIN = 34;

Serial.begin(115200);

void setup() {
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(ECHO_PIN), respostaSonar, RISING);
}

void loop() {
  // Código principal do programa
}

void respostaSonar() {
  Serial.println("Objeto detectado");
}
```

## Atividade

### **Tarefa:** Implemente uma solução que habilite um LED a piscar em resposta a uma mudança no nível de um sensor de distância (por exemplo, unidade ultrassônica).

#### **Passos a seguir:**
1. Defina a função `ISR` para a tarefa de leitura do sensor.
2. Implemente a lógica do piscar do LED dentro dessa função.
3. Configure o sensor de distância para disparar a interrupção em intervalos regulares.
4. Teste e valide o funcionamento do programa.

### **Dicas**
- Use `attachInterrupt` para associar a interrupção ao sensor de distância.
- Utilize `digitalWrite` para controlar o estado do LED.
- Verifique que o código principal (`loop()`) não está sendo afetado negativamente pelo uso da interrupção.

## Conclusão

Interrupções no ESP32 são uma ferramenta útil para processar eventos de maneira eficiente. Elas permitem que o microcontrolador responda rapidamente a cenários em tempo real, mas é importante ter consciência das limitações e dos aspectos de programação específicos envolvidos.