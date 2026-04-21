# 실습보고서 #2

> **실습일:** 2026-04-08
> **실습 환경:** Raspberry Pi 4 Model B + MCP3002 (SPI) + ADXL345 (I2C)

---

## 1. 실험 목표 및 목적

### 통신 프로토콜 학습
임베디드 시스템에서 근거리 통신에 주로 사용되는 동기식 직렬 통신 방식인 **SPI(Serial Peripheral Interface)** 와 **I2C(Inter-Integrated Circuit)** 의 동작 원리 및 차이점을 학습한다.

### 데이터 처리 역량 강화
센서로부터 전송되는 디지털 데이터를 수신하기 위한 **비트 연산(Bitwise Operation)** 및 **16진수 데이터 처리** 과정을 이해한다.

### 실습 목표

| 항목 | 내용 |
|---|---|
| SPI 통신 실습 | 라즈베리파이 ↔ MCP3002(10bit 2채널 ADC) 연결, 가변저항/조도센서/조이스틱 아날로그 신호 디지털 변환 |
| I2C 통신 실습 | 라즈베리파이 ↔ ADXL345(3축 디지털 가속도계) 연결, 3축 가속도 데이터 수집 |
| 환경 설정 | Interface Configuration에서 SPI/I2C 활성화, Python 라이브러리 활용 |
| 응용 분석 | 수집된 가속도 데이터로 기울임 각도(Tilt Angle) 계산 |

---

## 2. 실험 진행 과정

### 2-1. SPI 통신 실험

> 라즈베리파이의 SPI 버스를 통해 MCP3002(10bit 2채널 ADC)에서 아날로그 전압을 읽어 디지털 값으로 변환

#### 라즈베리파이 ↔ MCP3002 핀 연결

| MCP3002 핀 | 기능 | 라즈베리파이 핀 |
|---|---|---|
| 1번 (CS/SHDN) | Chip Select | 24번 (CE0) |
| 5번 (DIN) | MOSI | 19번 |
| 6번 (DOUT) | MISO | 21번 |
| 7번 (CLK) | 클럭 | 23번 |

#### 가변저항 (CH0)

- 가변저항을 3.3V ~ GND 사이에 연결
- 다이얼 회전 → 내부 저항값 변화 → 0V~3.3V 연속적인 아날로그 전압 발생 → MCP3002 CH0 입력

#### 조도센서 CdS (CH1) — 분압 회로

조도센서는 저항값이 변하는 소자이므로, MCP3002가 읽을 수 있는 전압으로 변환하기 위해 **분압 회로** 구성 (조도센서 + 100kΩ 고정 저항 직렬 연결)

$$V_{CH1} = \frac{R_{100k}}{R_{CdS} + R_{100k}} \times 3.3V$$

| 조도 상태 | CdS 저항 | CH1 입력 전압 |
|---|---|---|
| 밝을 때 | 감소 | 상승 |
| 어두울 때 | 증가 | 하강 |

#### 조이스틱 KY023 (CH0, CH1)

- HORZ(VRx) → MCP3002 CH0: X축 방향 아날로그 값
- VERT(VRy) → MCP3002 CH1: Y축 방향 아날로그 값
- 10bit ADC → 0~1023 디지털 값으로 변환

---

### 2-2. I2C 통신 실험

> 라즈베리파이의 I2C 버스를 통해 ADXL345(3축 디지털 가속도계)에서 가속도 데이터를 읽어 디지털 값으로 변환

#### 라즈베리파이 ↔ ADXL345 핀 연결

| ADXL345 핀 | 기능 | 라즈베리파이 핀 |
|---|---|---|
| 5번 (SCL) | 클럭 | 5번 (BCM_3) |
| 4번 (SDA) | 데이터 | 3번 (BCM_2) |
| 9번 (3V3) | 전원 | 1번 (3.3V) |
| 8번 (GND) | 그라운드 | 9번 (GND) |

#### 장치 주소 확인

```bash
i2cdetect -y 1
```

→ 주소 `0x53` (`01010011`) 에서 감지

SDO/ALT ADDRESS 핀이 GND에 연결되어 있어 기본 주소 `0x53`으로 고정. (VCC 연결 시 `0x1D`)

