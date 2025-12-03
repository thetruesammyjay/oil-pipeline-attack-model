# Oil Pipeline Attack Simulation Guide

This simulation demonstrates a "Stuxnet-style" attack scenario on critical infrastructure. It highlights the danger of Cyber-Physical attacks where the digital view (SCADA) and physical reality become decoupled.

## How to Run

Requires Python and the simpy library.

1. Install SimPy: `pip install simpy`
2. Run the script: `python pipeline_attack_sim.py`

## Understanding the Output

The logs are split into three logical views:

### 1. SCADA Monitor (The Operator's Screen)

This is what the humans in the control room see.

```text
[12s] SCADA Monitor | Reading: 300.00 PSI | Status: OK
```

- **Normal**: Reads actual pressure.
- **Under Attack**: Reads the static spoofed_value (300 PSI), leading the operator to believe everything is fine.

### 2. Reality Check (The Physical Truth)

This line (indented in the logs) reveals what is actually happening inside the steel pipe.

```text
>>> REALITY CHECK: Actual Pressure is 1250.00 PSI (Invisible to SCADA)
```

You will see this number rise rapidly after the attack begins.

Because the SCADA system is blinded, it fails to trigger the SAFETY_THRESHOLD shutoff.

### 3. Attack Events

```text
[---] Step 2: Injecting 'False Data' (Spoofing 300 PSI)...
[---] Step 3: Sending MODBUS command: CLOSE_VALVE_01...
```

- **Spoofing**: Disables the feedback loop.
- **Valve Close**: Causes the physical hazard (pressure buildup against a closed valve).

## Experiments to Try

You can modify the constants at the top of `pipeline_attack_sim.py` to test different defense strategies:

### Test the Safety System (Disable Spoofing)

Comment out the line `pipeline.sensor_spoofed = True` in the `attacker_process` function.

**Result**: The SCADA system will see the pressure rise, trigger the alarm at 1000 PSI, and shut off the pump before the pipe ruptures.

### Change the Buildup Rate

Modify `PUMP_BUILDUP_RATE`. If the pressure builds faster than the SCADA poll rate (`TICK_RATE`), the pipe might burst even without spoofing (a "Time-of-Check to Time-of-Use" vulnerability).

### Adjust Burst Limit

Lower `MAX_BURST_PRESSURE` to simulate an aging, corroded pipeline that is easier to attack.
