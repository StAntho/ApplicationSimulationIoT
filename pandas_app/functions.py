import streamlit as st

def get_heart_rate_max(age):
    # Gellish & colleagues (2007)
    hrM = 191.5 - (0.007 * age ** 2)
    return round(hrM, 2)

def get_heart_rate_min(age):
    # Gellish & colleagues (2007)
    hrm = 163.5 - (0.006 * age ** 2)
    return round(hrm, 2)

def imc(weight, height):
    # Formula: weight (kg) / height (m) ^ 2
    return round(weight / (height / 100) ** 2, 2)

def caloric_expenditure(age, weight, heart_rate, duration):
    return ((-55.0969 + (0.6309 * heart_rate) + (0.1988 * weight) + (0.2017 * age)) / 4.184) * duration

def caloric_expenditure_bis(weight, distance):
    return 1.036 * weight * distance

def get_vo2_max(age, weight, heart_rate):
    return 15.3 * (heart_rate / (220 - age)) * weight

def get_vo2_max_bis(weight, heart_rate):
    return 3.5 * (heart_rate / 60) * weight

def training_intensity(heart_rate, heart_rate_max):
    return (heart_rate / heart_rate_max) * 100

def training_load(heart_rate, heart_rate_max, duration):
    return (heart_rate / heart_rate_max) * duration

def peak_expiratory_flow(age, height, weight):
    # Formula: (0.021 * age) + (0.041 * height) - (0.018 * weight) - 2.649
    return (0.021 * age) + (0.041 * height) - (0.018 * weight) - 2.649  

# Volume courant des poumons
def tidal_volume(weight):
    # Formula: 6.2 * weight
    return 6.2 * weight

# Index de fatigue
def fatigue_index(power, duration):
    # Formula: (power / duration) * 100
    return (power / duration) * 100

# Cyclisme
def get_tss(duration, power,):# Allen & Coggan's formula
    # NP = (sum(P^4) / N) ^ (1/4)
    # P: power in watts
    # N: number of data points
    np = (sum([p ** 4 for p in power]) / len(power)) ** (1/4)
    # Training Stress Score (TSS)
    # Andrew Coggan's formula
    ftp = 0.95 * (sum(power) / len(power))
    # TSS = (s * NP * IF) / (FTP * 3600) * 100
    # s: duration in seconds
    # NP: Normalized Power (NP)
    # FTP: Functional Threshold Power (FTP)
    # 3600: number of seconds in an hour
    # 100: scaling factor
    return (duration * np * (np/ftp)) / (ftp * 3600) * 100
