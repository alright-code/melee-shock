from abc import abstractmethod, ABC
from melee_shock.models import Player, OutputMode
import logging

logger = logging.getLogger(__name__)


class BaseAPI(ABC):
    def __init__(self, players: dict[int, Player]):
        self.players = players

    def _map_shockers(self):
        self.shocker_map: dict[int, int] = {}
        num_enabled = sum(
            1 for p in self.players.values() if p.output_mode != OutputMode.DISABLED
        )
        if num_enabled > len(self.shocker_ids):
            raise RuntimeError(
                f"Not enough shockers for enabled players: {num_enabled} enabled but only {len(self.shocker_ids)} shockers found"
            )
        shocker_idx = 0
        for port, player in self.players.items():
            if player.output_mode != OutputMode.DISABLED:
                self.shocker_map[port] = self.shocker_ids[shocker_idx]
                shocker_idx += 1
        logger.info("Mapped shockers to ports: %s", self.shocker_map)

    @abstractmethod
    def beep(self, port: int, duration: int):
        pass

    @abstractmethod
    def vibrate(self, port: int, intensity: int, duration: int):
        pass

    @abstractmethod
    def shock(self, port: int, intensity: int, duration: int):
        pass
