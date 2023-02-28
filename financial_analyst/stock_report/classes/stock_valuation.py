class StockValuation:
    def __init__(
        self: float,
        final_value: float,
        current_percentage: float,
        intrinsic_by_industry: float,
        historical: float,
        per_current_value: float,
        pcf_current_value: float,
        ps_current_value: float,
        pbv_current_value: float,
    ) -> None:
        self.final_value = final_value
        self.current_percentage = current_percentage
        self.intrinsic_by_industry = intrinsic_by_industry
        self.historical = historical
        self.per_current_value = per_current_value
        self.pcf_current_value = pcf_current_value
        self.ps_current_value = ps_current_value
        self.pbv_current_value = pbv_current_value
