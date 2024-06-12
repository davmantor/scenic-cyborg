from enum import Enum, StrEnum, auto
from typing import Optional

class Image(Enum):
    KALI_BOX = "Kali_Box", (0.9, 0.05, 0.05), "root"
    INTERNAL = "Internal", (0.1, 0.1, 0.1), "SYSTEM"
    GATEWAY = "Gateway", (0.25, 0.6, 0.25), "root"
    VELOCIRAPTOR_SERVER = "Velociraptor_Server", (0.05, 0.25, 0.8), "root"
    LINUX_USER_HOST1 = "linux_user_host1", (0, 0.9, 0.15), "root"
    LINUX_USER_HOST2 = "linux_user_host2", (0, 0.9, 0.15), "root"
    LINUX_DECOY_HOST1 = "linux_decoy_host",  (0.6, 0.25, 0.25), "root"
    WINDOWS_USER_HOST1 = "windows_user_host1", (0.05, 0.75, 0.05), "SYSTEM"
    WINDOWS_USER_HOST2 = "windows_user_host2", (0.05, 0.75, 0.05), "SYSTEM"
    OP_SERVER = "OP_Server", (0.25, 0.25, 0.25), "root"

    def __init__(self, value: str, color: tuple[int], username: str):
        self.color = color
        self.username = username

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
    EXPLOIT_REMOTE_SERVICE = "ExploitRemoteService"
    PRIVILEDGE_ESCALATE = "PrivledgeEscalate"
    IMPACT = "Impact"
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
    PWN = "PwnRewardCalculator"
    DISRUPT = "DistruptRewardCalculator"
    HYBRID_RED = "HybridImpactPwnRewardCalculator"

class InitialAccessLevel(Enum):
    NONE = auto()
    IP = auto()
    ALL = auto()

class Confidentiality(StrEnum):
    NONE = 'None'
    LOW = 'Low'
    MED = 'Medium'
    HI = 'High'

Availability = Confidentiality

# Maps types to sets of possible images
class SubnetKind(Enum):
    # Gateway is defined so that we can use it as a valid target for green sessions; there should not be one in the user network
    USER = {Image.LINUX_USER_HOST1: 0.15, Image.LINUX_USER_HOST2: 0.15, Image.WINDOWS_USER_HOST1: 0.35, Image.WINDOWS_USER_HOST2: 0.35, Image.GATEWAY: 0}, None, 5
    ENTERPRISE = {Image.INTERNAL: 1}, Image.GATEWAY, 4
    OPER = {Image.OP_SERVER: 1}, Image.GATEWAY, 6
    # DECOY = {Image.LINUX_DECOY_HOST1: 1}, Image.GATEWAY, 4

    def __init__(self, images: dict[Image, float], makeOne: Optional[Image], sz: int):
        self._value = self.name.capitalize()
        self.images = images
        self.makeOne = makeOne
        self.size = sz
