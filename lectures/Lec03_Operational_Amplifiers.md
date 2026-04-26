# Lec03 — Operational Amplifiers (OP Amp)

> Chapter 5 | 기출 15점 배점, 계산 연계형

---

## 1. 증폭기 기본 개념

```
Vout = Av × Vin       (Av = Voltage Gain)
Z_in = Vin / Iin      (입력 임피던스)
Z_out = ΔVout / ΔIout (출력 임피던스)
```

- 실제 사용 시 **Negative Feedback(음의 피드백)** 과 함께 사용 → 선형 동작 범위 확보

---

## 2. 이상 OP Amp 3대 법칙 ★출제

| Rule | 조건 | 내용 |
|---|---|---|
| Rule 1 | Infinite Open Loop Gain | A = ∞ → 개방 루프 = 비교기(Comparator)로만 사용 |
| Rule 2 | Infinite Input Impedance | R_in = ∞, R_out = 0 → **I₊ = I₋ = 0** (입력 단자에 전류 없음) |
| Rule 3 | Zero Differential Input Voltage | **V₊ = V₋ (Virtual Short)** — 피드백이 있을 때만 성립 |

> **모든 OP Amp 분석 방법:** `I₊ = I₋ = 0`, `V₊ = V₋` 두 조건에서 KCL 적용

실제 OP Amp 수치: R_in = 10⁶~10¹²Ω, R_out = 10~1000Ω, Open Loop Gain = 10⁴~10⁶

---

## 3. 증폭기 회로별 수식 ★출제·계산

### 반전 증폭기 (Inverting Amplifier)

```
Vout = −(Rf/Rin) × Vin
```

- 이득 = −Rf/Rin (음수 → 신호 반전)
- V₊ = 0 이므로 V₋ = 0 (Virtual Ground)
- KCL 유도: Vin/Rin + Vout/Rf = 0

### 비반전 증폭기 (Non-Inverting Amplifier)

```
Vout = (1 + Rf/R) × Vin
```

- 이득 항상 ≥ 1 (양수)
- V₊ = Vin, V₋ = Vin (Rule 3 적용)

### 차동 증폭기 (Differential Amplifier) ★기출 직접 출제

```
Vout = (Rf/R1)(V2 − V1)       ← R1=R2, Rf=Rg 대칭 조건

일반 공식 (비대칭):
Vout = −(Rf/R1)·V1 + (1+Rf/R1)·(Rf/(R2+Rf))·V2
```

### 계측 증폭기 (Instrumentation Amplifier)

```
Vout = [R4/R3 × (1 + 2R2/R1)] × (V2 − V1)
```

- 차동 증폭기 앞에 비반전 버퍼 2개 추가
- 매우 높은 입력 임피던스 + 높은 CMRR
- 용도: 미세 차동 신호를 노이즈 환경에서 측정 (센서 적합)

### 가산 증폭기 (Summing Amplifier)

```
Vout = −[(R4/R1)V1 + (R4/R2)V2 + (R4/R3)V3]

R1=R2=R3, R1=3×R4 이면:
Vout = −(1/3)(V1+V2+V3)  ← 평균
```

### 전체 비교 요약

| 종류 | Vout 수식 | 이득 부호 | 특징 |
|---|---|---|---|
| 반전 | −(Rf/Rin)·Vin | 음수 | Virtual Ground |
| 비반전 | (1+Rf/R)·Vin | 양수, ≥1 | 높은 입력 임피던스 |
| 차동 | (Rf/R)(V2−V1) | 양수 | 공통 모드 제거 |
| 계측 | [Rf/R(1+2R2/Rg)](V2−V1) | 양수 | 최고 CMRR |
| 적분기 | −(1/RC)∫Vin dt | − | Rf 자리에 C |
| 미분기 | −RC·dVin/dt | − | Rin 자리에 C |

---

## 4. 적분기 / 미분기

| 회로 | 구조 변경 | 수식 |
|---|---|---|
| 적분기 (Integrator) | Rf 자리에 커패시터 C | `Vout(t) = −(1/RC)∫Vin(τ)dτ` |
| 미분기 (Differentiator) | Rin 자리에 커패시터 C | `Vout(t) = −RC·dVin/dt` |

---

## 5. Comparator (비교기) ★출제

- OP Amp를 **피드백 없이** 사용 → 아날로그 → 1비트 디지털 변환

```
V₊ > V₋  →  Vout = +Vsat (≈ 공급전압)
V₊ < V₋  →  Vout = −Vsat

예) 공급 ±5V:
  V₊ 쪽이 크면 → Vout ≈ +4.7V
  V₋ 쪽이 크면 → Vout ≈ −4.7V (또는 0.7V, 단극성 공급 시)
```

---

## 6. 실제 OP Amp 특성

- 출력 포화 전압(V_sat): 공급 전압보다 약간 낮음 (예: ±5V 공급 → 출력 ≈ ±4.7V)
- 입력 offset: 실제로는 V₊=V₋이어도 Vout≠0 → **Offset Null 핀**으로 보정
