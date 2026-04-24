# Lec 01 — Introduction

---

## 1. 메카트로닉스 (Mechatronics) 정의

- **Mecha**(nics) + (Elec)**tronics** → 1969년 일본에서 처음 사용
- Mechatronics 저널 공식 정의:
  > "Fusion of mechanical and electrical disciplines in modern engineering process. New concept to the **design of systems, devices, and products** aimed at achieving an **optimal balance between basic mechanical structures and its overall control**"
- Interdisciplinary field: 기계 + 전자 + 정보 + 지능형 시스템
- 메카트로닉스 = Electromechanics + **Intelligence(software)** 개념 포함

---

## 2. 메카트로닉스 시스템 구조

```
MECHANICAL SYSTEM (system model / dynamic response)
        ↑
ACTUATORS ──→ SENSORS ──→ INPUT SIGNAL CONDITIONING & INTERFACING
  - solenoids, voice coils     - switches / strain gauge          - discrete circuits / filters
  - DC motors                  - potentiometers / thermocouple     - amplifiers / A/D, D/A
  - stepper motors             - photoelectrics / accelerometer
  - servomotors                - digital encoder / MEMS
  - hydraulics, pneumatics
        ↑
OUTPUT SIGNAL ←── DIGITAL CONTROL ARCHITECTURES ←── USER INTERFACE
CONDITIONING        - logic circuits / sequencing          Inputs: buttons, knobs, keypad
& INTERFACING       - microcontroller / logic, arithmetic  Outputs: LEDs, LCD, monitor
  - D/A, D/D          - SBC / control algorithms
  - PWM               - PLC / communication
  - power transistors
  - power amps
```

### 계측 시스템 흐름
```
Transducer → Signal Processor → Recorder
```
- 예시 (디지털 온도계): 열전대 → 증폭기 → A/D + display decoder → LED 디스플레이

---

## 3. 메카트로닉스 역사

| 연도 | 주요 발전 |
|------|-----------|
| ~1900 | 순수 기계 시스템 (증기엔진, 발전기) |
| 1920 | 전기 드라이브 추가 (DC/AC 모터) |
| 1935 | 자동 제어 (릴레이, 솔레노이드, PI 제어기) |
| 1955 | 전자(아날로그) 제어, 순차 제어 |
| 1975 | 디지털 연속/순차 제어 (마이크로컨트롤러 1978) |
| 1985~ | **Mechatronic systems**: 기계+전자 통합, 소프트웨어가 기능 결정, 시너지 효과 |

---

## 4. 메카트로닉스가 기계 시스템을 바꾼 방식

- 기존: 순수 기계 제어 (예: Watt Governor — 원심력으로 밸브 제어)
  - Limited complexity in feedback
  - Power for valve from main shaft
- 변화: 전자부품 추가 (예: Solenoid valve)
  - **Component isolation / modularization** 실현

### Component Isolation의 결과
1. Flexible power source
2. Flexible kinematic design
3. Control
   - Feedback Control: 정교한 제어 가능
   - **Computers for control**: 소프트웨어로 무한한 복잡도 처리 가능
   - → Managing complexity becomes important issue in mechatronics

---

## 5. 메카트로닉스 응용 분야

Control Systems + Electronic Systems + Mechanical Systems + Computers의 교차점 = **MECHATRONICS**

응용: Automotive, Aerospace, Medical, Xerography, Defense Systems, Consumer Products, Manufacturing, Materials Processing

---

## 6. Mechatronics for Mechanical Engineers

- 사실상 오늘날 거의 모든 기계 요소 = 메카트로닉스 시스템
  - 자동차, 로봇, 핸드폰, 신재생 에너지, 나노 소자, 현미경, MEMS
- 연구·개발 아이디어를 실현/구현하기 위한 도구
  - 실험 데이터의 수집 및 분석
  - 실험 장치의 제작 및 구현
  - 제품 설계, 제작, 및 제어
  - 캡스톤 디자인 프로젝트

