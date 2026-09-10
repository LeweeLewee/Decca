# Decca ADC noise diagnostic

Captured: 2026-09-06T21:05:02.1818551+01:00
Raw data: `adc-noise-20260906-203847.csv`

## Device output

firmware=0.27.1
ota_hostname=decca.local
phase_a_pwm=217
phase_b_pwm=255_constant_high_ledc_detached
transition=PHASE_A_START
transition=PHASE_A_END_SET_100_PERCENT
transition=PHASE_B_START_GPIO25_CONSTANT_HIGH
transition=PHASE_B_END_RESTORE_PRETEST_STATE
restored_pwm=217
summary_begin
phase,pot,signal,count,min,max,peak_to_peak,mean,stddev,largest_single_sample_excursion,ui_trigger_excursions
A,volume,raw,6000,944,975,31,963.173,3.787,21,21
A,volume,filtered,6000,953,967,14,963.770,1.429,11,0
A,bass,raw,6000,2023,2055,32,2044.314,4.074,27,25
A,bass,filtered,6000,2033,2048,15,2045.033,1.459,10,0
A,treble,raw,6000,2070,2097,27,2090.271,4.320,23,54
A,treble,filtered,6000,2079,2095,16,2091.099,1.579,10,0
A,balance,raw,6000,2009,2033,24,2029.259,4.072,22,7
A,balance,filtered,6000,2017,2032,15,2030.092,1.443,11,0
B,volume,raw,6000,944,975,31,963.485,3.529,26,19
B,volume,filtered,6000,954,968,14,964.047,1.312,10,0
B,bass,raw,6000,2026,2059,33,2044.798,3.794,23,20
B,bass,filtered,6000,2033,2049,16,2045.416,1.244,10,0
B,treble,raw,6000,2070,2096,26,2090.753,3.874,23,32
B,treble,filtered,6000,2079,2095,16,2091.421,1.380,11,0
B,balance,raw,6000,2009,2037,28,2029.562,3.729,21,8
B,balance,filtered,6000,2019,2033,14,2030.289,1.257,10,0
summary_end
diagnostic_complete
