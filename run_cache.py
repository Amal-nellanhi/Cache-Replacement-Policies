import m5
from m5.objects import *
import argparse

# 1. Parse Command Line Arguments for Policy
parser = argparse.ArgumentParser()
parser.add_argument('--policy', type=str, default='LRU', 
                    choices=['LRU', 'FIFO', 'Random', 'MRU'],
                    help='Replacement policy to use')
args = parser.parse_args()

# 2. Define the System
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing' # Required for gathering cache stats
system.mem_ranges = [AddrRange('512MB')] # Small memory for low-end laptop

# 3. CPU Setup (TimingSimple is faster than O3)
system.cpu = TimingSimpleCPU()

# 4. Cache Configuration
# We create a simple L1 Data Cache. 
# We ignore L1 Instruction Cache for simplicity (connect it to membus directly)
class MyL1Cache(Cache):
    assoc = 2              # 2-way set associative
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    size = '32kB'          # Small cache to force misses
    
    # DYNAMIC POLICY SWITCHING HERE
    def __init__(self, policy_name):
        super().__init__()
        if policy_name == 'LRU':
            self.replacement_policy = LRURP()
        elif policy_name == 'FIFO':
            self.replacement_policy = FIFORP()
        elif policy_name == 'Random':
            self.replacement_policy = RandomRP()
        elif policy_name == 'MRU':
            self.replacement_policy = MRURP() # Extra credit policy!

system.cpu.icache = MyL1Cache(args.policy)
system.cpu.dcache = MyL1Cache(args.policy)

# Connect Caches to CPU
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

# 5. Interconnect (Memory Bus)
system.membus = SystemXBar()

# Connect caches to memory bus
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

# 6. Interrupt Controller (Required for x86)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# 7. Memory Controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# 8. Set the Workload (Binary to run)
binary = 'workload' # Path to your compiled C binary
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# 9. Instantiate and Run
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Beginning simulation with policy: {args.policy}...")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")