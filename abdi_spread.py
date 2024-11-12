\subsection{Abdi's Method for Spread Calculation}

Abdi's spread estimator provides a closed-form solution that relies on the covariance of close-to-mid-range returns around the same closing price. The formula for the spread is given by:

\[
\text{Spread} = 2p \cdot \mathbb{E}\left[(c_t - \eta_t)(c_t - \eta_{t+1})\right]
\]

where:
\begin{itemize}
    \item \( c \) is the daily closing log-price,
    \item \( \eta \) is the daily mid-range, calculated as the average of the daily high and low log-prices:
    \[
    \eta_t = \frac{\ln(H_t) + \ln(L_t)}{2}
    \]
\end{itemize}

This method is similar to Roll's autocovariance measure but uses the covariance of close-to-mid-range returns rather than consecutive close-to-close price returns.

\begin{tcolorbox}[colback=white!95!gray, colframe=black, title=Python Code: Calculation of Abdi's Spread]
\begin{lstlisting}[language=Python, basicstyle=\ttfamily\small]
import numpy as np

def abdi_spread(close_prices, high_prices, low_prices, p=1):
    # Ensure there are enough data points
    if len(close_prices) < 2:
        return None
    # Calculate daily mid-range values
    mid_range = (np.log(high_prices) + np.log(low_prices)) / 2
    # Calculate daily close-to-mid-range differences
    eta_diffs = close_prices - mid_range
    # Calculate covariance between (ct - ηt) and (ct - ηt+1)
    cov_matrix = np.cov(eta_diffs[:-1], eta_diffs[1:])
    cov_value = cov_matrix[0, 1]
    # Calculate spread using the covariance value
    spread = 2 * p * cov_value if cov_value is not None else None
    return spread


\end{lstlisting}
\end{tcolorbox}