#### 3축 가속도 데이터 레지스터 구조 (Little-Endian)

| 축 | 하위 byte 주소 | 상위 byte 주소 |
|---|---|---|
| X | 0x32 | 0x33 |
| Y | 0x34 | 0x35 |
| Z | 0x36 | 0x37 |

- 센서 초기화: `POWER_CTL` 레지스터(`0x2D`)의 Measure bit를 `1(0x08)`로 설정
- 기본 측정 범위: **±2g**, 분해능: **3.9mg/LSB**
- 수평 놓을 때: `X ≈ 0g, Y ≈ 0g, Z ≈ 1g` (중력이 Z축 방향으로 작용)

---

## 3. 실험 결과 및 분석

### 3-1. SPI 통신 — 디지털 신호 변환 과정

#### MCP3002 내부 변환 과정

1. **샘플 앤 홀드(Sample & Hold):** 입력 아날로그 전압을 캡처하여 변환 중 일정하게 유지
2. **축차 비교(SAR, Successive Approximation):** 기준전압(Vref) 기반 이진 탐색 방식으로 10bit 디지털 값 결정
3. **해상도:** 10bit → 0~3.3V를 **0~1023** 정수 값으로 변환

#### SPI 데이터 전송 구조

- 라즈베리파이(Master)가 시작 bit + 채널 선택 bit를 DIN으로 전송
- MCP3002가 10bit 데이터를 **2번의 8bit 전송**으로 분할하여 DOUT으로 응답
  - 첫 번째 byte: 상위 2bit (B9, B8)
  - 두 번째 byte: 하위 8bit (B7~B0)

---

### 3-2. I2C 통신 — 디지털 신호 변환 과정

I2C는 **SCL(클럭)** 과 **SDA(데이터)** 단 2선으로 여러 장치와 통신하는 동기식 직렬 프로토콜. 모든 데이터는 **8bit(1byte)** 단위로 전송.

#### 통신 순서

```
START → 장치주소(7bit) + R/W(1bit) → ACK
      → 레지스터 주소(8bit) → ACK
      → 데이터(8bit) → ACK → STOP
```

| 신호 | 역할 |
|---|---|
| START | SCL HIGH 상태에서 SDA HIGH → LOW |
| STOP | SCL HIGH 상태에서 SDA LOW → HIGH |
| ACK | Slave가 SDA를 LOW로 당겨 수신 확인 |

#### 2byte 데이터 합산 및 변환

```python
acc = (acc1 << 8) + acc0        # 16bit로 합산
if acc > 0x1FF:                 # 10bit 부호 판정 (511 초과 = 음수)
    acc = (65536 - acc) * -1    # 2의 보수 변환
acc = acc * 3.9 / 1000          # g 단위로 변환
```

**주의:** `read_byte_data()`를 2번 호출하면 두 byte 사이에 센서 내부 값이 업데이트될 수 있음. 데이터시트에서는 **Multi-byte read** 방식(`0x32`부터 연속 6byte 수신) 권장.

---

## 4. 코드별 실험 결과

### 17_SPI_01.py — SPI 기반 ADC 2채널 측정

```python
import spidev, time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000  # 1MHz
spi.bits_per_word = 8

dummy = 0xff
start = 0x47  # 0100 0111
sgl   = 0x20  # 0010 0000 (싱글 엔드 모드)
ch0   = 0x00  # 0000 0000
ch1   = 0x10  # 0001 0000
msbf  = 0x08  # 0000 1000 (MSB 퍼스트)

def measure(ch):
    ad = spi.xfer2([(start + sgl + ch + msbf), dummy])
    val = (((ad[0] & 0x03) << 8) + ad[1]) * 3.3 / 1023
    return val

try:
    while 1:
        mes_ch0 = measure(ch0)
        mes_ch1 = measure(ch1)
        print('ch0 = %2.2f' % mes_ch0, '[V], ch1 = %2.2f' % mes_ch1, '[V]')
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

spi.close()
```

