# 실습보고서 #3

> **실습일:** 2026-04-15
> **실습 환경:** Raspberry Pi 4 Model B + L298N(DC 모터) + 28BYJ-48(스테핑 모터) + 서보 모터
> **실습 영상:** [lab03_media 다운로드](https://github.com/MEEEJEEE/mechatronics-playground/releases/tag/lab03-media)

---

## 1. 실험 목표 및 목적

### 모터 제어 원리 학습
- 전기 모터의 기본 동작 원리 이해: 속도는 인가 전압에 비례, 토크는 전류에 비례
- PWM(Pulse Width Modulation) 제어 원리: 듀티비(Duty Ratio), 주기(Period), 주파수(Frequency)가 출력 전압에 미치는 영향 이해

### 실습 목표

| 항목 | 내용 |
|---|---|
| PWM 기반 모터 제어 | 듀티비 조절로 평균 전압 변화 → 모터 속도 제어 |
| 유효 전압 개념 | 12V 입력, 듀티비 10% → 평균 출력 전압 1.2V |
| 다양한 모터 비교 | DC 모터 / 스테퍼 모터 / 서보 모터 제어 방식 차이 이해 |

---

## 2. 실험 진행 과정 및 배경 개념

### 2-1. DC 모터

#### 구조

| 구성요소 | 역할 |
|---|---|
| 고정자(Stator) | 외곽의 영구자석, 일정한 자기장 형성 |
| 회전자(Rotor/Armature) | 전류가 흐르는 코일 뭉치, 중심축에서 회전 |
| 정류자(Commutator) + 브러시(Brush) | 코일의 전류 방향을 주기적으로 반전 → 한 방향 연속 회전 유지 |

#### 구동 원리 — 플레밍의 왼손 법칙

1. 브러시/정류자를 통해 회전자 코일에 전류 인가
2. 자기장 속 전류 → 로런츠 힘 발생
3. 코일 양쪽 면이 반대 방향의 힘을 받아 회전 토크 발생
4. 180° 회전마다 정류자가 전류 방향 반전 → 계속 한 방향으로 회전

#### 모터 드라이버 IC (L298N) 사용 이유

- **전류 증폭:** GPIO 핀 최대 출력 전류 약 16mA → 모터 구동 전류 부족. 외부 전원을 모터에 공급하는 징검다리 역할
- **H-브리지 내장:** 전류 방향 전환으로 정/역회전 구현
- **보호 회로:** 역기전력 차단 다이오드 내장 → 라즈베리파이 보호
- **논리/구동 회로 분리:** 3.3V 제어 신호로 5V~12V 이상의 모터 제어 가능

#### H-브리지 동작 원리

| 스위치 상태 | AIN1 | AIN2 | 결과 |
|---|---|---|---|
| S1 + S4 ON | HIGH | LOW | 정회전 |
| S2 + S3 ON | LOW | HIGH | 역회전 |
| 모두 OFF | LOW | LOW | 정지 |

#### PWM 제어

```
듀티비 0%   → 모터 정지
듀티비 50%  → 절반 속도
듀티비 100% → 최대 속도
```

본 실험: **100Hz** 주파수, **10% 단위**로 듀티비 변화

---

### 2-2. 스테핑 모터 (28BYJ-48)

외부 디지털 펄스 신호에 동기화하여 **일정 각도씩 회전**하는 전동기. 피드백 제어 없이도 회전 각도와 속도를 정밀하게 제어 가능.

#### 구조

| 구성요소 | 역할 |
|---|---|
| 회전자(Rotor) | 영구자석, 중심축에 연결 |
| 고정자(Stator) | 코일(권선)이 감긴 전자석, 회전자를 인력/척력으로 제어 |
| 감속 기어 | 28BYJ-48 내장, 작은 회전력을 정밀하고 강한 힘으로 변환 |

#### DC 모터 vs 스테핑 모터 비교

| 항목 | 스테핑 모터 | DC 모터 |
|---|---|---|
| 제어 방식 | 디지털 펄스 (개별 스텝) | 아날로그 전압 (연속 회전) |
| 위치 제어 | 매우 정밀 (오픈 루프 가능) | 별도 센서 없이 정밀 제어 불가 |
| 회전 속도 | 저속에서 높은 토크 | 고속 회전에 유리 |
| 정지 유지 | 유지 토크(Holding Torque) 있음 | 전원 차단 시 관성에 의해 회전 후 정지 |
| 주요 용도 | 3D 프린터, 로봇 관절, CNC | 선풍기, RC카, 드론 프로펠러 |

---

### 2-3. 서보 모터

#### 내부 구조 — 폐루프 제어(Closed-loop Control)

- **가변 저항:** 모터 축 회전 시 저항값 변화 → 현재 각도를 전기 신호로 제어부에 전달
- **제어 회로:** 목표 각도 신호 vs 현재 각도 신호 비교 → 일치할 때까지 모터 구동, 일치하면 정지

#### 제어 방식 — PWM

전압 크기가 아닌 **펄스 폭(Pulse Width)** 으로 명령을 받음. 표준 주파수 **50Hz**, 듀티비에 따라 각도 결정.

---

## 3. 코드별 실험 결과

### 07_Motor_01.py — DC 모터 자동 가감속 + 방향 전환

```python
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
AIN1, AIN2, PWMA = 13, 15, 12
GPIO.setup([AIN1, AIN2], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PWMA, GPIO.OUT)

p = GPIO.PWM(PWMA, 100)  # 100Hz
p.start(0)

try:
    while True:
        GPIO.output(AIN1, GPIO.HIGH); GPIO.output(AIN2, GPIO.LOW)  # 정방향
        for pw in range(0, 101, 10):
            p.ChangeDutyCycle(pw); time.sleep(0.5)
        for pw in range(100, -1, -10):
            p.ChangeDutyCycle(pw); time.sleep(0.5)
        time.sleep(0.5)

        GPIO.output(AIN1, GPIO.LOW); GPIO.output(AIN2, GPIO.HIGH)  # 역방향
        for pw in range(0, 101, 10):
            p.ChangeDutyCycle(pw); time.sleep(0.5)
        for pw in range(100, -1, -10):
            p.ChangeDutyCycle(pw); time.sleep(0.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

p.stop(); GPIO.cleanup()
```

**특징**
- PWM 주파수 **100Hz**, 듀티비 **10% 단위**로 0→100→0 반복
- 정방향 → 0.5초 정지 → 역방향 무한 반복
- 실험 결과: 서서히 가속 후 감속, 정지, 역방향 동일 동작 확인

---

### 08_tk_Motor_01.py — DC 모터 GUI 제어 (슬라이더)

```python
import RPi.GPIO as GPIO, tkinter as tk

GPIO.setmode(GPIO.BOARD)
AIN1, AIN2, PWMA = 13, 15, 12
GPIO.setup([AIN1, AIN2, PWMA], GPIO.OUT, initial=GPIO.LOW)
p = GPIO.PWM(PWMA, 100); p.start(0)

dir = tk.IntVar(); spd = tk.IntVar()

def change_dir(dr):
    val = dir.get()
    if val == 0:    GPIO.output(AIN1, GPIO.LOW);  GPIO.output(AIN2, GPIO.HIGH)  # 시계
    elif val == 1:  GPIO.output(AIN1, GPIO.LOW);  GPIO.output(AIN2, GPIO.LOW)   # 정지
    elif val == 2:  GPIO.output(AIN1, GPIO.HIGH); GPIO.output(AIN2, GPIO.LOW)   # 반시계

def change_pw(pw):
    p.ChangeDutyCycle(spd.get())

root = tk.Tk()
tk.Scale(root, label='Direction', from_=0, to=2, variable=dir, command=change_dir).pack()
tk.Scale(root, label='Speed',     from_=0, to=100, variable=spd, command=change_pw).pack()

root.mainloop()
p.stop(); GPIO.cleanup()
```

**특징**
- `Direction` 슬라이더: 0(시계) / 1(정지) / 2(반시계) 3단계 방향 제어
- `Speed` 슬라이더: 0~100 듀티비 실시간 반영
- 실험 결과: GUI 조작에 따라 방향 즉각 변경, 속도 선형 변화 확인

---

### 09_Motor_02.py — 스테핑 모터 자동 제어 (1상 여자)

```python
from collections import deque
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
AIN1, BIN1, AIN2, BIN2 = 15, 16, 18, 22
GPIO.setup([AIN1, BIN1, AIN2, BIN2], GPIO.OUT, initial=GPIO.LOW)

sig = deque([1, 0, 0, 0])  # 1상 여자 신호 패턴
step = 100
dir = 1  # 1: 정방향, -1: 역방향

try:
    while 1:
        for cnt in range(0, step):
            GPIO.output(AIN1, sig[0]); GPIO.output(BIN1, sig[1])
            GPIO.output(AIN2, sig[2]); GPIO.output(BIN2, sig[3])
            time.sleep(0.01)   # 10ms 간격
            sig.rotate(dir)    # 패턴 한 칸 회전
        dir = dir * -1         # 100스텝마다 방향 전환
except KeyboardInterrupt:
    pass

GPIO.cleanup()
```

**특징**
- `deque([1, 0, 0, 0])`: 한 번에 코일 1개만 자화 (1상 여자)
- `sig.rotate(dir)`: 패턴을 한 칸씩 밀어 코일 순차 활성화 → 회전
- 스텝 간격 **10ms**, 100스텝마다 방향 자동 전환

---

### 10_tk_Motor_02.py — 스테핑 모터 GUI 제어 (입력 스텝 수)

```python
from collections import deque
import RPi.GPIO as GPIO, tkinter as tk, time

GPIO.setmode(GPIO.BOARD)
AIN1, BIN1, AIN2, BIN2 = 15, 16, 18, 22
GPIO.setup([AIN1, BIN1, AIN2, BIN2], GPIO.OUT, initial=GPIO.LOW)

sig = deque([1, 0, 0, 0])
dir = tk.IntVar(value=1)

root = tk.Tk()
tk.Radiobutton(root, text='CW',  variable=dir, value=1).pack()   # 시계 방향
tk.Radiobutton(root, text='CCW', variable=dir, value=-1).pack()  # 반시계 방향
e = tk.Entry(root); e.pack()  # 스텝 수 입력

def rot_mtr():
    for cnt in range(0, int(e.get())):
        GPIO.output(AIN1, sig[0]); GPIO.output(BIN1, sig[1])
        GPIO.output(AIN2, sig[2]); GPIO.output(BIN2, sig[3])
        time.sleep(0.01)
        sig.rotate(dir.get())

tk.Button(root, text='rotate', command=rot_mtr).pack()
root.mainloop()
GPIO.cleanup()
```

**특징**
- 라디오 버튼으로 CW(1) / CCW(-1) 방향 선택
- Entry 위젯으로 스텝 수 직접 입력 → 입력한 스텝만큼 정확히 이동
- 이벤트 기반: 버튼 클릭 시에만 구동 → 무한 루프 없이 효율적

---

### 11_Motor_03.py — 서보 모터 자동 왕복

```python
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

freq = 50.0      # 서보 표준 주파수
dc_min = 2.5     # 0도
dc_max = 12.5    # 180도
deg_min, deg_max = 0.0, 180.0

p = GPIO.PWM(12, freq); p.start(0)

def convert_dc(deg):
    return (deg - deg_min) * (dc_max - dc_min) / (deg_max - deg_min) + dc_min

try:
    while 1:
        for deg in range(0, 181, 1):    # 0→180도, 1도 단위
            p.ChangeDutyCycle(convert_dc(float(deg))); time.sleep(0.01)
        for deg in range(180, -1, -1):  # 180→0도
            p.ChangeDutyCycle(convert_dc(float(deg))); time.sleep(0.01)
except KeyboardInterrupt:
    pass

p.stop(); GPIO.cleanup()
```

**특징**
- 각도 → 듀티비 선형 변환: `dc = (deg / 180) * (12.5 - 2.5) + 2.5`
- 1도 단위, 10ms 간격으로 부드러운 왕복 구현

#### ✴︎ 에러 발생 및 해결 — 서보 모터 흔들림

**원인**

| 문제 | 내용 |
|---|---|
| 소프트웨어 PWM 불안정 | OS 스케줄링 영향 → 신호 불규칙 → 흔들림 발생 |
| 비표준 주파수 | 100Hz 사용 → 서보 표준(50Hz)의 2배, 내부 회로 해석 오류 |
| 잘못된 듀티비 범위 | `dc_min=5.0 / dc_max=22.0` → 실제 0~180도 동작 범위 벗어남 |

**수정 내용**

| 항목 | 수정 전 | 수정 후 |
|---|---|---|
| 주파수 | 100Hz | **50Hz** (서보 표준) |
| dc_min | 5.0 | **2.5** |
| dc_max | 22.0 | **12.5** |
| 스텝 단위 | 10도 | **1도** |
| 대기 시간 | 1초 | **0.01초** |

---

### 12_tk_Motor_03.py — 서보 모터 GUI 제어 (슬라이더)

```python
import RPi.GPIO as GPIO, tkinter as tk

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

freq = 100.0; dc_min = 5.0; dc_max = 22.0
deg_min, deg_max = 0.0, 180.0

p = GPIO.PWM(12, freq); p.start(0)
deg = tk.DoubleVar(); deg.set(0)

def change_dc(dum):
    dc = (deg.get() - deg_min) * (dc_max - dc_min) / (deg_max - deg_min) + dc_min
    p.ChangeDutyCycle(dc)

root = tk.Tk()
tk.Scale(root, label='Angle', orient='h',
         from_=0, to=180, variable=deg, command=change_dc).pack()

root.mainloop()
p.stop(); GPIO.cleanup()
```

**특징**
- 슬라이더로 0~180도 실시간 각도 제어
- `command=change_dc`: 슬라이더 값 변경 시 즉시 듀티비 갱신
- 무한 루프 없이 이벤트 기반 동작

---

## 4. Discussion

### deque와 스택/큐 자료구조

스테핑 모터 코드(09, 10번)에서 `collections.deque` 사용.

| 자료구조 | 방식 | 특징 | 활용 예 |
|---|---|---|---|
| 스택(Stack) | LIFO (후입선출) | 한쪽 끝에서만 삽입/삭제 | 뒤로 가기, Call Stack, Undo |
| 큐(Queue) | FIFO (선입선출) | 한쪽 삽입, 반대쪽 삭제 | 프린터 스풀, 프로세스 스케줄링 |
| **deque** | **양방향** | 양쪽 끝 삽입/삭제 + **rotate() 기능** | 스테핑 모터 신호 패턴 제어 |

```python
# deque rotate() 핵심 동작
sig = deque([1, 0, 0, 0])
sig.rotate(1)  # → [0, 1, 0, 0]
sig.rotate(1)  # → [0, 0, 1, 0]
sig.rotate(1)  # → [0, 0, 0, 1]
sig.rotate(1)  # → [1, 0, 0, 0]  (원점 복귀)
```

`[1, 0, 0, 0]` 패턴을 유지하면서 순서만 바꿔야 하므로, 일반 리스트보다 deque가 메모리 효율과 속도 면에서 유리.

---

### 트랜지스터 어레이 IC 사용 이유

- **구동 전류 증폭:** GPIO 출력 전류(약 16mA)로는 모터 직접 구동 불가 → IC가 큰 전류 제어
- **다채널 통합:** 여러 트랜지스터를 IC 하나로 대체 → 회로 간소화
- **내장 보호 다이오드:** 유도성 부하(모터) 역기전력(Back EMF) 흡수
- **논리/구동 분리:** 3.3V 신호로 더 높은 전압의 모터 제어 가능
