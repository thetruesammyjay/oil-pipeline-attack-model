# Oil Pipeline Cyber-Physical Attack Simulation

A research framework and simulation tool for modeling Cyber-Physical Attacks on critical oil & gas infrastructure. This project demonstrates how adversaries couple physical sabotage with cyber-spoofing to bypass SCADA safety systems.

## 📋 Overview

Oil pipelines are complex Cyber-Physical Systems (CPS) where network packets control physical fluid dynamics. Traditional security models often treat these domains separately. This project merges them to demonstrate a "Stuxnet-style" attack vector:

* **Physical Layer**: Modeling fluid dynamics (pressure buildup, valve states, rupture limits).
* **Cyber Layer**: Modeling SCADA sensor networks, Man-in-the-Middle (MITM) attacks, and data spoofing.

The core simulation proves that a purely network-secured system can still fail catastrophically if the physical state is decoupled from the digital monitoring view.

## 🛠 Features

* **Cyber-Physical Simulation**: A Python simpy engine that runs simultaneous processes for the hydraulic physics and the SCADA control loop.
* **Attack Modeling**: Demonstrates a coordinated multi-stage attack:
  * Reconnaissance: Network infiltration.
  * Deception: Sensor spoofing (freezing pressure readings).
  * Destruction: Valve manipulation leading to over-pressure rupture.
* **Theoretical Frameworks**:
  * Graph Theory: Topology representation of pump stations and sensor nodes.
  * Attack Trees: Visualization of vulnerability paths (Physical vs. Cyber).
  * Game Theory: Stackelberg models for analyzing Defender vs. Attacker payoffs.

## 🚀 Getting Started

### Prerequisites

You need Python installed along with the simpy discrete-event simulation library.

```bash
pip install simpy
```

### Installation

```bash
git clone https://github.com/thetruesammyjay/oil-pipeline-attack-model.git
cd oil-pipeline-attack-model
```

### Running the Simulation

Execute the main simulation script:

```bash
python pipeline_attack_sim.py
```

### Understanding the Output

The simulation logs distinguish between the Operator's View (what the SCADA screen shows) and Physical Reality (what is happening in the pipe).

```text
[12s] SCADA Monitor | Reading: 300.00 PSI | Status: OK
      >>> REALITY CHECK: Actual Pressure is 1250.00 PSI (Invisible to SCADA)
```

If the attack is successful, you will see a CRITICAL FAILURE log indicating a pipeline rupture due to the safety system failing to trigger.

## 🧠 Methodology

### 1. Mathematical Model

The pipeline is modeled as a graph G = (V, E), where edges represent pipe segments governed by hydraulic continuity equations. The simulation simplifies the Bernoulli Principle to model pressure changes (ΔP) based on valve status and pump flow rates (Q).

### 2. The Attack Vector

We utilize a False Data Injection Attack (FDIA).

* **Normal State**: Sensor_reading = Pressure_actual
* **Attack State**: Sensor_reading = α (where α is a constant "safe" value), while Pressure_actual → ∞.

### 3. Game Theory Analysis

The project includes conceptual models for a Stackelberg Game, where the Defender (Operator) commits to a defense strategy (e.g., redundant sensors) and the Attacker chooses the optimal strike strategy to maximize physical damage (U_A).

## ⚠️ Disclaimer

**Educational Purpose Only.**

This software and documentation are designed strictly for academic research, security training, and defensive analysis. The authors do not condone nor support the use of this code for malicious activities against any infrastructure.

## 👤 Author

**Sammy Jay**

* GitHub: [@thetruesammyjay](https://github.com/thetruesammyjay)

Starred this repo? ⭐ Feel free to fork and contribute!