**특징**
- `spidev` 라이브러리로 SPI 버스 0, 디바이스 0을 **1MHz 클럭, 8bit/word** 초기화
- 스타트 bit + 싱글 엔드 + 채널 선택 + MSB 퍼스트 비트를 조합하여 `xfer2()`로 송수신
- 수신된 2byte에서 하위 10bit 추출 후 **0~3.3V 전압**으로 환산
- 0.5초 주기로 CH0(가변저항), CH1(조도센서) 반복 측정 후 콘솔 출력
- 실험 결과: 가변저항 회전에 따라 **0~3.3V 범위에서 연속 변화** 확인

---

### 18_tk_SPI_01.py — 조이스틱으로 화면 원 이동 (GUI)

```python
import tkinter as tk, spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.bits_per_word = 8

dummy = 0xff; start = 0x47; sgl = 0x20
ch0 = 0x00; ch1 = 0x10; msbf = 0x08

root = tk.Tk()
c = tk.Canvas(root, width=500, height=500)
c.pack()
cc = c.create_oval(200, 200, 220, 220, fill='blue')

def measure(ch):
    ad = spi.xfer2([(start + sgl + ch + msbf), dummy])
    val = (((ad[0] & 0x03) << 8) + ad[1]) - 512  # 중심값 0 기준으로 보정
    return val

def movement(val):
    if val > 255:   return -10
    elif val > 63:  return -5
    elif val < -255: return 10
    elif val < -63:  return 5
    return 0

def draw():
    diff = [movement(measure(ch0)), movement(measure(ch1))]
    c.move(cc, diff[0], diff[1])
    root.after(50, draw)  # 50ms 주기 (20fps)

draw()
root.mainloop()
```

**특징**
- MCP3002 10bit 값(0~1023)을 **-512~511** 범위로 보정 (중심 = 0)
- 임계값 기반 이동량 결정: `>255 → -10px`, `>63 → -5px` (반대 방향도 동일)
- `root.after(50, draw)`로 **비블로킹 50ms 주기** 갱신

---

### 19_I2C_01.py — I2C 기반 3축 가속도 측정

```python
import smbus, time

bus = smbus.SMBus(1)
address = 0x1D
x_adr, y_adr, z_adr = 0x32, 0x34, 0x36

def init_ADXL345():
    bus.write_byte_data(address, 0x2D, 0x08)  # Measure 모드 활성화

def measure_acc(adr):
    acc0 = bus.read_byte_data(address, adr)      # 하위 byte
    acc1 = bus.read_byte_data(address, adr + 1)  # 상위 byte
    acc = (acc1 << 8) + acc0
    if acc > 0x1FF:
        acc = (65536 - acc) * -1  # 2의 보수 변환
    acc = acc * 3.9 / 1000        # g 단위 변환
    return acc

try:
    init_ADXL345()
    while 1:
        x = measure_acc(x_adr)
        y = measure_acc(y_adr)
        z = measure_acc(z_adr)
        print('X = %2.2f' % x, '[g], Y = %2.2f' % y, '[g], Z = %2.2f' % z, '[g]')
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
```

**특징**
- `smbus` 라이브러리로 I2C bus 1 사용, 슬레이브 주소 `0x1D`
- `POWER_CTL(0x2D)`에 `0x08` 기록 → 대기모드 → 측정모드 전환
- 수평 놓을 때: **Z ≈ 1g** (중력이 Z축 방향으로 작용) 확인

---

### 20_tk_I2C_01.py — ADXL345 기울기로 화면 원 이동 (GUI)

```python
import tkinter as tk, smbus

bus = smbus.SMBus(1)
address = 0x1D
x_adr, y_adr, z_adr = 0x32, 0x34, 0x36

root = tk.Tk()
c = tk.Canvas(root, width=500, height=500)
c.pack()
cc = c.create_oval(200, 200, 220, 220, fill='green')

def init_ADXL345():
    bus.write_byte_data(address, 0x2D, 0x08)

def measure_acc(adr):
    acc0 = bus.read_byte_data(address, adr)
    acc1 = bus.read_byte_data(address, adr + 1)
    acc = (acc1 << 8) + acc0
    if acc > 0x1FF:
        acc = (65536 - acc) * -1
    return acc * 3.9 / 1000

def movement(val):
    if val > 0.5:    return 10
    elif val > 0.2:  return 5
    elif val < -0.5: return -10
    elif val < -0.2: return -5
    return 0  # 데드존: ±0.2g 이내 정지

def draw():
    x = measure_acc(x_adr) * -1  # X축 방향 반전 (직관적 이동 방향 일치)
    y = measure_acc(y_adr)
    c.move(cc, movement(x), movement(y))
    root.after(50, draw)

init_ADXL345()
draw()
root.mainloop()
```

