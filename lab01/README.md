# 실습보고서 #1

> **실습일:** 2026-04-01
> **실습 환경:** Raspberry Pi 4 Model B + GPIO

---

## 1. 실험 목표 및 목적

Raspberry Pi 4 Model B의 GPIO 핀을 활용하여 LED를 제어하는 과정을 통해 디지털 신호 기반의 하드웨어 제어 원리를 이해한다.

- LED의 전기적 특성(전압, 전류)을 분석하고, 적절한 저항을 설계·적용하여 안전한 회로 구성 방법 학습
- 스위치를 이용한 입력 제어와 PWM(Pulse Width Modulation) 신호를 활용한 출력 제어 실습
- 단순 On/Off 제어를 넘어 다양한 신호 제어 방식과 임베디드 시스템의 기본 개념 습득

---

## 2. 실험 진행 과정

### 2-1. LED 회로 구성

- **연결:** 11번 헤더 핀(GPIO 17) → 1.3 kΩ 저항 → LED → 9번 핀(GND)
- **부하선 분석:** LED 데이터시트의 Forward current vs. Forward voltage 그래프에 부하선을 그어 동작점 도출

$$I = \frac{3.3V - V_{LED}}{1300\Omega}$$

- 교점에서 읽은 $V_{LED} = 1.8V$
- $V_{저항} = 3.3V - 1.8V = 1.5V$
- $I = \frac{1.5V}{1300\Omega} \approx 1.15mA$
- 최대 정격 전류 30mA 대비 현저히 작아 LED 밝기가 어두움

### 2-2. 스위치 + LED 회로 구성

- **풀업 회로:** 1번 핀(3.3V) → 10 kΩ 풀업 저항 → 7번 핀(GPIO 4), 스위치는 7번 핀과 9번 핀(GND) 사이 연결
- **LED 회로:** 11번 헤더 핀(GPIO 17) → 1.3 kΩ 저항 → LED → 9번 핀(GND)

| 스위치 상태 | 7번 핀 전위 | 입력값 |
|---|---|---|
| Up (열림) | 3.3V | 1 (HIGH) |
| Down (눌림) | 0V (전압강하) | 0 (LOW) |

---

## 3. 코드별 실험 결과

### 01_LED_01.py — `while`문 기반 LED 점멸

```python
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=0)

try:
    while True:
        GPIO.output(11, 1)  # ON
        time.sleep(0.5)
        GPIO.output(11, 0)  # OFF
        time.sleep(0.5)
except: pass

GPIO.cleanup()
```

**특징**
- 무한 루프(`while`)를 통한 자동 점멸 구현
- `sleep(0.5)`으로 0.5초 간격 깜빡임 제어
- 종료 시 `cleanup()`으로 핀 설정 초기화

---

### 02_tk_LED_01.py — GUI 버튼으로 LED 토글

```python
import RPi.GPIO as GPIO, tkinter as tk

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=0)

def func():
    GPIO.output(11, not GPIO.input(11))  # 현재 상태 반전

root = tk.Tk()
tk.Button(root, text='LED', command=func).pack()

root.mainloop()
GPIO.cleanup()
```

**특징**
- 루프 없이 버튼 클릭 시에만 로직 수행 (GUI 이벤트 기반)
- `not GPIO.input(11)`: 별도 변수 없이 현재 핀 상태 읽어 반전 출력

---

### 03_LED_02.py — PWM으로 밝기 Fade in/out

```python
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 100)  # 100Hz
p.start(0)

dc = [0, 1, 2, 3, 4, 5, 10, 20, 30, 50, 70, 100]

try:
    while True:
        for v in dc:
            p.ChangeDutyCycle(v)
            time.sleep(0.1)
        dc.reverse()  # 밝기 변화 방향 반전
except: pass

p.stop()
GPIO.cleanup()
```

**특징**
- PWM 주파수: **100Hz** → 주기 10ms
- 듀티비 70일 때: HIGH 시간 = **7ms**
- `dc.reverse()`로 Fade in → Fade out 반복 구현

> **PWM을 사용하는 이유:** GPIO는 HIGH(3.3V)/LOW(0V) 두 상태만 출력 가능. PWM은 HIGH/LOW를 빠르게 전환하면서 HIGH 비율(듀티비)을 조절해 아날로그처럼 밝기 제어 가능.

---

### 04_tk_LED_02.py — GUI 슬라이더로 PWM 밝기 제어

```python
import RPi.GPIO as GPIO, tkinter as tk

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 100)
p.start(0)

def change_duty(dc):
    p.ChangeDutyCycle(float(dc))

root = tk.Tk()
tk.Scale(root, label='LED', orient='h', from_=0, to=100,
         command=change_duty).pack()

root.mainloop()
p.stop()
GPIO.cleanup()
```

