import simpy
import random

# --- CONFIGURATION ---
SIMULATION_TIME = 60      # Total simulation time in seconds
TICK_RATE = 1             # Physics update every 1 second
MAX_BURST_PRESSURE = 1500 # The physical limit of the pipe (PSI)
SAFETY_THRESHOLD = 1000   # SCADA triggers alarm above this (PSI)
NORMAL_PRESSURE = 300     # Operating pressure (PSI)
PUMP_BUILDUP_RATE = 150   # PSI increase per second when valve is closed

class OilPipeline:
    def __init__(self, env):
        self.env = env
        self.pressure = NORMAL_PRESSURE
        self.valve_open = True
        self.pump_on = True
        self.ruptured = False
        self.sensor_spoofed = False
        self.spoofed_value = 0
    
    def get_sensor_reading(self):
        """
        Returns the pressure reading. 
        If attacked (spoofed), returns the fake value.
        Otherwise, returns real physical pressure.
        """
        if self.sensor_spoofed:
            return self.spoofed_value
        return self.pressure

    def physics_model(self):
        """
        Simulates the continuous physical fluid dynamics.
        """
        while True:
            yield self.env.timeout(TICK_RATE)
            
            if self.ruptured:
                continue

            # Physics Logic: 
            # If Pump is ON and Valve is CLOSED, pressure builds up.
            # If Pump is OFF, pressure slowly dissipates.
            if self.pump_on and not self.valve_open:
                self.pressure += PUMP_BUILDUP_RATE + random.uniform(-10, 10) # Add some noise
            elif not self.pump_on:
                self.pressure = max(0, self.pressure - 50) # Pressure drops if pump off
            else:
                # Normal operation, pressure fluctuates slightly around normal
                self.pressure = NORMAL_PRESSURE + random.uniform(-5, 5)

            # Check for catastrophic failure
            if self.pressure >= MAX_BURST_PRESSURE:
                self.ruptured = True
                print(f"\n[!!!] CRITICAL FAILURE at t={self.env.now}: "
                      f"Pipeline RUPTURED! Pressure: {self.pressure:.2f} PSI")
                print("      -> Oil spill initiated. Environmental damage impending.")

def scada_system(env, pipeline):
    """
    The control room logic. Monitors sensors and triggers safety stops.
    """
    while True:
        yield self.env.timeout(TICK_RATE)
        
        if pipeline.ruptured:
            break

        # Read sensor (which might be lying!)
        reading = pipeline.get_sensor_reading()
        
        # SCADA Logic
        status = "OK"
        if reading > SAFETY_THRESHOLD:
            status = "ALARM! EMERGENCY STOP!"
            pipeline.pump_on = False # Safety shutoff
        
        print(f"[{env.now:02d}s] SCADA Monitor | Reading: {reading:6.2f} PSI | Status: {status}")
        
        # In a real scenario, SCADA logs would look normal during a spoofing attack
        # We print real pressure to console just for the user to see the reality gap
        if pipeline.sensor_spoofed:
             print(f"      >>> REALITY CHECK: Actual Pressure is {pipeline.pressure:.2f} PSI (Invisible to SCADA)")

def attacker_process(env, pipeline, attack_time):
    """
    Simulates the Cyber-Physical Attack.
    """
    yield env.timeout(attack_time)
    
    print(f"\n[---] ATTACK STARTED at t={env.now}")
    print("[---] Step 1: Compromising ICS Network...")
    print("[---] Step 2: Injecting 'False Data' (Spoofing 300 PSI)...")
    
    # 1. Blind the SCADA system
    pipeline.sensor_spoofed = True
    pipeline.spoofed_value = 300 # Fake normal reading
    
    yield env.timeout(2) # Short delay to simulate pivoting
    
    print("[---] Step 3: Sending MODBUS command: CLOSE_VALVE_01...")
    
    # 2. Physically disrupt the flow
    pipeline.valve_open = False
    
    print("[---] Attack Execution Complete. Waiting for physics to react...\n")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print(f"--- OIL PIPELINE ATTACK SIMULATION ---")
    print(f"Burst Limit: {MAX_BURST_PRESSURE} PSI")
    print(f"Safety Cutoff: {SAFETY_THRESHOLD} PSI")
    print(f"--------------------------------------")

    # Setup Environment
    env = simpy.Environment()
    pipe = OilPipeline(env)
    
    # Add processes to environment
    env.process(pipe.physics_model())       # The physical pipe
    env.process(scada_system(env, pipe))    # The control room
    
    # Schedule attack at t=10 seconds
    env.process(attacker_process(env, pipe, attack_time=10))
    
    # Run
    env.run(until=SIMULATION_TIME)