---

## 7. Computer Systems 분류

### 컴퓨터 시스템 카테고리
- Main frame computers, server, desktop computer
- **Embedded computer** ← 메카트로닉스 핵심
  - TVs, VCRs, DVD players, remote controls, washing machines, cell phones, air conditioners, game consoles, ovens, toys
  - PC 수 << Embedded 수 (압도적으로 많음)
  - 공통점: 둘 다 processor, memory, I/O 보유
  - 차이점: intended use가 다름 → system design과 software에 반영

---

## 8. Embedded Computer

- **Dedicated to a specific task** (특정 작업에 전용)
- Used to replace application-specific electronics
- 장점:
  - Functionality는 **software**가 결정 → hardware가 아님
  - → 복잡한 회로보다 생산·진화가 쉬움
- 특징:
  - 하나의 application이 **permanently** 실행됨
  - Software는 시스템의 **nonvolatile memory**에 저장
  - Hardware는 desktop system보다 훨씬 단순

---

## 9. Software Layer 구조

```
Desktop Computer:          Complex Embedded:      Simple Embedded:
Applications               Applications           Application
Operating System     →     Operating System   →   Firmware
Firmware                   Firmware
Hardware                   Hardware               Hardware
```

- 각 레이어는 **바로 위/아래 레이어하고만** 상호작용
- 레이어가 적을수록 단순한 임베디드 시스템

### Firmware
- 컴퓨터 최초 전원 ON 시 프로세서가 실행하는 프로그램
- 다른 하드웨어 서브시스템을 **초기화**하고 올바른 동작을 위해 **구성**
- **Bootloader** (firmware 내 위치):
  - 디스크(또는 nonvolatile memory/네트워크)에서 OS를 읽어 메모리에 올리는 특수 프로그램
  - 프로세서가 OS를 실행할 수 있도록 준비

### Operating System (OS)
- 컴퓨터 동작 제어
- 메모리 사용 구성
- 장치 제어 (keyboard, mouse, screen, disk drives)
- 사용자 인터페이스 제공
- application program에 소프트웨어 도구 세트 제공
- **임베디드 시스템은 OS가 필요 없을 수도 있음**

### Application Software
- 컴퓨터의 기능을 제공
- application 아래 모든 것 = **system software**

---

## 10. Basic Computer System

- Processor ↔ Memory (Data bus, Address bus, Control bus)
- I/O devices: Modems, scanners, printers, keyboards, mice
- Disks, Display

### Data Flow
- Instructions: Processor ← Memory (Read)
- Data: Processor ↔ Memory (Read/Write)

---

## 11. Microprocessor vs Microcontroller

| 구분 | Microprocessor (MPU) | Microcontroller (MCU) |
|------|----------------------|-----------------------|
| 정의 | 단일 집적회로에 구현된 프로세서 | 프로세서 + 메모리 + I/O 장치를 단일 집적회로에 통합 |
| 별칭 | CPU (Central Processing Unit) | — |
| 예시 | Intel Pentium, Freescale/IBM PowerPC, MIPS, ARM, Sun SPARC, Apple M1 | PIC, AVR, PowerPC (I/O 내장) |
| 용도 | 범용 컴퓨팅 | 임베디드 시스템 전용 |
| 특징 | CPU만 → 외부 RAM, ROM, I/O 필요 | CPU + RAM + ROM + I/O 내장 → 외부 부품 최소화 |

---

## 12. Von Neumann Machine

- **데이터와 명령어 사이에 본질적 차이 없음**
- Data has no inherent meaning (맥락에 따라 의미 결정)
- **데이터와 명령어가 같은 메모리 공유**
- Memory = 1차원 선형 저장 위치 배열
- 구조: CPU (Control Unit + ALU) ↔ 버스(Bus) ↔ Memory Unit (Program memory + Data memory)

