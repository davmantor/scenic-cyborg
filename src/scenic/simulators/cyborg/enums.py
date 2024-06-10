from enum import Enum, StrEnum, auto

class Images(StrEnum):
    KALI_BOX = "Kali_Box"
    INTERNAL = "Internal"
    GATEWAY = "Gateway"
    VELOCIRATOR_SERVER = "Velociraptor_Server"
    LINUX_USER_HOST1 = "linux_user_host1"
    LINUX_USER_HOST2 = "linux_user_host2"
    LINUX_DECOY_HOST1 = "linux_decoy_host"
    WINDOWS_USER_HOST1 = "windows_user_host1"
    WINDOWS_USER_HOST2 = "windows_user_host2"
    OP_SERVER = "OP_Server"

class AgentType(StrEnum):
    BEELINE = "B_Line"
    BLUE_MONITOR = "BlueMonitorAgent"
    BLUE_REACT = "BlueReactAgent"
    COUNTER_KILLCHAIN = "CounterKillchainAgent"
    GREEN = "GreenAgent"
    KILLCHAIN = "KillchainAgent"
    MEANDER = "Meander"
    SLEEP = "SleepAgent"

class BlueActions(StrEnum):
    ANALYSE = "Analyse"
    MONITOR = "Monitor"
    MISINFORM = "Misinform"
    REMOVE = "Remove"
    RESTORE = "Restore"
    SLEEP = "Sleep"

class RedActions(StrEnum):
    DISCOVER_NETWORK_SERVICES = "DiscoverNetworkServices"
    DISCOVER_REMOTE_SERVICES = "DiscoverRemoteServices"
    IMPACT = "Impact"
    PRIVILEDGE_ESCALATE = "PrivledgeEscalate"
    SLEEP = "Sleep"

class GreenActions(StrEnum):
    PING_SWEEP = "GreenPingSweep"
    PORT_SCAN = "GreenPortScan"
    CONNECTION = "GreenConnection"
    SLEEP = "Sleep"

class Artifacts(StrEnum):
    WINDOWS_PROCESS = "Windows.Events.ProcessCreation"
    LINUX_PROCESS = "Linux.Events.ProcessCreation"
    LINUX_PSLIST = "Linux.Sys.Pslist"
    PS_FOR_USER = "Custom.CybORG.Generic.System.Pslist"
    USER_INFO = "Custom.Wrappered.Windows.Sys.Users"
    CLIENT_COMMAND = "Custom.CybORG.Generic.RunClientCommand"
    WINDOWS_CLIENT_COMMAND = "Custom.Cyborg.Generic.RunWindowsClientCommand"

class RewardCalculator(StrEnum):
    NONE = "None"
    EMPTY = "EmptyRewardCalculator"
    CONFIDENTIALITY = "ConfidentialityRewardCalculator"
    AVAILABILITY = "AvailabilityRewardCalculator"
    BASELINE = "BaselineRewardCalculator"
    HYBRID_BLUE = "HybridAvailabilityConfidentialityRewardCalculator"
    PWM = "PwnRewardCalculator"
    DISRUPT = "DistruptRewardCalculator"
    HYBRID_RED = "HybridImpactPwnRewardCalculator"

class InitialAccessLevel(Enum):
    NONE = auto()
    IP = auto()
    ALL = auto()

class Availability(StrEnum):
    NONE = 'None'
    LOW = 'Low'
    MED = 'Medium'
    HI = 'High'

Confidentiality = Availability
