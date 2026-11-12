"""hodgkin-huxley model of one patch of membrane, with hand-written integrators!

units: time in ms, voltage in mV, current density in uA/cm^2,
conductance in mS/cm^2, capacitance in uF/cm^2.

the state is a length-4 array y = [V, m, h, n].
"""

import math

import numpy as np

# classic HH parameters (squid axon, 6.3 C), shifted so rest is near -65 mV.
C_M = 1.0       # membrane capacitance
G_NA = 120.0    # max sodium conductance
G_K = 36.0      # max potassium conductance
G_L = 0.3       # leak conductance
E_NA = 50.0     # sodium reversal potential
E_K = -77.0     # potassium reversal potential
E_L = -54.387   # leak reversal, chosen so the resting potential is -65 mV
V_REST = -65.0


def _x_over_1_minus_exp(x, k):
    """return x / (1 - exp(-x / k)), using its limit k when x is near 0.

    alpha_m and alpha_n have this form; plugging in x = 0 directly would
    divide 0 by 0.
    """
    if abs(x) < 1e-6:
        return k
    return x / (1.0 - math.exp(-x / k))


def rates(v):
    """opening (alpha) and closing (beta) rates of the m, h, n gates at voltage v, in 1/ms."""
    alpha_m = 0.1 * _x_over_1_minus_exp(v + 40.0, 10.0)
    beta_m = 4.0 * math.exp(-(v + 65.0) / 18.0)
    alpha_h = 0.07 * math.exp(-(v + 65.0) / 20.0)
    beta_h = 1.0 / (1.0 + math.exp(-(v + 35.0) / 10.0))
    alpha_n = 0.01 * _x_over_1_minus_exp(v + 55.0, 10.0)
    beta_n = 0.125 * math.exp(-(v + 65.0) / 80.0)
    return alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n


def steady_state(v):
    """state [v, m, h, n] with every gate at its equilibrium value for a fixed v."""
    alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n = rates(v)
    m = alpha_m / (alpha_m + beta_m)
    h = alpha_h / (alpha_h + beta_h)
    n = alpha_n / (alpha_n + beta_n)
    return np.array([v, m, h, n])


def ionic_currents(y):
    """Sodium, potassium and leak currents (outward positive) for state y.

    Returns (i_na, i_k, i_l). Each is conductance x driving force.
    """
    V, m, h, n = y
    i_na = G_NA * (m**3 * h) * (V - E_NA)
    i_k = G_K * (n**4) * (V - E_K)
    i_l = G_L * (V - E_L)
    return (i_na, i_k, i_l)


def hh_rhs(t, y, i_ext):
    """dy/dt for the HH equations; i_ext is a function of time giving injected current.

    Returns np.array([dV/dt, dm/dt, dh/dt, dn/dt]).
    """
    v, m, h, n = y
    alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n = rates(v)
    i_na, i_k, i_l = ionic_currents(y)
    I = i_ext(t)
    dvdt = (I - i_na - i_k - i_l)/C_M
    dmdt = (alpha_m * (1 - m) ) - (beta_m * m)
    dhdt = (alpha_h * (1 - h)) - (beta_h * h)
    dndt = (alpha_n * (1 - n)) - (beta_n * n)
    return np.array([dvdt, dmdt, dhdt, dndt])


def euler_step(f, t, y, dt):
    """One forward-Euler step: follow the slope at the start for the whole step."""
    return y + dt * f(t, y)


def rk4_step(f, t, y, dt):
    """One classical Runge-Kutta (RK4) step: a weighted average of four slopes.

    Same inputs and output as euler_step above.
    """
    k1 = f(t, y)
    k2 = f(t + dt/2, y + (dt/2) * k1)
    k3 = f(t + dt/2, y + (dt/2) * k2)
    k4 =f(t + dt, y + dt * k3)
    return y + dt * ((k1 + 2*k2 + 2*k3 + k4)/6)

def no_current(t):
    return 0.0


def pulse(start, duration, amplitude):
    """Current that is `amplitude` for start <= t < start + duration, else 0."""
    def i_ext(t):
        return amplitude if start <= t < start + duration else 0.0
    return i_ext


def simulate(t_max, dt, i_ext=no_current, y0=None, method="rk4"):
    """Integrate the HH equations from t = 0 to t_max.

    Returns (t, y): t has shape (n_steps + 1,), y has shape (n_steps + 1, 4)
    with columns V, m, h, n. Starts at rest unless y0 is given.
    """
    step = {"rk4": rk4_step, "euler": euler_step}[method]
    n_steps = int(round(t_max / dt))
    t = np.arange(n_steps + 1) * dt
    y = np.empty((n_steps + 1, 4))
    y[0] = steady_state(V_REST) if y0 is None else y0

    def f(t_now, y_now):
        return hh_rhs(t_now, y_now, i_ext)

    for i in range(n_steps):
        y[i + 1] = step(f, t[i], y[i], dt)
    return t, y


def count_spikes(v, threshold=0.0):
    """Number of upward crossings of `threshold` mV in a voltage trace."""
    above = v >= threshold
    return int(np.sum(~above[:-1] & above[1:]))