### I/O 방식
| 방식 | 설명 |
|------|------|
| **Ported I/O** | I/O 장치를 위한 별도 주소 공간 (Intel x86 계열) |
| **Memory-mapped I/O** | I/O 장치가 메모리와 동일한 주소 공간에 존재 (대부분 프로세서) |

---

## 13. Harvard Architecture

- Von Neumann과의 차이점:
  - **명령어와 데이터가 별도 메모리 공간** → 각각 별도의 address, data, control bus
  - 명령어와 데이터 fetch가 **동시에** 발생 가능
  - 명령어 크기가 표준 데이터 단위(word) 크기에 구속받지 않음
- 예시: **AVR processors** (Arduino에 사용)

| 구분 | Von Neumann | Harvard |
|------|-------------|---------|
| 메모리 | 프로그램+데이터 공유 | 프로그램/데이터 분리 |
| 버스 | 1개 | 2개 (각각) |
| 동시 fetch | 불가 | 가능 |
| 병목 | 있음 | 없음 |
| 속도 | 느림 | 빠름 |
| 사용처 | 일반 PC | MCU, DSP, AVR |

---

## 14. Processor Operation

프로세서가 외부 칩과 수행하는 **6가지 기본 접근 유형**:
1. write data to memory
2. write data to an I/O device
3. read data from memory
4. read data from an I/O device
5. read instructions from memory
6. perform internal manipulation of data within the processor

### Registers
- 프로세서의 **내부 데이터 저장소**
- 프로세서는 제한된 수의 레지스터 보유
- 현재 조작 중인 데이터/피연산자를 보관

---

## 15. Interrupts (인터럽트)

- 별칭: **traps** 또는 **exceptions**
- 정의: 현재 프로그램 실행에서 프로세서를 다른 곳으로 전환하여 발생한 이벤트를 처리하는 기법
- 장점: I/O 장치가 서비스를 필요로 하는지 계속 확인(polling)하는 부담에서 프로세서를 해방

### 인터럽트 발생 시 처리 절차
1. 프로세서가 레지스터와 program counter를 스택에 저장 (현재 상태 보존)
2. **interrupt vector**를 program counter에 로드
3. interrupt vector = **ISR(Interrupt Service Routine)**이 위치한 주소
4. ISR 실행 후 원래 프로그램으로 복귀

### Hardware Interrupts — I/O 장치 준비 감지 방법
| 방식 | 설명 |
|------|------|
| **Busy waiting / Polling** | 프로세서가 장치의 status register를 준비될 때까지 계속 확인 |
| **Vectored interrupts** | 인터럽트 발생 장치가 프로세서에 interrupt vector를 직접 제공 |

---

## 16. Digital Signal Processors (DSP)

- 배열 데이터의 수치 처리에 최적화된 **명령어 세트와 아키텍처**를 가진 특수 프로세서
- 특징:
  - 매우 높은 처리량 → CISC와 RISC 프로세서를 특정 응용에서 능가
  - 배열의 수치 처리에 적합한 특수 하드웨어
  - 산술 연산 속도 향상을 위한 전용 하드웨어 내장
- 임베디드 응용에 널리 사용
- 많은 일반 임베디드 마이크로컨트롤러가 DSP 기능 일부 포함

---

## 17. Type of Memory

### RAM (Random Access Memory)
- 컴퓨터 시스템의 **"working memory"**
- 실제로는 대부분의 컴퓨터 메모리가 random access이므로 명칭이 다소 부적절
- **휘발성(Volatile)**: 전원 차단 시 데이터 소실

### ROM (Read-Only Memory)
- 실제로는 많은 현대 ROM도 쓰기 가능 → 명칭이 다소 부적절
- 종류: EPROM, EEROM(=EEPROM), **Flash memory** (=Flash RAM=Flash ROM)
- **비휘발성(Nonvolatile)**: 전원 없이도 내용 유지
- RAM보다 느림, fast static RAM보다 훨씬 느림

