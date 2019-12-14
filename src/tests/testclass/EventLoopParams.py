from typing import List
from typing import Dict

from dataclasses import dataclass


@dataclass
class EventLoopParams:

    mi_dict:         Dict[int, str]
    la_dict                         = {}
    mi_lista:        List[int]
    la_lista                        = []
    use_sleep:       bool           = False
    relative_pause:  bool           = False
    do_draw:         bool           = True
    relative_warmup: int            = 4
    last_click_time: float          = 1000.0
    num_clicks:      int            = 2
    mi_nombre:       str            = 'hasii'
