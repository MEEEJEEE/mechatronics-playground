# coding: utf-8

import smbus
import time
import math

# smbus 객체 인스턴스 생성
bus = smbus.SMBus(1)

# IC 주소
address = 0x53

# 각 축의 데이터 주소
x_adr = 0x32
y_adr = 0x34
z_adr = 0x36

# 센서 IC를 초기화하는 함수
def init_ADXL345():
    # POWER_CTL 레지스터(주소: 0x2D)의 Measure 비트에 1을 써서 계측 시작
    bus.write_byte_data(address, 0x2D, 0x08)

# IC에서 데이터를 얻는 함수
def measure_acc(adr):
    # 각 축의 측정값 하위 바이트를 읽기
    acc0 = bus.read_byte_data(address, adr)
    # 각 축의 측정값 상위 바이트를 읽기
    acc1 = bus.read_byte_data(address, adr + 1)

    # 수신한 2바이트 데이터를 10비트 데이터로 합치기
    acc = (acc1 << 8) + acc0
    # 부호가 있는지 (10비트째가 1인지) 판정
    if acc > 0x1FF:
        # 음수로 변환
        acc = (65536 - acc) * -1
    # 가속도 값으로 변환 (단위: g)
    acc = acc * 3.9 / 1000

    return acc

# 기울임 각도 계산 함수
def calculate_tilt_angles(x_acc, y_acc, z_acc):
    """
    가속도 데이터로부터 Roll과 Pitch 각도를 계산
    Roll: Y축 기준 회전 (X-Z 평면에서의 기울임)
    Pitch: X축 기준 회전 (Y-Z 평면에서의 기울임)
    """
    
    # Roll 각도 계산 (Y축 중심 회전)
    # atan2(x, sqrt(y^2 + z^2))를 사용하여 더 정확한 계산
    roll = math.atan2(x_acc, math.sqrt(y_acc**2 + z_acc**2))
    
    # Pitch 각도 계산 (X축 중심 회전)
    # atan2(y, sqrt(x^2 + z^2))를 사용
    pitch = math.atan2(y_acc, math.sqrt(x_acc**2 + z_acc**2))
    
    # 라디안을 도(degree)로 변환
    roll_deg = math.degrees(roll)
    pitch_deg = math.degrees(pitch)
    
    return roll_deg, pitch_deg

# 예외 처리
try:
    # IC 초기화
    init_ADXL345()
    
    print("3축 가속도계 기울임 각도 측정")
    print("Ctrl+C로 종료")
    print("-" * 50)

    # 무한 반복
    while True:
        # 함수를 호출해서 데이터 얻음
        x_acc = measure_acc(x_adr)
        y_acc = measure_acc(y_adr)
        z_acc = measure_acc(z_adr)
        
        # 기울임 각도 계산
        roll, pitch = calculate_tilt_angles(x_acc, y_acc, z_acc)
        
        # 결과 표시
        print(f'X = {x_acc:6.3f}[g], Y = {y_acc:6.3f}[g], Z = {z_acc:6.3f}[g]')
        print(f'Roll = {roll:6.1f}°, Pitch = {pitch:6.1f}°')
        print("-" * 50)
        
        # 0.5초 대기
        time.sleep(0.5)

# 키보드에서 예외 검출
except KeyboardInterrupt:
    print("\n측정을 종료합니다.")
    pass