| 종류 | 휘발성 | 읽기/쓰기 | 용도 |
|------|--------|-----------|------|
| SRAM | O | R/W (빠름) | 캐시, 레지스터 |
| DRAM | O | R/W | 메인 메모리 |
| Flash | X | R/W (느린 쓰기) | 펌웨어, 프로그램 저장 |
| EEPROM | X | R/W (바이트 단위) | 설정값 저장 |
| ROM | X | R only | 변경 불필요 코드 |

---

## 18. Block Diagram of Embedded Computer

임베디드 컴퓨터 내부 구성:
- **CPU**
- **ROM** (프로그램 저장)
- **RAM** (데이터 저장)
- **Analog in (ADC)**: 온도, 빛, 가속도, 진동, 습도, 압력, 자기장 측정
- **Digital I/O**: 스위치, 버튼, 모터, on/off 제어
- **SPI, I2C**: 외부 칩 통신
- **Counter/Timers**: 모터, 디지털 펄스
- **Serial port (UART)**: 호스트 컴퓨터, 네트워크 통신

---

## 19. Arduino vs Raspberry Pi

| 항목 | Arduino Uno | Raspberry Pi 4 | BeagleBone |
|------|-------------|----------------|------------|
| 종류 | MCU | SBC | SBC |
| Processor | ATMega 328 | ARM Cortex-A72 | ARM Cortex-A8 |
| Clock Speed | 16MHz | 700MHz+ | 700MHz |
| RAM | 2KB | 1GB~4GB | 256MB |
| Flash | 32KB | SD Card | 4GB(microSD) |
| OS | 없음 | Linux (Debian/Ubuntu) | Linux |
| Analog Input | 6 × 10-bit ADC 내장 | **없음** (외부 ADC 필요) | 7 × 12-bit |
| Digital GPIO | 14 | 8 | 66 |
| PWM | 6 | — | 8 |
| 실시간 제어 | **가능** | 어려움 | 어려움 |
| 용도 | 센서·모터 저수준 제어 | 영상처리·고수준 연산 | 범용 임베디드 |
| Dev IDE | Arduino Tool | IDLE, Scratch, Linux | Python, Scratch, Linux |

### SBC 비교 (Jetson Nano vs 라즈베리파이4 vs 라떼판다 알파)

| 항목 | Jetson Nano | 라즈베리파이 4 | 라떼판다 알파 |
|------|-------------|---------------|--------------|
| 크기 | 100×80mm | 85×56mm | 115×78mm |
| OS | Linux | Linux | **Windows 10** |
| CPU | 4 Core ARM Cortex A57 | 4 Core ARM Cortex A72 | Intel M3-8100Y |
| GPU | **128 CUDA core (Maxwell)** | Broadcom VideoCore IV | Intel HD Graphics 615 |
| RAM | 4GB DDR4 | 1~4GB | **8GB DDR4** |
| 전원 | 10~20W | 15W | 36~45W |

---

## 20. Why do we need the processor?

- 프로세서는 입력의 debounce 회로를 대체 가능
- 내부 메모리와 소프트웨어 실행 능력으로:
  - 시스템 상태(mode) 추적
  - 여러 입력을 상호 관련하여 모니터링
  - 출력에 복잡한 제어 시퀀싱 제공
- **핵심**: 마이크로프로세서 포함 → **하드웨어 복잡도 감소** + **시스템 기능 증가**
  - 더 발전된 프로세서와 다양한 I/O → 임베디드 컴퓨터의 기능과 유용성이 크게 향상

---

## 21. Microcontroller Application 예시

- 포텐셔미터(속도 설정) → **A/D 변환** → PIC 마이크로컨트롤러 → **D/A 변환** → Power Amp → DC Motor
- 부가: LED 인디케이터, Digital Encoder (피드백)
- 실제 구성: PIC + D/A + 전압 레귤레이터 + 전력 증폭기(Heat sink) + DC 모터 + Gear Drive + 관성 부하(Inertial load)

---

*Lec01 끝 — 다음: Lec02 Electric Circuits and Components*
