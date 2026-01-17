"""
Module for defining API routes related to exchange rates.
"""
from fastapi import APIRouter, Query, HTTPException, status

from app.services import RateService
from app.schemas import RateResponse, RateListResponse

router = APIRouter(prefix="/rates", tags=["Exchange Rates"])

@router.get("/today", summary="Get today's exchange rates", response_model=RateListResponse)
def get_today_exchange_rates():
    """
    Retrieve today's exchange rates.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_today_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for today.",
            )
        return rates
    finally:
        rate_service.dispose()


@router.get("/week", summary="Get rates for the last week", response_model=RateListResponse)
def get_last_week_exchange_rates():
    """
    Retrieve rates for the last week.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_last_week_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for this week."
            )
        return rates
    finally:
        rate_service.dispose()

@router.get("/month", summary="Get rates for the last month", response_model=RateListResponse)
def get_last_month_exchange_rates():
    """
    Retrieve rates for the last month.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_last_month_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for this month."
            )
        return rates
    finally:
        rate_service.dispose()


@router.get("/3months", summary="Get rates for the last 3 months", response_model=RateListResponse)
def get_last_3_months_exchange_rates():
    """
    Retrieve rates for the last 3 months.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_last_3_months_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for the last 3 months."
            )
        return rates
    finally:
        rate_service.dispose()


@router.get("/6months", summary="Get rates for the last 6 months", response_model=RateListResponse)
def get_last_6_months_exchange_rates():
    """
    Retrieve rates for the last 6 months.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_last_6_months_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for the last 6 months."
            )
        return rates
    finally:
        rate_service.dispose()

@router.get("/year", summary="Get rates for the last year", response_model=RateListResponse)
def get_last_year_exchange_rates():
    """
    Retrieve rates for the last year.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_last_year_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for the last year."
            )
        return rates
    finally:
        rate_service.dispose()

@router.get("/custom", summary="Get rates within a specified date range", response_model=RateListResponse)
def get_custom_exchange_rates(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    """
    Retrieve rates within a specified date range.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_rates_by_custom_range(start_date, end_date)
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found for the specified date range."
            )
        return rates
    finally:
        rate_service.dispose()

@router.get("/all", summary="Get all rates", response_model=RateListResponse)
def get_all_exchange_rates():
    """
    Retrieve all rates.
    """
    rate_service = RateService()
    try:
        rates = rate_service.get_all_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No rates found in the database."
            )
        return rates
    finally:
        rate_service.dispose()

@router.get("/{id}", summary="Get a rate by ID", response_model=RateResponse)
def get_rate_by_id(id: int):
    """
    Retrieve a rate by its ID.
    """
    rate_service = RateService()
    try:
        rate = rate_service.get_rate_by_id(id)
        if not rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rate not found."
            )
        return rate
    finally:
        rate_service.dispose()