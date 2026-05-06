# Lec07 — Sensors (센서)

> Chapter 9 | 스트레인 게이지·휘트스톤 브리지 기출 15점

---

## 1. 센서 기본 특성

| 용어 | 정의 |
|---|---|
| **정확도 (Accuracy)** | 측정값이 참값에 얼마나 가까운가 |
| **정밀도 (Precision)** | 반복 측정 시 결과의 일관성 |
| **분해능 (Resolution)** | 감지할 수 있는 최소 변화량 |
| **선형성 (Linearity)** | 출력이 입력에 비례하는 정도 |
| **감도 (Sensitivity)** | 단위 입력당 출력 변화량 |

---

## 2. 센서 종류 분류

| 카테고리 | 주요 센서 |
|---|---|
| 위치/변위 | Potentiometer, Encoder, Hall Effect, LVDT |
| 근접/동작 | Ultrasonic, PIR (Passive Infrared), Optical Slotted |
| 관성 | Accelerometer, Gyroscope, MEMS |
| 압력/힘 | Strain Gauge, IC Barometer, LVDT |
| 광학 | LDR, Photodiode, Phototransistor |
| 온도 | Thermocouple, RTD, Thermistor (NTC/PTC) |

---

## 3. 스트레인 게이지 (Strain Gauge) ★출제·계산

변형(Strain) `ε = ΔL/L`을 저항 변화로 감지. 대표 응용: Load Cell(로드셀)

```
저항: R = ρL/A  (ρ: 비저항, L: 길이, A: 단면적)

변형 시 저항 변화:
  dR/R = ε_axial(1 + 2ν) + dρ/ρ
  (ν = Poisson's ratio, 기하학적 변화만 고려 시 dρ/ρ = 0)

Gauge Factor:
  F = (ΔR/R) / ε_axial
  기하학적 변화만 고려: F = 1 + 2ν  (일반적 F ≈ 2)
  ν=0.5이면: F = 1 + 2(0.5) = 2

저항 변화량: ΔR = F × R × ε
```

**기출 계산 예시:**
```
ν=0.5 → Gauge Factor = 1 + 2(0.5) = 2
ε=+0.25, R=10kΩ → ΔR = 2 × 10k × 0.25 = 5kΩ
새 저항 = 10k + 5k = 15kΩ
```

---

## 4. 휘트스톤 브리지 (Wheatstone Bridge) ★출제·계산

미세한 저항 변화(ΔR)를 전압으로 변환하는 회로. 스트레인 게이지 신호 읽기에 필수.

```
일반 출력 전압 (쿼터 브리지, 게이지 1개):
  ΔVout/Vex = (R1+ΔR1)/(R1+ΔR1+R4) − R2/(R2+R3)

단순화 (모든 저항=R, 하나만 R+ΔR, ΔR << R 근사):
  Vout ≈ Vex × ΔR/(4R)

정확한 계산 (쿼터 브리지):
  V1 = Vex × (R+ΔR)/(2R+ΔR)
  V2 = Vex/2
  Vout = V1 − V2
```

**기출 계산:**
```
Vex=5V, R=10kΩ, 게이지 저항=15kΩ (ΔR=5kΩ)
  V1 = 5 × 15k/(15k+10k) = 5 × 15/25 = 3V
  V2 = 5 × 10k/(10k+10k) = 2.5V
  Vout = V1 − V2 = 0.5V  (이후 차동 증폭기로 증폭)
```

| 브리지 구성 | 게이지 수 | 감도 | 특징 |
|---|---|---|---|
| 쿼터 브리지 (Quarter) | 1개 | 기준 | 기본 구성 |
| 하프 브리지 (Half) | 2개 | 2배 | 온도 보상 가능 |
| 풀 브리지 (Full) | 4개 | 4배 | 완전 온도 보상. Load Cell 구조 |

---

## 5. 온도 센서 ★출제

| 종류 | 원리 | 특징 | 정밀도 |
|---|---|---|---|
| **RTD (PT100)** | 온도에 따른 저항 변화 (선형) | 정확도 높음, 선형적 | ±0.3°C |
| **Thermistor** | 온도에 따른 저항 변화 (지수함수) | 민감하지만 비선형 | `R = R₀·e^β(1/T−1/T₀)` |
| **Thermocouple** | Seebeck 효과 (서로 다른 금속 접합) | 넓은 측정 범위, 기준접점 필요 | `V = α(T1−T2)` |

### NTC / PTC Thermistor

| 종류 | 특성 | 전압 분배기에서 온도 ↑ 시 |
|---|---|---|
| **NTC** (Negative Temp. Coeff.) | 온도 ↑ → 저항 ↓ | R_NTC ↓ → Vout ↓ |
| **PTC** (Positive Temp. Coeff.) | 온도 ↑ → 저항 ↑ | R_PTC ↑ → Vout ↑ |
| CTR | 특정 온도에서 급격히 저항 감소 | — |

> **기출 T/F:** "NTC 서미스터 전압 분배기에서 온도↑ → 출력전압↑" → **False**  
> NTC는 온도↑ → 저항↓ → (R_NTC가 하단이면) 분배비 감소 → Vout 감소

---

## 6. 위치/변위 센서

### 광 엔코더 (Optical Encoder)

슬롯 디스크 + LED + 포토셀 구성. 디지털 펄스로 각도·속도 측정.

| 종류 | 특성 |
|---|---|
| **Incremental** | 상대 위치 (펄스 카운팅). A·B 채널로 방향 구분. INDEX 채널로 기준점 |
| **Absolute** | 절대 위치. 전원 꺼도 위치 기억 |

### LVDT (Linear Variable Differential Transformer)

- 자기 유도 방식 선형 변위 측정
- 비접촉, 고정밀, 마모 없음

---

## 7. 가속도·자이로 센서 (MEMS) ★중요

| 센서 | 측정량 | 방식 | 비고 |
|---|---|---|---|
| **가속도계 (Accelerometer)** | 선형 가속도 (정적+동적 모두) | MEMS 용량 변화 | 예) ADXL150: 단축, ±50G, 분해능 10mG |
| **자이로스코프 (Gyroscope)** | 각속도 (Angular Velocity) | 코리올리 힘 → 용량 변화 | 종류: Ring Laser, Fiber Optic, MEMS |

**IMU** = 가속도계 + 자이로스코프 (+ 자력계)

---

## 8. 레이저 삼각측량 (Laser Triangulation)

- 레이저 빔 조사 → 반사광 위치를 CCD/CMOS로 감지 → 삼각법으로 거리·변위 계산
- 비접촉 방식. 고속 측정 가능. 표면 반사율에 영향 받을 수 있음.

---

## 9. 기출 연계 핵심 흐름 정리 ★출제

```
기출 P8→P9 연계 계산 전체 흐름:

1. Gauge Factor: ν=0.5 → F = 1+2(0.5) = 2
2. 새 저항: ε=+0.25, R=10kΩ → ΔR = 2×10k×0.25 = 5kΩ → R_new = 15kΩ
3. 브리지 출력: Vex=5V, 10kΩ 3개, 15kΩ 게이지
     V1 = 5×15/25 = 3V,  V2 = 2.5V,  Vout = 0.5V
4. 차동 증폭기: R=10kΩ, Rf=20kΩ → Vout = (Rf/R)(V2−V1) 계산
5. 범위: ε=−17%~+25% → 저항 범위 → 브리지 출력 범위 → 증폭 후 범위
6. ADC 보호 회로: 5V ADC 범위 초과 방지
     → Voltage Clamp (Zener 또는 Voltage Divider)
```
