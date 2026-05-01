# Lec06 — Actuators (모터)

> Chapter 10 | 모터 종류별 원리, PWM, H-Bridge

---

## 1. DC 브러시드 모터 (Brushed DC Motor) ★중요

**원리:** 전류 흐르는 코일이 자기장 안에서 로렌츠 힘(`F = BIL`) 받아 회전.  
브러시(Brush)와 정류자(Commutator)로 전류 방향 자동 전환.

| 특성 | 단점 |
|---|---|
| 속도 ∝ 인가 전압 | 브러시 마모 → 수명 제한 |
| 토크 ∝ 전류 | 전기적 노이즈 발생 |
| 속도 제어: 전압 조절 또는 PWM | BLDC보다 효율 낮음 |

---

## 2. H-Bridge ★출제

DC 모터의 정방향·역방향 제어 회로. 트랜지스터 4개(A, B, C, D)로 구성.

| 상태 | 활성 스위치 | 결과 |
|---|---|---|
| 정방향 | B·C close, A·D open | 모터 정회전 |
| 역방향 | A·D close, B·C open | 모터 역회전 |
| 정지 | 모두 open 또는 close | 자유회전 또는 제동 |

**TA8080K:** 내장 H-Bridge IC + 단락 보호 기능  
트루스 테이블: `DI1=H, DI2=L → M(+)=H, M(-)=L` (정방향)

---

## 3. PWM (Pulse Width Modulation) ★출제

디지털 신호로 아날로그 전압을 모사하는 방법. 모터 속도, LED 밝기 제어에 사용.

```
V_avg = V_supply × Duty Cycle

Duty Cycle = t_high / T_cycle  (0~100%)

예) 12V, Duty 10% → V_avg = 12 × 0.1 = 1.2V
예) 12V, Duty 50% → V_avg = 12 × 0.5 = 6.0V
```

> 모터 속도 ∝ 평균 전압 ∝ Duty Cycle. DAC 없이 아날로그 전압 효과를 디지털로 구현.

---

## 4. BLDC 모터 (Brushless DC) ★중요

- 브러시 없음 → 수명 길고 효율 높음
- **ESC(Electronic Speed Controller)** 로 전자 정류

| 종류 | 특성 | 용도 |
|---|---|---|
| **Inrunner** | 로터가 내부에서 회전. 고속 저토크 | 드론, RC카 |
| **Outrunner** | 로터가 외부를 감싸며 회전. 저속 고토크 | 드론 프로펠러 |

**위치 감지:** 홀 센서(Hall Sensor) 또는 광 엔코더 → 로터 위치 파악 → 정확한 전류 전환

---

## 5. 스테퍼 모터 (Stepper Motor) ★출제·계산

- 펄스 신호 1개 = 정해진 각도(step angle)만큼 회전
- 오픈 루프 제어 가능

```
Step Angle = 360° / 전체 스텝 수

예) 28BYJ-48: 2048 스텝/회전
  → Step angle = 360/2048 ≈ 0.176°
```

### 스테퍼 모터 종류

| 종류 | 원리 | 정밀도 |
|---|---|---|
| Variable Reluctance (VR) | 철심 로터, 가변 자기 저항 | 낮음 |
| Permanent Magnet (PM) | 영구자석 로터 | 중간 |
| **Hybrid** | VR + PM 결합 | **가장 높음** |

### 구동 방식

| 방식 | 원리 | 특징 |
|---|---|---|
| 1상 여자 (Wave Drive) | 1개 코일만 활성화 | 토크 낮음 |
| 2상 여자 (Full Step) | 2개 코일 동시 활성화 | 토크 큼 |
| 하프 스텝 (Half Step) | 1상·2상 교대 | 분해능 2배, 더 부드러운 회전 |

---

## 6. 기어트레인 (Gear Train) ★계산

```
속도비: ω_out / ω_in = N_in / N_out
토크비: T_out / T_in = N_out / N_in

→ 감속비 높으면: 속도 감소, 토크 증가 (에너지 보존)

예) N_in=10, N_out=50 → 속도 ×(1/5), 토크 ×5
```

---

## 7. RC 서보 모터

**내부 구성:** DC모터 + 기어박스 + 포텐셔미터(위치 피드백) + 제어회로

```
PWM 신호로 각도 제어:
  1ms   펄스 → 0°   (한쪽 끝)
  1.5ms 펄스 → 90°  (중간, neutral position)
  2ms   펄스 → 180° (다른 쪽 끝)
  주기: 20~30ms (50Hz)
```