**특징**
- 18번 조이스틱 코드와 구조 동일, 아날로그 전압 대신 **센서 기울기(g)** 로 제어
- 데드존: **±0.2g 이내 정지** (약 12° 이하)
- 빠른 이동: **±0.5g 초과** (약 30° 이상)
- X축에 `-1` 적용 → 센서 기울기 방향과 화면 이동 방향 일치

---

### 19_I2C_01_tilt.py — 기울임 각도(Tilt Angle) 계산

```python
import smbus, time, math

bus = smbus.SMBus(1)
address = 0x53  # SDO=GND → 0x53
x_adr, y_adr, z_adr = 0x32, 0x34, 0x36

def init_ADXL345():
    bus.write_byte_data(address, 0x2D, 0x08)

def measure_acc(adr):
    acc0 = bus.read_byte_data(address, adr)
    acc1 = bus.read_byte_data(address, adr + 1)
    acc = (acc1 << 8) + acc0
    if acc > 0x1FF:
        acc = (65536 - acc) * -1
    return acc * 3.9 / 1000

def calculate_tilt_angles(x, y, z):
    # Roll:  X축 기준 회전각
    roll  = math.atan2(x, math.sqrt(y**2 + z**2))
    # Pitch: Y축 기준 회전각
    pitch = math.atan2(y, math.sqrt(x**2 + z**2))
    return math.degrees(roll), math.degrees(pitch)

try:
    init_ADXL345()
    while True:
        x = measure_acc(x_adr)
        y = measure_acc(y_adr)
        z = measure_acc(z_adr)
        roll, pitch = calculate_tilt_angles(x, y, z)
        print(f'X={x:6.3f}[g], Y={y:6.3f}[g], Z={z:6.3f}[g]')
        print(f'Roll={roll:6.1f}°, Pitch={pitch:6.1f}°')
        print('-' * 50)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
```

**특징**
- `atan2(y, x)` 사용: 분모가 0이 되는 경우(90°)에도 안전하게 처리, 사분면 정확히 구분
- 기울임 원리:

$$Z = \cos(\theta), \quad X = \sin(\theta) \quad \Rightarrow \quad \theta = \arctan\left(\frac{X}{Z}\right)$$

---

## 5. Discussion

### SPI vs I2C 비교

| 항목 | SPI | I2C |
|---|---|---|
| 신호선 수 | 4선 (MOSI, MISO, SCLK, CS) | 2선 (SDA, SCL) |
| 통신 방식 | 전이중(Full-Duplex) | 반이중(Half-Duplex) |
| 장치 구별 | CS 핀으로 구별 | 7bit 주소로 구별 |
| 속도 | 빠름 (수십 MHz) | 느림 (100kHz~1MHz) |
| 배선 복잡도 | 장치 추가 시 CS 핀 증가 | 배선 변경 없이 주소만 추가 |

### Roll-Pitch-Yaw 중 가속도계로 측정 가능한 각도

| 각도 | 측정 가능 여부 | 이유 |
|---|---|---|
| Roll (X축 기준 회전) | ✅ | 회전 시 각 축의 중력 분배가 변화 |
| Pitch (Y축 기준 회전) | ✅ | 회전 시 각 축의 중력 분배가 변화 |
| Yaw (Z축 기준 회전) | ❌ | Z축 회전 시 중력 방향 불변 → Z ≈ 1g 유지 |

Yaw 측정을 위해서는 **자이로스코프(Gyroscope)** 또는 **지자기 센서(Magnetometer)** 가 필요하다.

### `read_byte_data()` 2회 호출의 잠재적 문제

두 byte를 개별 호출로 읽으면 그 사이에 센서 내부 값이 갱신될 경우 **하위/상위 byte가 서로 다른 시점의 데이터**가 될 수 있다. 데이터시트에서는 레지스터 `0x32`부터 6byte를 연속 수신하는 **Multi-byte read** 방식을 권장한다.
