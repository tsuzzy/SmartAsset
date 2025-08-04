"""
Financial calculation utilities
"""
import numpy as np
from typing import List, Dict, Any


def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio"""
    if not returns:
        return 0.0
    
    returns_array = np.array(returns)
    excess_returns = returns_array - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) != 0 else 0.0


def calculate_max_drawdown(returns: List[float]) -> float:
    """Calculate maximum drawdown"""
    if not returns:
        return 0.0
    
    cumulative = np.cumprod(1 + np.array(returns))
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    return np.min(drawdown)


def calculate_portfolio_volatility(weights: List[float], covariance_matrix: np.ndarray) -> float:
    """Calculate portfolio volatility"""
    if not weights or len(weights) != covariance_matrix.shape[0]:
        return 0.0
    
    weights_array = np.array(weights)
    return np.sqrt(weights_array.T @ covariance_matrix @ weights_array)


def calculate_portfolio_return(weights: List[float], returns: List[float]) -> float:
    """Calculate portfolio return"""
    if not weights or len(weights) != len(returns):
        return 0.0
    
    return np.dot(weights, returns)


def calculate_allocation_percentage(asset_value: float, total_portfolio_value: float) -> float:
    """Calculate asset allocation percentage"""
    if total_portfolio_value == 0:
        return 0.0
    
    return (asset_value / total_portfolio_value) * 100


def calculate_compound_annual_growth_rate(initial_value: float, final_value: float, years: float) -> float:
    """Calculate Compound Annual Growth Rate (CAGR)"""
    if initial_value <= 0 or years <= 0:
        return 0.0
    
    return (final_value / initial_value) ** (1 / years) - 1


def calculate_risk_metrics(returns: List[float]) -> Dict[str, float]:
    """Calculate comprehensive risk metrics"""
    if not returns:
        return {
            "volatility": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "var_95": 0.0
        }
    
    returns_array = np.array(returns)
    
    metrics = {
        "volatility": np.std(returns_array),
        "sharpe_ratio": calculate_sharpe_ratio(returns),
        "max_drawdown": calculate_max_drawdown(returns),
        "var_95": np.percentile(returns_array, 5)  # 95% VaR
    }
    
    return metrics


def calculate_optimal_weights(returns: List[List[float]], target_return: float = None) -> List[float]:
    """Calculate optimal portfolio weights using mean-variance optimization"""
    if not returns or len(returns) == 0:
        return []
    
    returns_array = np.array(returns)
    mean_returns = np.mean(returns_array, axis=1)
    cov_matrix = np.cov(returns_array)
    
    n_assets = len(mean_returns)
    
    # Simple equal weight allocation if no target return specified
    if target_return is None:
        return [1.0 / n_assets] * n_assets
    
    # For now, return equal weights
    # TODO: Implement proper mean-variance optimization when pyportfolioopt is available
    return [1.0 / n_assets] * n_assets


def calculate_correlation_matrix(returns: List[List[float]]) -> np.ndarray:
    """Calculate correlation matrix from returns"""
    if not returns or len(returns) == 0:
        return np.array([])
    
    returns_array = np.array(returns)
    return np.corrcoef(returns_array) 