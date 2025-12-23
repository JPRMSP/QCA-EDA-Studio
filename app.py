import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config("QCA-EDA Studio", layout="wide")

st.title("🧬 QCA-EDA Studio")
st.caption("Quantum Cellular Automata – Architecture, Clocking, Fault & Memory Simulation")

# ---------------- CORE QCA FUNCTIONS ---------------- #

def majority(a, b, c):
    return np.sign(a + b + c)

def inverter(a):
    return -a

def aoi_gate(a, b, c):
    return inverter(majority(a, b, c))

# ---------------- CLOCKING ---------------- #

CLOCKS = ["Switch", "Hold", "Release", "Relax"]

def clock_phase(t):
    return CLOCKS[t % 4]

# ---------------- GRID SIMULATION ---------------- #

def qca_grid(inputs):
    grid = np.zeros((3,3))
    grid[1,0], grid[0,1], grid[1,2] = inputs
    grid[1,1] = majority(*inputs)
    return grid

# ---------------- DEFECT MODEL ---------------- #

def defect(cell, prob):
    if random.random() < prob:
        return random.choice([-1, 0, 1])
    return cell

# ---------------- SEQUENTIAL ---------------- #

def d_flip_flop(d, clk):
    return d if clk == "Hold" else None

# ---------------- MEMORY ---------------- #

def lut(address):
    table = {
        0: -1,
        1: 1
    }
    return table[address]

# ---------------- UI ---------------- #

st.sidebar.header("🔧 Inputs")
a = st.sidebar.selectbox("A", [-1, 1])
b = st.sidebar.selectbox("B", [-1, 1])
c = st.sidebar.selectbox("C", [-1, 1])

time = st.sidebar.slider("Clock Time", 0, 15, 0)
defect_prob = st.sidebar.slider("Defect Probability", 0.0, 0.5, 0.1)

# ---------------- LOGIC ---------------- #

maj = majority(a, b, c)
aoi = aoi_gate(a, b, c)
clk = clock_phase(time)

st.subheader("⚙️ Logic Outputs")
st.write("Majority Output:", maj)
st.write("AOI Output:", aoi)
st.write("Clock Phase:", clk)

# ---------------- GRID ---------------- #

grid = qca_grid([a, b, c])
grid_faulty = np.vectorize(lambda x: defect(x, defect_prob))(grid)

st.subheader("📐 QCA Grid (Fault-Aware)")
fig, ax = plt.subplots()
ax.imshow(grid_faulty, cmap="coolwarm", vmin=-1, vmax=1)
for i in range(3):
    for j in range(3):
        ax.text(j, i, grid_faulty[i,j], ha="center", va="center")
ax.set_xticks([])
ax.set_yticks([])
st.pyplot(fig)

# ---------------- SEQUENTIAL ---------------- #

st.subheader("🔁 Sequential Logic")
d = st.selectbox("D Input", [-1, 1])
ff = d_flip_flop(d, clk)
st.write("D Flip-Flop Output:", ff)

# ---------------- MEMORY ---------------- #

st.subheader("💾 LUT-Based QCA Memory")
addr = st.radio("Address", [0,1])
st.write("Memory Output:", lut(addr))

# ---------------- METRICS ---------------- #

st.subheader("📊 Design Metrics")
st.metric("Cell Count", 9)
st.metric("Clock Zones", 4)
st.metric("Estimated Fault Rate", f"{defect_prob*100:.1f}%")

st.caption("Anna University | FI9058 | QCA-EDA Studio")