**특징**
- `Scale` 위젯으로 듀티비 0~100 실시간 조절
- `command` 옵션으로 슬라이더 값 변경 시 즉시 PWM 반영

---

### 05_Switch_01.py — 스위치로 LED 제어 (폴링 방식)

```python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

SW = 7
LED = 11

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SW, GPIO.IN)

while 1:
    key_in = GPIO.input(SW)

    if key_in == 0:          # 스위치 눌림
        GPIO.output(LED, GPIO.HIGH)
    else:                    # 스위치 안 눌림
        GPIO.output(LED, GPIO.LOW)
```

**특징**
- 폴링 방식: `while`문으로 지속적으로 스위치 상태 확인 → CPU 사용률 증가
- GPIO 입력 → 즉시 출력, 단순한 구조

---

### 06_tk_Switch_01.py — 스위치 + GUI 시각화 (이벤트 기반)

```python
import RPi.GPIO as GPIO, tkinter as tk

GPIO.setmode(GPIO.BOARD)

SW = 7
LED = 11

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀업 저항 설정

root = tk.Tk()
c = tk.Canvas(root, width=200, height=200)
c.pack()
cc = c.create_oval(50, 50, 150, 150, fill='')

def check_SW(channel):
    key_in = GPIO.input(channel)

    if key_in == 0:       # 스위치 눌림
        GPIO.output(LED, GPIO.HIGH)
        c.itemconfig(cc, fill='red')
    else:                 # 스위치 안 눌림
        GPIO.output(LED, GPIO.LOW)
        c.itemconfig(cc, fill='')

GPIO.add_event_detect(SW, GPIO.BOTH, callback=check_SW)

root.mainloop()
GPIO.cleanup()
```

**특징**
- 이벤트 기반: 상태 변화 시에만 `check_SW` 실행 → CPU 효율적
- `GPIO.PUD_UP`: 소프트웨어 풀업 저항 설정 (기본 HIGH)
- Canvas 원 색상으로 LED 상태 시각화

| 스위치 | LED | GUI 원 |
|---|---|---|
| Up (안 눌림) | OFF | 투명 |
| Down (눌림) | ON | 빨강 |

---

## 4. 에러 발생 및 해결

### `lgpio.error: 'GPIO busy'`

**원인:** `except KeyboardInterrupt: pass`로 인해 `GPIO.cleanup()`이 실행되지 않으면, 이전 프로세스가 GPIO를 계속 점유함

**해결 방법:**

```bash
# 1. GPIO를 점유 중인 Python 프로세스 확인
ps -ef | grep python

# 2. 해당 PID 강제 종료
sudo kill -9 <PID>
# 예시: sudo kill -9 1234
```

**예방:** 코드 작성 시 항상 아래 패턴 적용

```python
except KeyboardInterrupt:
    pass

p.stop()        # PWM 사용 시
GPIO.cleanup()  # 반드시 실행되도록 배치
```

---

## 5. Discussion — 06_tk_Switch_01.py 응용

기존 06번 코드의 원(Circle)을 **별(Star)** 모양으로 변형한 응용 예제

**파일:** [`06_tk_Switch_01.py (star)`](https://github.com/MEEEJEEE/mechatronics-playground/blob/main/06_tk_Switch_01.py%20(star))

```python
points = [
    100, 40,   # 위 꼭짓점
    120, 90,
    170, 90,
    130, 120,
    150, 170,
    100, 140,
    50, 170,
    70, 120,
    30, 90,
    80, 90
]

cc = c.create_polygon(points, fill='')

def check_SW(channel):
    key_in = GPIO.input(channel)
    if key_in == 0:
        GPIO.output(LED, GPIO.HIGH)
        c.itemconfig(cc, fill='yellow')  # 별 노란색
    else:
        GPIO.output(LED, GPIO.LOW)
        c.itemconfig(cc, fill='')        # 별 투명
```

### 발생한 문제 및 원인 분석

| 문제 | 원인 |
|---|---|
| 실행 시 별이 보이지 않음 | 초기 `fill=''`(투명) 상태 + 이벤트 기반 구조 |

- `cc = c.create_polygon(points, fill='')` → 별은 존재하지만 투명
- `GPIO.add_event_detect`는 스위치 상태 **변화 시에만** 함수 실행
- 따라서 프로그램 시작 직후 스위치 이벤트 없이는 별이 나타나지 않음 (정상 동작)
- 스위치를 누르거나 떼야 비로소 `check_SW`가 호출되어 별이 표시됨
