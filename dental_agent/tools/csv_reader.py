import pandas as pd
from langchain_core.tools import tool

from dental_agent.config.settings import CSV_PATH, DATE_FORMAT


def _format_datetime_series(series: pd.Series) -> pd.Series:
    return series.dt.strftime(DATE_FORMAT).str.lstrip("0").str.replace("/0", "/", regex=False)


def _load_df() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()
    df["is_available"] = df["is_available"].astype(str).str.upper() == "TRUE"
    df["date_slot"] = pd.to_datetime(df["date_slot"], format="mixed", dayfirst=False)
    df["doctor_name"] = df["doctor_name"].fillna("").astype(str).str.lower().str.strip()
    df["specialization"] = df["specialization"].fillna("").astype(str).str.lower().str.strip()
    df["patient_to_attend"] = (
        df["patient_to_attend"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace("nan", "")
        .str.replace(r"\.0$", "", regex=True)
    )
    return df


@tool
def get_available_slots(
    specialization: str = "",
    doctor_name: str = "",
    date_filter: str = "",
) -> list:
    """Return available appointment slots."""
    df = _load_df()
    mask = df["is_available"]

    if specialization:
        mask = mask & (df["specialization"] == specialization.lower().strip())
    if doctor_name:
        mask = mask & (df["doctor_name"] == doctor_name.lower().strip())
    if date_filter:
        try:
            target_date = pd.to_datetime(date_filter).date()
            mask = mask & (df["date_slot"].dt.date == target_date)
        except Exception:
            pass

    result = df[mask][["date_slot", "specialization", "doctor_name"]].copy()
    result["date_slot"] = _format_datetime_series(result["date_slot"])
    return result.head(20).to_dict(orient="records")


@tool
def get_patient_appointments(patient_id: str) -> list:
    """Return all booked appointments for a given patient ID."""
    df = _load_df()
    mask = df["patient_to_attend"] == str(patient_id).strip()
    result = df[mask][["date_slot", "specialization", "doctor_name", "patient_to_attend"]].copy()
    result["date_slot"] = _format_datetime_series(result["date_slot"])
    return result.to_dict(orient="records")


@tool
def check_slot_availability(doctor_name: str, date_slot: str) -> dict:
    """Check if a specific doctor slot is available."""
    df = _load_df()
    try:
        target_dt = pd.to_datetime(date_slot, format="mixed", dayfirst=False)
    except Exception:
        return {"found": False, "is_available": False, "patient_to_attend": ""}

    mask = (df["doctor_name"] == doctor_name.lower().strip()) & (df["date_slot"] == target_dt)
    rows = df[mask]

    if rows.empty:
        return {"found": False, "is_available": False, "patient_to_attend": ""}

    row = rows.iloc[0]
    return {
        "found": True,
        "is_available": bool(row["is_available"]),
        "patient_to_attend": row["patient_to_attend"] or "",
    }


@tool
def list_doctors_by_specialization(specialization: str) -> list:
    """Return distinct doctor names for a given specialization."""
    df = _load_df()
    mask = df["specialization"] == specialization.lower().strip()
    return sorted(df[mask]["doctor_name"].unique().tolist())
