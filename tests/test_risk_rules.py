import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.clean import calculate_risk

def test_high_risk_grade_threshold():
    assert calculate_risk({"G3": 9, "absences": 0}) == "High"

def test_high_risk_absence_threshold():
    assert calculate_risk({"G3": 15, "absences": 16}) == "High"

def test_medium_risk_grade_threshold():
    assert calculate_risk({"G3": 13, "absences": 0}) == "Medium"

def test_medium_risk_absence_threshold():
    assert calculate_risk({"G3": 15, "absences": 11}) == "Medium"

def test_low_risk():
    assert calculate_risk({"G3": 14, "absences": 10}) == "Low"
